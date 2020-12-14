from typing import Dict
from pydantic import BaseModel,FilePath
from datetime import date

class DocInDB(BaseModel):
    iddoc: int
    nomdoc: str
    feccarguedoc: str
    fecvencimientodoc: str
    pathdoc: str
    idusuario:int