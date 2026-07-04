from fastapi import APIRouter, HTTPException, status
from app.modelos.facturas import Factura
from app.modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
from app.conexion_bd import Sesion_dependencia
from sqlmodel import select

rutas_transacciones = APIRouter()


@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones(sesion: Sesion_dependencia):
    return sesion.exec(select(Transaccion)).all()


@rutas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def obtener_transaccion(transaccion_id: int, sesion: Sesion_dependencia):
    transaccion = sesion.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaccion no encontrada"
        )
    return transaccion


@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionCrear, sesion: Sesion_dependencia):
    factura_encontrada = sesion.get(Factura, factura_id)
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La factura no existe"
        )
    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id
    transaccion_val = Transaccion.model_validate(transaccion_dict)
    sesion.add(transaccion_val)
    sesion.commit()
    sesion.refresh(transaccion_val)
    return transaccion_val


@rutas_transacciones.put("/transacciones/{transaccion_id}", response_model=Transaccion)
async def editar_transaccion(transaccion_id: int, datos_transaccion: TransaccionEditar, sesion: Sesion_dependencia):
    transaccion = sesion.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaccion no encontrada"
        )
    transaccion_data = datos_transaccion.model_dump(exclude_unset=True)
    transaccion.sqlmodel_update(transaccion_data)
    sesion.add(transaccion)
    sesion.commit()
    sesion.refresh(transaccion)
    return transaccion


@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def eliminar_transaccion(transaccion_id: int, sesion: Sesion_dependencia):
    transaccion = sesion.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaccion no encontrada"
        )
    sesion.delete(transaccion)
    sesion.commit()
    return transaccion