import os
import pandas as pd
from datetime import datetime

def process_autofix(file_path):
    xls = pd.ExcelFile(file_path)
    data_frames = []

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df['MARCA'] = sheet_name

        # Seleccion de columnas necesarias
        df = df[['CODIGO', 'DESCR', 'PRECIO', 'MARCA']]

        # Renombrar las columnas
        df.rename(columns={'DESCR': 'DESCRIPCION'}, inplace=True)

        # Modificar formato de las columnas
        df['PRECIO'] = df['PRECIO'].astype(str).str.replace(',', '.').astype(float).map(lambda x: f'{x:.2f}')
        df['DESCRIPCION'] = df['DESCRIPCION'].str.slice(0, 100)

        data_frames.append(df)

    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
        combined_df = combined_df[['CODIGO', 'DESCRIPCION', 'MARCA', 'PRECIO']]

        today = datetime.today().strftime('%Y-%m-%d')
        filename = f"Autofix_{today}.xlsx"
        save_path = os.path.join("C:\\Users\\nCuello\\Desktop\\AIT solutions\\desafio_data_entry_ait\\data\\processed_files", filename)
        combined_df.to_excel(save_path, index=False)
        print(f"Archivo procesado y guardado como {save_path}")
    else:
        print("No se encontraron datos válidos para combinar en Autofix.")

def process_autorepuestos(file_path):
    # Leer el archivo Excel
    df = pd.read_excel(file_path, header=10)  # Comenzar desde la fila 11

    # Renombrar columnas
    df.rename(columns={
            'CODIGO PROVEEDOR': 'CODIGO',
            'DESCRIPCION': 'DESCRIPCION',
            'PRECIO DE LISTA': 'PRECIO',
            'MARCA': 'MARCA'
        }, inplace=True)

    # Ajustar formato de columnas
    df['PRECIO'] = df['PRECIO'].astype(str).str.replace(',', '.').astype(float).map(lambda x: f'{x:.2f}')
    df['DESCRIPCION'] = df['DESCRIPCION'].str.slice(0, 100)

    # Eliminar columnas innecesarias
    columns_to_drop = ['PRECIO OFERTA/OUTLET', 'CODIGO RUBRO', 'RUBRO', 'CODIGO MARCA', 'IVA', 'CODIGO BARRA']
    df.drop(columns_to_drop, axis=1, inplace=True)
    
    # Guardar el nuevo archivo .xlsx
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f"Autorepuestos_Express_{today}.xlsx"
    save_path = os.path.join("C:\\Users\\nCuello\\Desktop\\AIT solutions\\desafio_data_entry_ait\\data\\processed_files", filename)
    df.to_excel(save_path, index=False)
    print(f"Archivo procesado y guardado como {save_path}")

def process_mundorepcar(file_path):
    # Leer el archivo csv
    df = pd.read_csv(file_path, sep=';')

    # Renombrar columnas
    df.rename(columns={
            'Cod. Fabrica': 'CODIGO',
            'Descripcion': 'DESCRIPCION',
            'Importe': 'PRECIO',
            'Marca': 'MARCA'
        }, inplace=True)
    
    # Ajustar formato de columnas
    df['PRECIO'] = df['PRECIO'].astype(str).str.replace(',', '.').astype(float).map(lambda x: f'{x:.2f}')
    df['DESCRIPCION'] = df['DESCRIPCION'].str.slice(0, 100)

    # Eliminar columnas innecesarias
    columns_to_drop = ['Cod. Articulo', 'Rubro', 'Iva 105', 'Imagen']
    df.drop(columns_to_drop, axis=1, inplace=True)
    # Guardar el nuevo archivo .xlsx
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f"MundoRepCar_{today}.xlsx"
    save_path = os.path.join("C:\\Users\\nCuello\\Desktop\\AIT solutions\\desafio_data_entry_ait\\data\\processed_files", filename)
    df.to_excel(save_path, index=False)
    print(f"Archivo procesado y guardado como {save_path}")

def process_prices():
    downloaded_files_dir = 'C:\\Users\\nCuello\\Desktop\\AIT solutions\\desafio_data_entry_ait\\data\\downloaded_files'

    for file in os.listdir(downloaded_files_dir):
        file_path = os.path.join(downloaded_files_dir, file)
        print(file)
        if "Autofix" in file:
            process_autofix(file_path)
        elif "AutoRepuestos Express" in file:
            process_autorepuestos(file_path)
        elif "MundoRepCar" in file:
            process_mundorepcar(file_path)

if __name__ == "__main__":
    process_prices()
