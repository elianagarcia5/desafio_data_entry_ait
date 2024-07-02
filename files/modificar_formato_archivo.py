import os
import csv
from xlsxwriter.workbook import Workbook

def csv_to_excel(csv_file_path, excel_file_path):
    # Verifica que el archivo CSV existe
    if not os.path.isfile(csv_file_path):
        print(f"El archivo {csv_file_path} no existe.")
        return

    # Crea un archivo Excel con el nombre especificado
    workbook = Workbook(excel_file_path)
    worksheet = workbook.add_worksheet()

    # Lee el archivo CSV y escribe los datos en el archivo Excel
    with open(csv_file_path, 'rt', encoding='utf8') as f:
        reader = csv.reader(f, delimiter=';')
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)

    # Cierra el archivo Excel
    workbook.close()
    print(f"Archivo convertido y guardado en {excel_file_path}")

# Especifica la ruta del archivo CSV que deseas convertir
csv_file_path = 'C:\\Users\\Feder\\Downloads\\AutoRepuestos Express Lista de Precios.csv'

# Especifica la ruta y el nombre del archivo Excel de salida
excel_file_path = 'C:\\Users\\Feder\\Downloads\\Mundo RepCar.xlsx'

# Llama a la función para convertir el archivo
csv_to_excel(csv_file_path, excel_file_path)
