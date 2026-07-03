from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from pydantic import computed_field
from .transacciones import Transaccion
from .clientes import Cliente, ClienteLeer
from datetime import datetime
class FacturaBase(SQLModel):
    fecha: datetime = Field(default=datetime.now)
    #cliente: Cliente 
    #transacciones: list[Transaccion] = []
    @computed_field
    @property
    def vr_total(self) -> float:
        total = 0.0

        transacciones = getattr(self, "transacciones", [])

        for t in transacciones:
            total += t.vr_unitario * t.cantidad

        return total

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    cliente_id : int = Field(default=None, foreign_key="cliente.id")
    #RELACIONES VIRTUALES con cliente= NO EN BD
    cliente: Cliente = Relationship(back_populates="factura")
    transacciones : list[Transaccion] = Relationship(back_populates="factura")
#MODELO PARA MOSTRAR USUARIO O CLIENTE
class FacturaLeer(FacturaBase):
    id:int 
    cliente: ClienteLeer

class FacturaLeerCompuesta(FacturaLeer):
    transacciones: list[Transaccion]=[]