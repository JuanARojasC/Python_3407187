from fastapi import APIRouter, HTTPException, status
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
from app.modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
from sqlmodel import select
from app.listas import facturas, transacciones
from app.conexion_bd import Sesion_dependencia
rutas_transacciones = APIRouter()

# transacciones: list[Transaccion] = []

# TRANSACCIONES

@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones(sesion:Sesion_dependencia):
    #lista_transa=sesion.exec(consulta).all()
    #return lista_transa
    return sesion.exec(select(Transaccion)).all()

@rutas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def obtener_transaccion(transaccion_id: int):
    for transaccion in transacciones:
        if transaccion.id == transaccion_id:
            return transaccion

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Transacción no encontrada"
    )


@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionCrear, sesion: Sesion_dependencia
):
    factura_encontrada = sesion.get(Factura, factura_id)
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La factura no existe"
        )
#VALIDAR DATOS - JSON Y DICT
    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id
    transaccion_val = Transaccion.model_validate(transaccion_dict)
    #GUARDAR EN DB
    sesion.add(transaccion_val)
    sesion.commit()
    sesion.refresh(transaccion_val)
    return transaccion_val


@rutas_transacciones.put("/transacciones/{transaccion_id}", response_model=Transaccion)
async def editar_transaccion(
    transaccion_id: int,
    datos_transaccion: TransaccionEditar
):
    for i, obj_transaccion in enumerate(transacciones):
        if obj_transaccion.id == transaccion_id:
            transaccion_val = Transaccion.model_validate(
                datos_transaccion.model_dump()
            )

            transaccion_val.id = transaccion_id
            transaccion_val.factura_id = obj_transaccion.factura_id

            transacciones[i] = transaccion_val

            for factura in facturas:
                if factura.id == obj_transaccion.factura_id:
                    for j, transaccion in enumerate(factura.transacciones):
                        if transaccion.id == transaccion_id:
                            factura.transacciones[j] = transaccion_val
                            break

            return transaccion_val

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Transacción no encontrada"
    )


@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def eliminar_transaccion(transaccion_id: int):
    for i, obj_transaccion in enumerate(transacciones):
        if obj_transaccion.id == transaccion_id:
            transaccion_eliminada = transacciones.pop(i)

            for factura in facturas:
                if factura.id == obj_transaccion.factura_id:
                    factura.transacciones = [
                        t for t in factura.transacciones
                        if t.id != transaccion_id
                    ]

            return transaccion_eliminada

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Transacción no encontrada"
    )