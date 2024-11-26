import json
import threading

from flask import Flask, render_template, request, jsonify, Response
from pathlib import Path
import pygit2
import requests
import time
import sqlite3
import logging

import utils

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)


@app.route('/')
def index():
    return render_template('index.html')


def check_page_content(content, right_answer):
    return content.strip() == right_answer.strip()


@app.route('/apply_requirements', methods=['POST'])
def apply_requirements():
    data = request.get_json()

    utils.executemany_sql_in_new_connection("INSERT INTO Routes (route, content) VALUES (?, ?)", data.get('routes', []))

    return jsonify({"message": "Files updated successfully"}), 200


def check_files(data, files, repo_id, cursor, connection):
    """
    Checking for presence/absence of different files in the repository
    :param data: data that will be submitted to JS (will be modified in this function)
    :param files: list of files that should exist in the repository
    :param repo_id: id of this repository in database
    :param cursor: cursor (to execure sql)
    :param connection: connection (to commit changes in the database)
    :return: None
    """
    logging.info(f"Checking files if repo №{repo_id}")
    for i, filename in enumerate(files):
        file_path = f'./cloned_repository/{filename}'
        path = Path(file_path)
        if path.is_file():
            data[repo_id]['routes_checking'][i][1] = 'OK'
            status = 'OK'
        else:
            data[repo_id]['routes_checking'][i][1] = "Doesn't exist"
            status = "Doesn't exist"
        cursor.execute("SELECT id FROM Files WHERE name=?", (filename,))
        file_id = cursor.fetchone()[0]
        cursor.executemany("INSERT INTO FileChecking (repository_id, file_id, status) VALUES (?, ?, ?)",
                           [(repo_id, file_id, status)])
        connection.commit()

    logging.info(f'Results of checking files in repo №{repo_id}:\n{data[repo_id]['routes_checking']}')


def check_routes(id_route_content, data, repo_id, cursor, connection):
    """
    This function checks the contents of pages corresponding to routes
    :param id_route_content: list of lists containing 3 elements: id, route and expected content of the page
    :param data: data that will be submitted to JS (will be modified in this function)
    :param repo_id: id of repository in the database
    :param cursor: cursor (to execure sql)
    :param connection: connection (to commit changes in the database)
    :return: None
    """
    logging.info(f"Checking routes in repo №{repo_id}")
    for route_id, route, right_answer in id_route_content:
        try:
            url = f"http://localhost:8080{route}"
            response = requests.get(url)
            content = response.text
        except Exception as e:
            data[repo_id]['files_checking'][route_id - 1][1] = 'RT'
            status = 'RT'
        else:
            if check_page_content(str(content), right_answer):
                data[repo_id]['files_checking'][route_id - 1][1] = 'OK'
                status = 'OK'
            else:
                data[repo_id]['files_checking'][route_id - 1][1] = 'WA'
                status = 'WA'

        cursor.executemany("INSERT INTO RoutesChecking (repository_id, route_id, status) VALUES (?, ?, ?)",
                           [(repo_id, route_id, status)])
        connection.commit()

    logging.info(f'Results of checking routes in repo №{repo_id}:\n{data[repo_id]['files_checking']}')


def run_solution(local_path, image_name, container_name):
    """
    This function runs code from cloned repository (if there is Dockerfile, docker container will be built, otherwise
    main.py will be started
    :param local_path: path to the cloned repository
    :param image_name: name of docker image that will be created
    :param container_name: name of docker container that will be created
    :return: None
    """
    logging.info(f"Running solution from github {local_path}")
    dockerfile_path = f"{local_path}/Dockerfile"
    # If there is no Dockerfile program will try to run main.py from the cloned repository
    if not Path(dockerfile_path).is_file():
        logging.info(f"Dockerfile is not found. Trying to run main.py from {local_path}/")
        try:
            with open(f'./cloned_repository/main.py', 'r', encoding='utf-8') as f:
                code = f.read()
            t1 = threading.Thread(target=lambda: exec(code))
            t1.start()
        except:
            pass
    else:
        logging.info(f"Dockerfile found. Building a container {container_name}")
        utils.build_docker_container(dockerfile_path='./cloned_repository/', image_name=image_name,
                                     container_name=container_name, building_logs=False, container_logs=False)


@app.route('/check_solution_from_github')
def check_solution_from_github():
    """
    This function clones github repository, checks for presence/absence of some files
    in the repository (function gets list of files from database),
    tries to build a Docker container with cloned repository and checks content of pages corresponding to routes
    from the database
    :return: returns a function that yields jsons for requests to the frontend
    """
    def generate():
        conn = sqlite3.connect("database.sqlite")
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM Files")
        files = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT repository_link FROM Repositories")
        repository_links = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT id FROM Repositories")
        repository_ids = [i[0] for i in cursor.fetchall()]

        cursor.execute("SELECT id, route, content FROM Routes")
        id_route_content = cursor.fetchall()

        data = [[] for _ in range(len(repository_links) + 1)]
        for repo_id, repo_url in zip(repository_ids, repository_links):
            local_path = './cloned_repository'

            utils.delete_folder(local_path)

            local_path = './cloned_repository'
            pygit2.clone_repository(repo_url, local_path)

            data[repo_id] = {'routes_checking': [[f"'{filename}'", 'NS'] for filename in files],
                              'files_checking': [[f'Test {i + 1}', 'NS'] for i in range(len(id_route_content))]}


            yield f"data: {json.dumps({'data': data[1:]})}\n\n"

            check_files(data, files, repo_id, cursor, conn)

            yield f"data: {json.dumps({'data': data[1:]})}\n\n"

            image_name = 'image1'
            container_name = 'container1'

            run_solution(local_path, image_name, container_name)

            time.sleep(5)  # waiting for program to start

            check_routes(id_route_content, data, repo_id, cursor, conn)

            utils.delete_container_and_image(container_name, image_name)
        cursor.close()

    return Response(generate(), mimetype='text/event-stream')


@app.route('/dynamic_fields/<name>', methods=['POST'])
def dynamic_fields(name):
    match name:
        case 'files':
            data = request.get_json()
            records = [(i,) for i in data.get('data', [])]
            utils.executemany_sql_in_new_connection("INSERT INTO Files (name) VALUES (?)", records)
            return jsonify({"message": "Files updated successfully"}), 200
        case 'repositories':
            data = request.get_json()
            records = [(i,) for i in data.get('data', [])]
            utils.executemany_sql_in_new_connection("INSERT INTO Repositories (repository_link) VALUES (?)", records)
            return jsonify({"message": "Files updated successfully"}), 200
        case _:
            return jsonify({"error": "Invalid name provided"}), 404


if __name__ == '__main__':
    utils.execute_sql_file('./sql/drop_database.sql')
    utils.execute_sql_file('./sql/schema.sql')

    app.run(port=8081)
