# renombrador.py
import os
import time
from automatizador_descarga import download_dir

# Directorio donde se descargan los archivos
download_dir = download_dir  # Usa una cadena cruda para evitar errores de escape

# Ruta del archivo txt con los nombres
nombres_marcas = os.path.join(download_dir, 'marcas.txt')

# Leer el archivo y almacenar cada línea en una lista
with open(nombres_marcas, 'r') as file:
    nombres_marcas_list = [line.strip() for line in file]

# Función para renombrar el archivo descargado
def rename_downloaded_file(original_filename, new_filename):
    original_file_path = os.path.join(download_dir, original_filename)
    new_file_path = os.path.join(download_dir, new_filename)
    while not os.path.exists(original_file_path):
        time.sleep(1)
    os.rename(original_file_path, new_file_path)

# Renombrar archivos en un bucle
def renombrar_archivos_autofix():
    for i in range(7):
        if i == 0:
            original_filename = 'AutoFix Repuestos.xlsx'  # Primer archivo sin número
        else:
            original_filename = f'AutoFix Repuestos({i}).xlsx'  # Archivos numerados
        new_filename = f'AutoFix Repuestos {nombres_marcas_list[i]}.xlsx'
        rename_downloaded_file(original_filename, new_filename)
        print(f'Renombrado {original_filename} a {new_filename}')