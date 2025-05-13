import time
import json
from fastapi import Body
import configparser
from dotenv import load_dotenv
import os
import sys
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse

SETTINGS_PATH = os.getenv("SETTINGS_PATH")
KAPLAN = os.getenv("KAPLAN")
PROC = os.getenv("PROC")

config = configparser.ConfigParser()
config.read(SETTINGS_PATH)

DOC_DATA = "descripcion.docx"
MASTER_DIR = os.path.join(config["frontend_path"]["public_path"], "master")

async def zip_download():
    """
    Generar un archivo ZIP con los resultados de las estadisticas
    """
    folder_path = PROC
    zip_path = '/tmp/statistics.zip'

    shutil.make_archive(base_name=zip_path.replace('.zip', ''), format='zip', root_dir=folder_path)

    time.sleep(0.5)

    if not os.path.exists(zip_path):
        raise HTTPException(status_code=500, detail="No se pudo generar el ZIP")

    return FileResponse(
        path=zip_path,
        filename="statistics.zip",
        media_type="application/zip"
    )

async def get_kaplanImage(image_name: str):
    
    folder_path = KAPLAN
    image_path = os.path.join(folder_path, image_name)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    return FileResponse(image_path, media_type='image/png')

async def upload_files(files: list[UploadFile] = File(...)) -> dict:
    """
    Copiar archivos proporcionados por el usuario a la carpeta de trabajo.
    """
        
    raw_data_path = os.path.join(os.path.dirname(__file__), '../../../data/raw')
    proc_data_path = os.path.join(os.path.dirname(__file__), '../../../data/processed')
    os.makedirs(raw_data_path, exist_ok=True)
    os.makedirs(MASTER_DIR, exist_ok=True)
    os.makedirs(proc_data_path, exist_ok=True)
    
    new_paths = []
    file_path = ""
    for file in files:
        if file.filename.endswith('.json'):
            new_filename = 'master.json'
            file_path = os.path.join(MASTER_DIR, new_filename)
            proc_file_path = os.path.join(proc_data_path, new_filename)

            file_content = file.file.read()

            with open(file_path, 'wb') as buffer:
                buffer.write(file_content)

            with open(proc_file_path, 'wb') as buffer:
                buffer.write(file_content)


        elif file.filename.endswith('.xlsx'):
            new_filename = 'BD.xlsx'
            file_path = os.path.join(raw_data_path, new_filename)
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
        else:
            return JSONResponse(status_code=400, content={"message": "Formato de archivo no permitido"})

        new_paths.append(file_path)
    
    return {"message": "Archivos copiados exitosamente", "paths": new_paths}