import time

import docker
import os
import shutil
import stat

client = docker.from_env()


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def delete_folder(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path, onerror=remove_readonly)
        print(f"Folder '{folder_path}' deleted successfully.")
    else:
        print(f"Folder '{folder_path}' does not exist.")


def build_docker_container(dockerfile_path="./", image_name="image", container_name='container',
                           building_logs=True, container_logs=True, delete_if_exist=True):
    try:
        if delete_if_exist:
            if container_exists(container_name):
                print(f'Deleting a container \'{container_name}\'...')
                container = client.containers.get(container_name)
                container.stop()
                container.remove()

            if image_exists(image_name):
                print(f'Deleting an image \'{image_name}\'...')
                image = client.images.get(image_name)
                client.images.remove(image.id)

        print(f"Building Docker-image '{image_name}'...")
        image, build_logs = client.images.build(path=dockerfile_path, tag=image_name)

        if building_logs:
            for log in build_logs:
                if 'stream' in log:
                    print(log['stream'].strip())

        print(f"Image '{image_name}' created successfully.")

        print(f"Starting a container '{container_name}'...")
        container = client.containers.run(
            image=image_name,
            detach=True,
            name=container_name,
            ports={"8080/tcp": 8080},
            #environment={"MY_ENV_VAR": "example_value"}
        )

        print(f"Сontainer '{container.name}' started successfully")

        if container_logs:
            print("Container logs:")
            print(container.logs().decode("utf-8"))

    except docker.errors.BuildError as e:
        print(f"Exception while building docker-image: {e}")
    except docker.errors.APIError as e:
        print(f"Exception while starting docker-container: {e}")


def container_exists(container_name):
    container_names = [c.name for c in client.containers.list(all=True)]
    return container_name in container_names


def image_exists(image_name):
    images = client.images.list()
    for image in images:
        if image_name in image.tags:
            return True
    return False


if __name__ == '__main__':
    image_name = 'image1'
    container_name = 'container1'

    build_docker_container(dockerfile_path='./cloned_repository/', image_name=image_name,
                                 container_name=container_name)

    time.sleep(10)

    route = '/hello Miku'
    url = f"http://localhost:8080{route}"
    response = __import__('requests').get(url)
    print(response.text)

    if input('Delete container and image (y/n)') == 'y':
        print('Deleting a container...')
        container = client.containers.get(container_name)
        container.stop()
        container.remove()

        print('Deleting an image...')
        image = client.images.get(image_name)
        client.images.remove(image.id)
