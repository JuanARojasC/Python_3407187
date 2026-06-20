from pydantic import BaseModel
class TransaccionBase(BaseModel):
    vr_unitario: float
    cantidad: int

class TransaccionCrear(TransaccionBase):
    pass

class TransaccionEditar(TransaccionBase):
    pass

class Transaccion(TransaccionBase):
    id : int  | None = None
    factura_id: int | None = None