import os
from datetime import datetime
from AutomateBrowser.ListProcessing import autorepuestos_data, autofix_data, mundo_repcar_data
from AutomateBrowser.DownloadLists import AutomateDownloads
from AutomateBrowser.UploadToApi import upload_file_to_api

with AutomateDownloads(teardown=True) as browser:
   browser.autorepuestos_list()
   browser.autofix_list()
   browser.mundo_repcar_list()

#Limpieza y procesamiento de listas
autorepuestos_data()
autofix_data()
mundo_repcar_data()

#Subida de Listas a la API
   # Ejercicio incompleto. Las listas tienen las columnas solicitadas
   # pero la validacion de la api informa que faltan columnas
today = datetime.today().strftime('%Y-%m-%d') # Fecha de hoy
list_proveedores = [f'AutoRepuestos Express {today}.xlsx', f'Mundo RepCard {today}.xlsx', f'Mundo RepCar {today}.xlsx']
for file_name in list_proveedores:
   upload_file_to_api(file_name)




