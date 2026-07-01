from fastapi import APIRouter, HTTPException, status
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from app.listas import clientes
from app.conexion_bd import Sesion_dependencia
from sqlmodel import select
rutas_clientes = APIRouter()

# cli entes: list[Cliente] = []
# CLIENTES

@rutas_clientes.get("/clientes", response_model=list[Cliente])
async def listar_clientes(sesion: Sesion_dependencia):
    lista_cli = sesion.exec(select(Cliente)).all()
    return lista_cli


@rutas_clientes.get("/clientes/{cliente_id}", response_model=Cliente)
async def listar_cliente(cliente_id: int, mi_sesion:Sesion_dependencia):
    cliente_bd = mi_sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cliente no encontrado"
    )
    return cliente_bd

@rutas_clientes.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear, mi_sesion:Sesion_dependencia):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    mi_sesion.add(cliente_val)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_val)
    return cliente_val


@rutas_clientes.patch("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(cliente_id: int, datos_cliente: ClienteEditar, mi_sesion: Sesion_dependencia):
    cliente_bd = mi_sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cliente no encontrado"
    )
    cliente_dict= datos_cliente.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(cliente_dict)
    mi_sesion.add(cliente_bd)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_bd)
    return cliente_bd


@rutas_clientes.delete("/clientes/{cliente_id}", response_model=Cliente)
async def eliminar_cliente(cliente_id: int, mi_sesion: Sesion_dependencia):
    cliente_bd = mi_sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cliente no encontrado"
    )
    mi_sesion.delete(cliente_bd)
    mi_sesion.commit()
    #Retornar mensaje, asi que elimina el response model
    return cliente_bd
