from fastapi import APIRouter, HTTPException, status
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
rutas_facturas = APIRouter()
from app.listas import clientes, facturas
# facturas: list[Factura] = []

# FACTURAS

@rutas_facturas.get("/facturas", response_model=list[Factura])
async def listar_facturas():
    return facturas


@rutas_facturas.get("/facturas/{factura_id}", response_model=Factura)
async def obtener_factura(factura_id: int):
    for i, obj_factura in enumerate(facturas):
        if obj_factura.id == factura_id:
            return obj_factura

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Factura no encontrada"
    )


@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, datos_factura: FacturaCrear):
    cliente_encontrado = None

    for cliente in clientes:
        if cliente.id == cliente_id:
            cliente_encontrado = cliente

    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El cliente no existe"
        )

    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.cliente = cliente_encontrado
    factura_val.id = len(facturas) + 1

    facturas.append(factura_val)

    return factura_val


@rutas_facturas.put("/facturas/{factura_id}", response_model=Factura)
async def editar_factura(factura_id: int, datos_factura: FacturaEditar):
    for i, obj_factura in enumerate(facturas):
        if obj_factura.id == factura_id:
            factura_val = Factura.model_validate(datos_factura.model_dump())
            factura_val.id = factura_id
            facturas[i] = factura_val
            return factura_val

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Factura no encontrada"
    )


@rutas_facturas.delete("/facturas/{factura_id}", response_model=Factura)
async def eliminar_factura(factura_id: int):
    for i, obj_factura in enumerate(facturas):
        if obj_factura.id == factura_id:
            factura_eliminada = facturas.pop(i)
            return factura_eliminada

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Factura no encontrada"
    )
