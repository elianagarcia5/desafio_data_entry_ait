import pandas as pd
import os
from sqlalchemy import create_engine, MetaData, Table, select, insert, update
from datetime import datetime
import re

from AutomateBrowser.constants import db_config


def get_name_proveedor(file_name):
    # expresion regular para tener el nombre del archivo sin la fecha
    match = re.match(r"(.+?) \d{4}-\d{2}-\d{2}", file_name)
    if match:
        proveedor_name = match.group(1)
    else:
        raise ValueError(f"El nombre del archivo '{file_name}' no tiene el formato esperado.")
    return proveedor_name


def upload_to_database(file_name, db_config):
    # Llamar a la funcion para extraer y guardar nombre del proveedor
    proveedor_name = get_name_proveedor(file_name)

    folder_path = os.path.abspath("../Files")
    file = pd.ExcelFile(os.path.join(folder_path, file_name))
    # Leer archivo Excel
    df = pd.read_excel(file)

    # Conectar a la db
    db_url = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['hostname']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(db_url)
    connection = engine.connect()
    metadata = MetaData()

    # Cargar las tablas
    proveedor_table = Table('Proveedor', metadata, autoload_with=engine)
    actualizacion_table = Table('Actualizacion', metadata, autoload_with=engine)
    repuesto_table = Table('Repuesto', metadata, autoload_with=engine)
    marca_table = Table('Marca', metadata, autoload_with=engine)

    # Guardar la fecha de actualizacion
    fecha_actualizacion = datetime.now().date()

    # Guardar proveedor_id
    proveedor_id = connection.execute(
        select(proveedor_table.c.id).where(proveedor_table.c.nombre == proveedor_name)).scalar()

    if proveedor_id is None:
        raise ValueError(f"El proveedor '{proveedor_name}' no existe en la base de datos.")

    # Registrar la actualizacion
    insert_actualizacion = insert(actualizacion_table).values(fecha=fecha_actualizacion, proveedor_id=proveedor_id)
    actualizacion_id = connection.execute(insert_actualizacion).inserted_primary_key[0]

    # Procesar cada repuesto en el DataFrame
    for index, row in df.iterrows():
        codigo = row['CODIGO']
        descripcion = row['DESCRIPCION']
        marca_name = row['MARCA']
        precio = row['PRECIO']

        # Guardar marca_id (crearla si no existe)
        marca_id = connection.execute(select(marca_table.c.id).where(marca_table.c.nombre == marca_name)).scalar()

        if marca_id is None:
            # Insertar la nueva marca
            insert_marca = insert(marca_table).values(nombre=marca_name)
            marca_id = connection.execute(insert_marca).inserted_primary_key[0]

        # Verificar si el repuesto ya existe
        existing_repuesto = connection.execute(
            select(repuesto_table).where(repuesto_table.c.codigo == codigo)).fetchone()

        if existing_repuesto:
            # Actualizar el precio del repuesto
            update_repuesto = update(repuesto_table).where(repuesto_table.c.id == existing_repuesto.id).values(
                precio=precio,
                ultima_actualizacion_id=actualizacion_id
            )
            connection.execute(update_repuesto)
        else:
            # Cargar nuevo repuesto
            insert_repuesto = insert(repuesto_table).values(
                codigo=codigo,
                descripcion=descripcion,
                precio=precio,
                marca_id=marca_id,
                proveedor_id=proveedor_id,
                ultima_actualizacion_id=actualizacion_id
            )
            connection.execute(insert_repuesto)
    connection.close()

upload_to_database('AutoRepuestos Express 2024-06-30.xlsx', db_config)
