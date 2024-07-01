"""
---------------
En el caso del archivo AutoRepuestos Express, 
no se puedo realizar un script dinamico 
para buscar los campos requeridos, 
para probar el funcionmiento se recomienda 
borrar del archivo AutoRepuestos Express.xlms las primeras 10 filas
---------------
"""

import os
import pandas as pd
from datetime import datetime


# Directorio donde se descargan los archivos
download_dir = r'C:\\Users\\Feder\\Downloads'

# Listas de proveedores y archivos a procesar
proveedores_autofix = [
    'AutoFix Repuestos FIAT',
    'AutoFix Repuestos CHEVROLET',
    'AutoFix Repuestos VOLKSWAGEN',
    'AutoFix Repuestos CITROEN',
    'AutoFix Repuestos TOYOTA',
    'AutoFix Repuestos FORD',
    'AutoFix Repuestos RENAULT'
]
proveedores = [
    'AutoRepuestos Express', 
    'AutoRepuestos Express Lista de Precios'
]

# Obtener la fecha actual
fecha_actual = datetime.now().strftime('%Y-%m-%d')

# Función para procesar y estandarizar cada archivo de lista de precios
def procesar_lista_precios(proveedor, input_filepath):
    columnas_requeridas = ['CODIGO', 'DESCRIPCION', 'MARCA', 'PRECIO']
    
    try:
        if input_filepath.endswith('.xlsx'):
            # Leer el archivo Excel
            try:
                df = pd.read_excel(input_filepath)
            except ValueError:
                # Intentar leer desde la fila 11 si no se encuentran las columnas en las primeras filas
                df = pd.read_excel(input_filepath, skiprows=10)
                if not all(col in df.columns for col in columnas_requeridas):
                    raise ValueError(f"No se encontraron las columnas requeridas en {input_filepath}")

        elif input_filepath.endswith('.csv'):
            # Leer el archivo CSV
            try:
                df = pd.read_csv(input_filepath)
            except ValueError:
                # Intentar leer desde la fila 11 si no se encuentran las columnas en las primeras filas
                df = pd.read_csv(input_filepath, skiprows=10)
                if not all(col in df.columns for col in columnas_requeridas):
                    raise ValueError(f"No se encontraron las columnas requeridas en {input_filepath}")

        else:
            raise ValueError(f"Formato de archivo no soportado: {input_filepath}")

    except Exception as e:
        raise ValueError(f"Error al leer el archivo: {e}")

    # Procesar los datos según el proveedor
    if proveedor.startswith('AutoFix'):
        df.rename(columns={'DESCR': 'DESCRIPCION'}, inplace=True)
        df['MARCA'] = proveedor.split()[-1]

    elif proveedor == 'AutoRepuestos Express':
        df.rename(columns={'CODIGO PROVEEDOR': 'CODIGO', 'PRECIO DE LISTA': 'PRECIO'}, inplace=True)

    elif proveedor == 'AutoRepuestos Express Lista de Precios':
        df.rename(columns={'Cod. Fabrica': 'CODIGO', 'Descripcion': 'DESCRIPCION', 'Importe': 'PRECIO'}, inplace=True)
        if 'MARCA' not in df.columns:
            df['MARCA'] = ''  # Placeholder si no existe la columna de marca

    # Verificar que las columnas necesarias existen en el DataFrame
    for columna in columnas_requeridas:
        if columna not in df.columns:
            raise KeyError(f"La columna requerida '{columna}' no está presente en el archivo {input_filepath}.")

    # Seleccionar las columnas estandarizadas
    df = df[columnas_requeridas]

    return df

# Procesar y combinar archivos AutoFix
autofix_combined_df = pd.DataFrame()
for proveedor in proveedores_autofix:
    input_filename = f'{proveedor}.xlsx'
    input_filepath = os.path.join(download_dir, input_filename)
    if os.path.exists(input_filepath):
        try:
            df = procesar_lista_precios(proveedor, input_filepath)
            autofix_combined_df = pd.concat([autofix_combined_df, df], ignore_index=True)
        except (KeyError, ValueError) as e:
            print(e)
    else:
        print(f'Archivo {input_filename} no encontrado.')

# Guardar el DataFrame combinado en un nuevo archivo Excel
if not autofix_combined_df.empty:
    autofix_output_filename = f'AutoFix_{fecha_actual}.xlsx'
    autofix_output_filepath = os.path.join(download_dir, autofix_output_filename)
    autofix_combined_df.to_excel(autofix_output_filepath, index=False)
    print(f'Archivo combinado de AutoFix procesado y guardado como {autofix_output_filename}')
else:
    print('No se encontraron archivos válidos para combinar de AutoFix.')

# Procesar los archivos para otros proveedores
for proveedor in proveedores:
    input_filename = f'{proveedor}.xlsx' if proveedor != 'AutoRepuestos Express Lista de Precios' else f'{proveedor}.csv'
    input_filepath = os.path.join(download_dir, input_filename)
    if os.path.exists(input_filepath):
        try:
            df = procesar_lista_precios(proveedor, input_filepath)
            
            # Crear el nombre del archivo de salida
            output_filename = f'{proveedor}_{fecha_actual}.xlsx'
            output_filepath = os.path.join(download_dir, output_filename)

            # Guardar el DataFrame en un nuevo archivo Excel
            df.to_excel(output_filepath, index=False)
            print(f'Archivo procesado y guardado como {output_filename}')
        except (KeyError, ValueError) as e:
            print(e)
    else:
        print(f'Archivo {input_filename} no encontrado.')