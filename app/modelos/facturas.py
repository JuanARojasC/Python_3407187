from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from pydantic import computed_field
from .transacciones import Transaccion
from .clientes import Cliente
from datetime import datetime
class FacturaBase(SQLModel):
    fecha: datetime = Field(default=datetime.now)
    #cliente: Cliente
    #transacciones: list[Transaccion] = []
    @computed_field
    @property
    def vr_total(self) ->float:
        #Calcular (cantidad * vr_unitario)
        #Consulta el ID_Actual
        #factura_id_actual= getattr(self,"id", None)
        #total_factura=0.0
        #if not factura_id_actual or not self.transacciones:
            #return total_factura
        #RECORRER TRANSACCIONES SEGUN FACTURA ID
        #for transaccion in self.transacciones:
            #if transaccion.factura_id == factura_id_actual:
                #total_factura +=transaccion.vr_unitario * transaccion.cantidad
        return 0.0

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    cliente_id : int = Field(default=None, foreign_key="cliente.id")