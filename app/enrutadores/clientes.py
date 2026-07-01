from fastapi import APIRouter, HTTPException, status
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from app.listas import clientes
rutas_clientes = APIRouter()

# clientes: list[Cliente] = []
# CLIENTES

@rutas_clientes.get("/clientes", response_model=list[Cliente])
async def listar_clientes():
    return clientes


@rutas_clientes.get("/clientes/{cliente_id}", response_model=Cliente)
async def listar_cliente(cliente_id: int):
    for i, obj_cliente in enumerate(clientes):
        if obj_cliente.id == cliente_id:
            return obj_cliente

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cliente no encontrado"
    )


@rutas_clientes.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = len(clientes) + 1
    clientes.append(cliente_val)
    return cliente_val


@rutas_clientes.patch("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(cliente_id: int, datos_cliente: ClienteEditar):
    for i, obj_cliente in enumerate(clientes):
        if obj_cliente.id == cliente_id:
            #VALIDAR CLIENTE
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = cliente_id
            clientes[i] = cliente_val
            return cliente_val

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cliente no encontrado"
    )


@rutas_clientes.delete("/clientes/{cliente_id}", response_model=Cliente)
async def eliminar_cliente(cliente_id: int):
    for i, obj_cliente in enumerate(clientes):
        if obj_cliente.id == cliente_id:
            cliente_eliminado = clientes.pop(i)
            return cliente_eliminado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cliente no encontrado"
    )
