from pydantic import BaseModel
from pydantic import computed_field
from .transacciones import Transaccion
from .clientes import Cliente
from datetime import datetime
class FacturaBase(BaseModel):
    fecha: datetime = datetime.now()
    cliente: Cliente
    transacciones: list[Transaccion] = []
    @computed_field
    @property
    def vr_total(self) ->float:
        #Calcular (cantidad * vr_unitario)
        #Consulta el ID_Actual
        factura_id_actual= getattr(self,"id", None)
        total_factura=0.0
        if not factura_id_actual or not self.transacciones:
            return total_factura
        #RECORRER TRANSACCIONES SEGUN FACTURA ID
        for transaccion in self.transacciones:
            if transaccion.factura_id == factura_id_actual:
                total_factura +=transaccion.vr_unitario * transaccion.cantidad
        return total_factura

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(FacturaBase):
    pass

class Factura(FacturaBase):
    id:int | None = None
