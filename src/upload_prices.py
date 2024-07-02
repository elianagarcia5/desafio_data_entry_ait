import requests
import os
from datetime import datetime

def upload_to_api(file_path):
    url = "https://desafio.somosait.com/api/upload/"
    print(file_path)

    # Nombre del archivo
    filename = os.path.basename(file_path)
    print(filename)

    try:
        with open(file_path, "rb") as f:
            r = requests.post(url, files={'file': f})
            # Verificar status de respuesta de la solicitud
            if r.status_code == 200:
                print(f"Subida exitosa para {filename}.")
            elif r.status_code == 400:
                print(f"Error para {filename}: Faltan columnas requeridas en el archivo.")
                print(r.text)
    except FileNotFoundError:
        print("The file was not found.")
    except requests.exceptions.RequestException as e:
        print("There was an exception that occurred while handling your request.", e)


# Carpeta donde se encuentran los archivos
folder_path = "C:\\Users\\nCuello\\Desktop\\AIT solutions\\desafio_data_entry_ait\\data\\processed_files"

# Obtener la lista de archivos en la carpeta
file_names = os.listdir(folder_path)

# Iterar sobre cada archivo
for file_name in file_names:
    # Comprobar que sea un archivo .xlsx
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)  # Ruta completa al archivo
        upload_to_api(file_path)
    else:
        print(f"Ignorando archivo {file_name} porque no es un archivo .xlsx")
