import os
import requests


def upload_file_to_api(file_name):
    print(file_name)
    folder_path = os.path.abspath("./Files")
    file_path = os.path.join(folder_path, file_name)
    url = "https://desafio.somosait.com/api/upload/"
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            print(f"Archivo subido con éxito: {response.json().get('link')}")
        else:
            print(f"Error al subir el archivo: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Exception occurred: {e}")


