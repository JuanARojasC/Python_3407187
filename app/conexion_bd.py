from fastapi import FastAPI, Depends
from sqlmodel import Session , SQLModel, create_engine
from typing import Annotated
nombre_bd="bd_clientes.sqlite3"
url_bd= f"sqlite:///{nombre_bd}"

#Motor BD
motor_bd = create_engine(url_bd)

#Definir metodo para crear las tablas 
def crear_tablas(app:FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield #No hay nada para retornar o ejecutar

#Definir metodo para la sesion
def obtener_sesion():
    with Session(motor_bd) as mi_sesion:
        yield mi_sesion #Retorna la sesion

#Denominado inyeccion de dependencias
#Registrar sesion como dependencia , utilizada en nuestros endpoint
Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]