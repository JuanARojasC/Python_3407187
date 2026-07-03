from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
class TransaccionBase(SQLModel):
    vr_unitario: float = Field(default=0.0)
    cantidad: int = Field(default=0)

class TransaccionCrear(TransaccionBase):
    pass

class TransaccionEditar(TransaccionBase):
    pass

class Transaccion(TransaccionBase, table=True):
    id : int  | None = Field(default=None, primary_key=True)
    factura_id: int | None = Field(default=None, foreign_key="factura.id")
    #RELACION VIRTUAL CON MODELO FACTURA
    factura: list["Factura"] = Relationship(back_populates="transacciones")

class TransaccionLeer(TransaccionBase):
    id: int
    