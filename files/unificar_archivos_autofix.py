import os
import pandas as pd
from datetime import datetime


# Obtener la fecha actual
fecha_actual = datetime.now().strftime('%Y-%m-%d')

# Función para obtener la marca del proveedor
def obtener_marca(proveedor):
    return proveedor.split()[-1]

# Función para procesar y combinar archivos AutoFix y guardar en un archivo Excel
def procesar_y_guardar_autofix(proveedores_autofix, download_dir):
    autofix_combined_df = pd.DataFrame()
    for proveedor in proveedores_autofix:
        input_filename = f'{proveedor}.xlsx'
        input_filepath = os.path.join(download_dir, input_filename)
        if os.path.exists(input_filepath):
            try:
                df = pd.read_excel(input_filepath)
                
                # Agregar la columna de marca
                marca = obtener_marca(proveedor)
                df['MARCA'] = marca
                
                # Concatenar al DataFrame combinado
                autofix_combined_df = pd.concat([autofix_combined_df, df], ignore_index=True)
                
            except (KeyError, ValueError) as e:
                print(e)
        else:
            print(f'Archivo {input_filename} no encontrado.')
    
    # Guardar el DataFrame combinado en un archivo Excel
    if not autofix_combined_df.empty:
        autofix_output_filename = 'Autofix.xlsx'
        autofix_output_filepath = os.path.join(download_dir, autofix_output_filename)
        autofix_combined_df.to_excel(autofix_output_filepath, index=False)
        print(f'Archivo combinado de AutoFix procesado y guardado como {autofix_output_filename}')
    else:
        print('No se encontraron archivos válidos para combinar de AutoFix.')