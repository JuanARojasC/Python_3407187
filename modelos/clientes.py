from pydantic import BaseModel
class ClienteBase(BaseModel):
    nombre: str
    descripcion: str | None = None

class ClienteAU(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int