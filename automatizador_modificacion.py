# automatizador.py
import os
from files.modificar_formato_archivo import csv_to_excel
from files.renombrar_archivos_autofix import renombrar_archivos_autofix
from files.unificar_archivos_autofix import procesar_y_guardar_autofix
from files.standarizar_formato import estandarizar_archivos



# Directorio donde se descargan los archivos
download_dir = r'C:\\Users\\Feder\\Downloads' #Cambiar direccion a gusto, recomendacion lugar predeterminado del navegador

# Listas de marcas Autofix
proveedores_autofix = [
        'AutoFix Repuestos FIAT',
        'AutoFix Repuestos CHEVROLET',
        'AutoFix Repuestos VOLKSWAGEN',
        'AutoFix Repuestos CITROEN',
        'AutoFix Repuestos TOYOTA',
        'AutoFix Repuestos FORD',
        'AutoFix Repuestos RENAULT'
]

# Llama a la función para renombrar los archivos descargados de AutoFix
renombrar_archivos_autofix()
# Llama a la función para procesar y guardar los archivos AutoFix
procesar_y_guardar_autofix(proveedores_autofix, download_dir)


# Especifica la ruta del archivo CSV que deseas convertir
csv_file_path = os.path.join(download_dir, 'AutoRepuestos Express Lista de Precios.csv')
# Especifica la ruta y el nombre del archivo Excel de salida
excel_file_path = os.path.join(download_dir, 'Mundo RepCar.xlsx')
# Llama a la función para convertir el archivo
csv_to_excel(csv_file_path, excel_file_path)



# Listas de proveedores y archivos a procesar
proveedores = [
        'AutoRepuestos Express', 
        'Mundo RepCar',
        'AutoFix'
]

# Llama a la función para estandarizar los archivos de los proveedores
estandarizar_archivos(proveedores, download_dir)