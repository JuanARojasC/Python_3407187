from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

class ClienteBase(SQLModel):
    nombre: str = Field(default=None)
    descripcion: str | None = Field(default=None)

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    #RELACION VIRTUAL CON FACTURA
    factura: list["Factura"]= Relationship(back_populates="cliente"
    #BORRAR CORRECTAMENTE
    , sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class ClienteLeer(ClienteBase):
    id: int