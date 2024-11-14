import requests
import sys

if __name__ == '__main__':
    url = "http://localhost:8081/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Server is available: 200.")
        else:
            print(f"Server answered with code: {response.status_code}")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Cant connect to the server on localhost:8081.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Exception: {e}")
        sys.exit(1)
