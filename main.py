import shutil
from typing import Callable
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from db import DocInDB 
import db 
from datetime import date
from typing import Dict
import dropbox
import tempfile
import os

app = FastAPI()

today = date.today()

database_docs = Dict[str, DocInDB]
database_docs = {
    1: DocInDB(**{"iddoc":1,
                "nomdoc":"resolucion 20 del 2020",
                "feccarguedoc":today.strftime("%d/%m/%Y"),
                "fecvencimientodoc":"12/12/2023",
                "pathdoc":"/uploadfiles/resolucion_20.pdf",
                "idusuario":1}),
    2: DocInDB(**{"iddoc":2,
                "nomdoc":"resolucion 21 del 2020",
                "feccarguedoc":today.strftime("%d/%m/%Y"),
                "fecvencimientodoc":"31/12/2021",
                "pathdoc":"/uploadfiles/resolucion_21.pdf",
                "idusuario":1}),
}

@app.get("/listfiles")
async def files():
    return {"info": database_docs}

@app.post("/upload-file/")
async def create_upload_file(iddoc:int,fecvencimientodoc:str,
                nomdoc:str,
                idusuario:int,uploaded_file: UploadFile = File(...)):
#codigo antiguo
#   file_location = f"uploadfiles/{uploaded_file.filename}"
#   with open(file_location, "wb+") as file_object:
#       file_object.write(uploaded_file.file.read())
# fin codigo antiguo
       
#nuevo codigo
    file_to = '/' + uploaded_file.filename
#conexion con DrpBox
    dbx = dropbox.Dropbox('ZLnvyxN_O3oAAAAAAAAAAROUWKg5XPiHwDd4fH-djVUAfupDPYiVJuayBgJJWsxA')
    #dbx.files_upload(open(file_from, 'rb').read(), file_to)
    dbx.files_upload(uploaded_file.file.read(), file_to)
#fin nuevo codigo
    if iddoc in database_docs:
       raise HTTPException(status_code=406, detail="El documento ya existe!")
    else:
        database_docs[iddoc] = DocInDB(**{"iddoc" : iddoc,
                                            "nomdoc" : nomdoc,
                                            "feccarguedoc": today.strftime("%d/%m/%Y"),
                                            "fecvencimientodoc": fecvencimientodoc,
                                            "pathdoc": "/uploadfiles/" + uploaded_file.filename,
                                            "idusuario": idusuario})
    return {"info": f"Archivo '{uploaded_file.filename}' ha sido cargado en dropbox y la informacion ha sido grabada con exito"}
#   return {"info": f"Archivo '{uploaded_file.filename}' ha sido cargado en '{file_location}' y la informacion ha sido grabada con exito"}