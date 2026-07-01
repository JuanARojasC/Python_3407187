from fastapi import APIRouter, HTTPException, status
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
rutas_facturas = APIRouter()
from app.conexion_bd import Sesion_dependencia
from app.listas import clientes, facturas
from sqlmodel import select
# facturas: list[Factura] = []

# FACTURAS

@rutas_facturas.get("/facturas", response_model=list[Factura])
async def listar_facturas(sesion:Sesion_dependencia ):
    #Select * from factura
    consulta = select(Factura)
    lista_facts=sesion.exec(consulta).all()
    return lista_facts 


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
async def crear_factura(cliente_id: int, datos_factura: FacturaCrear, sesion:Sesion_dependencia):
    #Buscarlo en la BD

    cliente_encontrado = sesion.get(Cliente, cliente_id)



    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El cl iente no existe"
        )
    #Validar datos factura- json, pasar a dict
    factura_dict = datos_factura.model_dump()
    factura_dict ["cliente_id"]= cliente_id
    factura_val = Factura.model_validate(factura_dict)
    factura_val.cliente = cliente_encontrado
    #Guardar en DB
    sesion.add(factura_val)
    sesion.commit()
    sesion.refresh(factura_val)

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
