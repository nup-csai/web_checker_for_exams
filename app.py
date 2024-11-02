import threading

from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path
from contextlib import redirect_stdout
import pygit2
import requests
import time

import utils
import settings

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def check_answer(answer, right_answer):
    return answer.strip() == right_answer.strip()


def check_page_content(content, right_answer):
    return content.strip() == right_answer.strip()


def check_solution(code):
    test_directory_name = 'tests'

    test_filenames = sorted([i for i in os.listdir(test_directory_name) if i.startswith('test')])

    answers_filenames = sorted([i for i in os.listdir(test_directory_name) if i.startswith('answer')])
    answers = []
    for answers_filename in answers_filenames:
        with open(f'{test_directory_name}/{answers_filename}', 'r', encoding='utf-8') as file:
            answers.append(file.read())

    test_info = []

    for i, test_filename in enumerate(test_filenames):
        input_filename = f'{test_directory_name}/{test_filename}'
        output_filename = 'output.txt'
        error_on_current_test = False
        with open(input_filename, 'r', encoding='utf-8') as file, open(output_filename, 'w',
                                                                       encoding='utf-8') as output_file:
            original_stdin = sys.stdin
            sys.stdin = file
            try:
                with redirect_stdout(output_file):
                    exec(code)
            except Exception as e:
                test_info.append([f'Test {i + 1}', 'RT'])
                error_on_current_test = True
            sys.stdin = original_stdin

        if not error_on_current_test:
            with open(output_filename, 'r', encoding='utf-8') as output_file:
                answer = output_file.read()
            if check_answer(answer, answers[i]):
                test_info.append([f'Test {i + 1}', 'OK'])
            else:
                test_info.append([f'Test {i + 1}', 'WA'])

    return jsonify(testing_data=test_info)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    code = data.get('text')

    return check_solution(code)


@app.route('/apply_requirements', methods=['POST'])
def apply_requirements():
    data = request.get_json()
    settings.routes = data.get('routes', [])
    return jsonify({"message": "Files updated successfully"}), 200


@app.route('/check_solution_from_github', methods=['POST'])
def check_solution_from_github():
    local_path = './cloned_repository'

    utils.delete_folder(local_path)

    repo_url = settings.repositories[0]  #'https://github.com/KonstBeliakov/test_repository.git'
    local_path = './cloned_repository'
    pygit2.clone_repository(repo_url, local_path)

    image_name = 'image1'
    container_name = 'container1'

    dockerfile_path = "./cloned_repository/Dockerfile"

    # Checking for presence/absence of different files in the repository
    files_checking_results = []
    for filename in settings.files_that_should_exist:
        file_path = f'./cloned_repository/{filename}'
        path = Path(file_path)
        if path.is_file():
            files_checking_results.append([f"'{filename}'", 'OK'])
        else:
            files_checking_results.append([f"'{filename}'", "Doesn't exist"])

    # If there is no Dockerfile program will try to run main.py from the cloned repository
    if not Path(dockerfile_path).is_file():
        print(f'Dockerfile is not found. Trying to run main.py from {local_path}/')
        try:
            with open(f'./cloned_repository/main.py', 'r', encoding='utf-8') as f:
                code = f.read()
            t1 = threading.Thread(target=lambda: exec(code))
            t1.start()
        except:
            pass
    else:
        print('Dockerfile found')
        utils.build_docker_container(dockerfile_path='./cloned_repository/', image_name=image_name,
                                     container_name=container_name)

    time.sleep(5)  # waiting for program to start

    checking_results = []

    for i, (route, right_answer) in enumerate(settings.routes, start=1):
        print(f'Test {i}')
        try:
            url = f"http://localhost:8080{route}"
            response = requests.get(url)
            content = response.text
            print(f'\troute: {route}')
            print(f'\tcontent: {content}')
            print(f'\tright answer: {right_answer}')
        except Exception as e:
            print(e)
            checking_results.append([f'Test {i}', 'RT'])
        else:
            if check_page_content(str(content), right_answer):
                checking_results.append([f'Test {i}', 'OK'])
            else:
                checking_results.append([f'Test {i}', 'WA'])

    print('Checking results:')
    print(checking_results)
    print()

    print('Deleting a container...')
    container = utils.client.containers.get(container_name)
    container.stop()
    container.remove()

    print('Deleting an image...')
    image = utils.client.images.get(image_name)
    utils.client.images.remove(image.id)

    return jsonify(routes_checking=checking_results, files_checking=files_checking_results)


@app.route('/dynamic_fields/<name>', methods=['POST'])
def dynamic_fields(name):
    match name:
        case 'files':
            data = request.get_json()
            settings.files_that_should_exist = data.get('data', [])
            print('settings.files_that_should_exist', settings.files_that_should_exist)
            return jsonify({"message": "Files updated successfully"}), 200
        case 'repositories':
            data = request.get_json()
            settings.repositories = data.get('data', [])
            print('settings.repositories', settings.repositories)
            return jsonify({"message": "Files updated successfully"}), 200
        case _:
            return jsonify({"error": "Invalid name provided"}), 404


if __name__ == '__main__':
    app.run(port=8081)
