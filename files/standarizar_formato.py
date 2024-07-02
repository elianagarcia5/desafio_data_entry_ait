"""
---------------
En el caso del archivo AutoRepuestos Express, 
no se puedo realizar un script dinamico 
para buscar los campos requeridos, 
para probar el funcionmiento correcto del procesado, se recomienda 
borrar del archivo AutoRepuestos Express.xlms las primeras 10 filas
y dejar en 1 fila los nombres de las columnas
---------------
"""
import os
import pandas as pd
from datetime import datetime



# Obtener la fecha actual
fecha_actual = datetime.now().strftime('%Y-%m-%d')

# Función para procesar y estandarizar cada archivo de lista de precios
def procesar_lista_precios(proveedor, input_filepath):
    columnas_requeridas = ['CODIGO', 'DESCRIPCION', 'MARCA', 'PRECIO']
    skiprows = 0  # Por defecto no se salta ninguna fila
    
    try:
        if proveedor == 'AutoRepuestos Express':
            skiprows = 10  # Salta las primeras 10 filas solo para AutoRepuestos Express
        
        df = pd.read_excel(input_filepath, skiprows=skiprows)
        
        # Procesar los datos según el proveedor
        if proveedor.startswith('AutoFix'):
            df.rename(columns={'DESCR': 'DESCRIPCION'}, inplace=True)
            
        elif proveedor == 'AutoRepuestos Express':
            df.rename(columns={'CODIGO PROVEEDOR': 'CODIGO', 'PRECIO DE LISTA': 'PRECIO'}, inplace=True)

        elif proveedor == 'Mundo RepCar':
            # Convertir valores numéricos a cadenas antes de concatenar
            df['Descripcion'] = df['Descripcion'].astype(str)
            df['Rubro'] = df['Rubro'].astype(str)
            df['DESCRIPCION'] = df['Descripcion'] + ' - ' + df['Rubro']
            df.rename(columns={'Cod. Fabrica': 'CODIGO', 'Importe': 'PRECIO'}, inplace=True)
            if 'MARCA' not in df.columns:
                df['MARCA'] = ''  # Placeholder si no existe la columna de marca

        # Verificar que las columnas necesarias existen en el DataFrame
        for columna in columnas_requeridas:
            if columna not in df.columns:
                raise KeyError(f"La columna requerida '{columna}' no está presente en el archivo {input_filepath}.")

        # Seleccionar las columnas estandarizadas
        df = df[columnas_requeridas]
        return df

    except Exception as e:
        raise ValueError(f"Error al leer el archivo: {e}")

# Función para procesar y estandarizar los archivos de los proveedores
def estandarizar_archivos(proveedores, download_dir):
    for proveedor in proveedores:
        input_filename = f'{proveedor}.xlsx'
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