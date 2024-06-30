import pandas as pd
import os
from datetime import datetime
import logging
import re

# Configuracion del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#Lee un archivo Excel y devuelve un dataframe
def read_excel_file(folder_path, file_name, header_row=0):
    file_path = os.path.join(folder_path, file_name)
    if not os.path.isfile(file_path):
        logger.error(f"No se encontró el archivo '{file_name}' en la ruta '{folder_path}'.")
        raise FileNotFoundError(f"No se encontró el archivo '{file_name}' en la ruta '{folder_path}'.")
    logger.info(f"Leyendo archivo Excel: {file_path}")
    return pd.read_excel(file_path, header=header_row)

#Guarda el DataFrame en un archivo Excel con la fecha actual
def save_dataframe_to_excel(df, folder_path, file_prefix):
    today = datetime.today().strftime('%Y-%m-%d')
    output_file = os.path.join(folder_path, f"{file_prefix} {today}.xlsx")
    df.to_excel(output_file, index=False)
    logger.info(f"Archivo guardado en: {output_file}")

def clean_autorepuestos_data(df):
    logger.info("Limpiando datos de AutoRepuestos Express")
    # Eliminar filas en blanco y resetear indice
    df = df.dropna(how='all').reset_index(drop=True)
    columns_to_drop = ['PRECIO OFERTA/OUTLET', 'IVA', 'CODIGO BARRA', 'CODIGO MARCA', 'CODIGO RUBRO', 'RUBRO']
    # Eliminar columnas
    df = df.drop(columns=columns_to_drop, errors='ignore')
    # Cambiar nombres de columnas
    df = df.rename(columns={'CODIGO PROVEEDOR': 'CODIGO', 'PRECIO DE LISTA': 'PRECIO'})
    # Cambiar formato de PRECIO, punto (.) como separador de decimales, y ningún separador de miles
    df['PRECIO'] = df['PRECIO'].apply(lambda x: f'{x:.2f}'.replace(',', ''))
    # modificar DESCRIPCION a un maximo de 100 caracteres
    if 'DESCRIPCION' in df.columns:
        df['DESCRIPCION'] = df['DESCRIPCION'].astype(str).str[:100]
    return df

# Limpia y transforma los datos de las hojas de AutoFix Repuestos
def clean_autofix_data(dfs):
    logger.info("Limpiando datos de AutoFix Repuestos")
    # Combinar todas las hojas en un solo DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.rename(columns={'DESCR': 'DESCRIPCION'}, inplace=True)
    # Cambiar formato de PRECIO, punto (.) como separador de decimales, y ningún separador de miles
    combined_df['PRECIO'] = combined_df['PRECIO'].apply(lambda x: f'{x:.2f}'.replace(',', ''))
    columns_to_drop = ['FOTO', 'COEF', 'CODRUB', 'CANPED', 'ORIGEN', 'DESCR2', 'NROORI', 'CODPRO']
    # Eliminar columnas
    combined_df = combined_df.drop(columns=columns_to_drop, errors='ignore')
    return combined_df

#Limpia y transforma los datos de Mundo RepCar
def clean_mundo_repcar_data(df):
    logger.info("Limpiando datos de Mundo RepCar")
    # Eliminar columnas
    df.drop(columns=['Imagen', 'Iva 105', 'Cod. Articulo'], inplace=True)
    df = df.rename(columns={'Importe': 'PRECIO', "Cod. Fabrica": 'CODIGO'})
    # Cambiar formato de PRECIO, punto (.) como separador de decimales, y ningún separador de miles
    df['PRECIO'] = df['PRECIO'].apply(lambda x: f'{x:.2f}'.replace(',', ''))
    # Combinar descripción y rubro
    df['DESCRIPCION'] = df['Descripcion'] + ' ' + df['Rubro']
    # Eliminar columnas
    df.drop(columns=['Descripcion', 'Rubro'], inplace=True)

    # Limpiar valores en la columna MARCA
    if 'Marca' in df.columns:
        #Elimina asteriscos, parentesis y espacios en blanco al inicio y al final
        df['Marca'] = df['Marca'].apply(lambda x: re.sub(r'\*\*|\*|\(.*?\)', '', x).strip())
        df = df.rename(columns={'Marca': 'MARCA'})
    return df

def autorepuestos_data():
    folder_path = os.path.abspath("./Files")
    file_name = "AutoRepuestos Express.xlsx"
    try:
        df = read_excel_file(folder_path, file_name, header_row=10)
        df = clean_autorepuestos_data(df)
        save_dataframe_to_excel(df, folder_path, "AutoRepuestos Express")
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")

def autofix_data():
    folder_path = os.path.abspath("./Files")
    file_name = "AutoFix Repuestos.xlsx"
    try:
        xls = pd.ExcelFile(os.path.join(folder_path, file_name))
        # Leer cada hoja del dataframe
        dfs = [pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names]
        for sheet, df in zip(xls.sheet_names, dfs):
            # Agregar columna MARCA con el nombre de la hoja
            df['MARCA'] = sheet
        # Limpiar y combinar datos
        combined_df = clean_autofix_data(dfs)
        # Guardar el dataframe
        save_dataframe_to_excel(combined_df, folder_path, "AutoFix")
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")

def mundo_repcar_data():
    folder_path = os.path.abspath("./Files")
    csv_filename = "AutoRepuestos Express Lista de Precios.csv"
    try:
        # Leer el archivo csv
        df = pd.read_csv(os.path.join(folder_path, csv_filename), delimiter=';')
        df = clean_mundo_repcar_data(df) # Limpia los datos
        #Guarda el dataframe
        save_dataframe_to_excel(df, folder_path, "Mundo RepCar")
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")


