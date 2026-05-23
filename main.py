from fastapi import FastAPI
from pydantic import BaseModel

clientes = []

class Cliente(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None

app = FastAPI()

@app.get("/clientes")
def listar_clientes():
    return {"clientes": clientes}

@app.get("/cliente/{id}")
def obtener_cliente(id: int):
    for cliente in clientes:
        if cliente.id == id:
            return {"cliente": cliente}
    return {"mensaje": "Cliente no encontrado"}

@app.post("/crear_cliente")
def crear_cliente(datos_cliente: Cliente):
    clientes.append(datos_cliente)
    return {"mensaje": "Cliente creado"}

@app.put("/editar_cliente/{id}")
def editar_cliente(id: int, datos_actualizados: Cliente):
    for i, cliente in enumerate(clientes):
        if cliente.id == id:
            clientes[i] = datos_actualizados
            return {"mensaje": "Cliente editado"}
    return {"mensaje": "Cliente no encontrado"}

@app.delete("/eliminar_cliente/{id}")
def eliminar_cliente(id: int):
    for index, cliente in enumerate(clientes):
        if cliente.id == id:
            clientes.pop(index)
            return {"mensaje": "Cliente eliminado"}
    return {"mensaje": "Cliente no encontrado"}