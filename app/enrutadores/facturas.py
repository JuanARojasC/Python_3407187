from fastapi import APIRouter, HTTPException, status
from app.modelos.clientes import Cliente
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar, FacturaLeer, FacturaLeerCompuesta
from app.conexion_bd import Sesion_dependencia
from sqlmodel import select

rutas_facturas = APIRouter()


@rutas_facturas.get("/facturas", response_model=list[FacturaLeerCompuesta])
async def listar_facturas(sesion: Sesion_dependencia):
    return sesion.exec(select(Factura)).all()


@rutas_facturas.get("/facturas/{factura_id}", response_model=FacturaLeerCompuesta)
async def obtener_factura(factura_id: int, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, factura_id)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    return factura


@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, datos_factura: FacturaCrear, sesion: Sesion_dependencia):
    cliente_encontrado = sesion.get(Cliente, cliente_id)
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El cliente no existe"
        )
    factura_dict = datos_factura.model_dump()
    factura_dict["cliente_id"] = cliente_id
    factura_val = Factura.model_validate(factura_dict)
    sesion.add(factura_val)
    sesion.commit()
    sesion.refresh(factura_val)
    return factura_val


@rutas_facturas.put("/facturas/{factura_id}", response_model=Factura)
async def editar_factura(factura_id: int, datos_factura: FacturaEditar, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, factura_id)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    factura_data = datos_factura.model_dump(exclude_unset=True)
    factura.sqlmodel_update(factura_data)
    sesion.add(factura)
    sesion.commit()
    sesion.refresh(factura)
    return factura


@rutas_facturas.delete("/facturas/{factura_id}", response_model=Factura)
async def eliminar_factura(factura_id: int, sesion: Sesion_dependencia):
    factura = sesion.get(Factura, factura_id)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    sesion.delete(factura)
    sesion.commit()
    return factura