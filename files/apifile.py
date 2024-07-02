import requests
import os

# URL del endpoint de la API
url = "https://desafio.somosait.com/api/upload/"


directorio_archivos = r'C:\\User\\Files\\Descargas'  # Ajusta la ruta según tu caso

# Obtener la lista de archivos .xlsx en el directorio
archivos_xlsx = [archivo for archivo in os.listdir(directorio_archivos) if archivo.endswith('.xlsx')]

for archivo in archivos_xlsx:
    # Construir el path completo al archivo
    filepath = os.path.join(directorio_archivos, archivo)

    # Configurar la petición POST con form-data
    files = {'file': open(filepath, 'rb')}
    response = requests.post(url, files=files)

    # Procesar la respuesta de la API
    if response.status_code == 200:
        # Éxito en la subida
        print(f"Archivo {archivo} subido correctamente.")
        print(f"Respuesta de la API: {response.json()}")
    elif response.status_code == 400:
        # Error: columnas requeridas faltantes
        try:
            error_message = response.json()['message']
        except KeyError:
            error_message = "Error al subir el archivo."
        print(f"Error al subir {archivo}: {error_message}")
    else:
        # Otro tipo de error
        print(f"Error al subir {archivo}. Código de estado: {response.status_code}")
