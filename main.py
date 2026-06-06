from fastapi import FastAPI

from modelos.clientes import Cliente, ClienteCrear
from modelos.facturas import Factura
from modelos.transacciones import Transaccion

clientes = []
facturas = []
transacciones = []

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
def crear_cliente(datos_cliente: ClienteCrear):
    cliente = Cliente.model_validate(datos_cliente.model_dump())
    cliente.id = len(clientes) + 1
    clientes.append(cliente)
    return {
        "mensaje": "Cliente creado",
        "cliente": cliente
    }

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

@app.get("/facturas")
def listar_facturas():
    return {"facturas": facturas}

@app.get("/factura/{id}")
def obtener_factura(id: int):
    for factura in facturas:
        if factura.id == id:
            return {"factura": factura}
    return {"mensaje": "Factura no encontrada"}

@app.post("/crear_factura")
def crear_factura(datos_factura: Factura):
    facturas.append(datos_factura)
    return {"mensaje": "Factura creada"}

@app.put("/editar_factura/{id}")
def editar_factura(id: int, datos_actualizados: Factura):
    for i, factura in enumerate(facturas):
        if factura.id == id:
            facturas[i] = datos_actualizados
            return {"mensaje": "Factura editada"}
    return {"mensaje": "Factura no encontrada"}

@app.delete("/eliminar_factura/{id}")
def eliminar_factura(id: int):
    for index, factura in enumerate(facturas):
        if factura.id == id:
            facturas.pop(index)
            return {"mensaje": "Factura eliminada"}
    return {"mensaje": "Factura no encontrada"}

@app.get("/transacciones")
def listar_transacciones():
    return {"transacciones": transacciones}

@app.get("/transaccion/{id}")
def obtener_transaccion(id: int):
    for transaccion in transacciones:
        if transaccion.id == id:
            return {"transaccion": transaccion}
    return {"mensaje": "Transacción no encontrada"}

@app.post("/crear_transaccion")
def crear_transaccion(datos_transaccion: Transaccion):
    transacciones.append(datos_transaccion)
    return {"mensaje": "Transacción creada"}

@app.put("/editar_transaccion/{id}")
def editar_transaccion(id: int, datos_actualizados: Transaccion):
    for i, transaccion in enumerate(transacciones):
        if transaccion.id == id:
            transacciones[i] = datos_actualizados
            return {"mensaje": "Transacción editada"}
    return {"mensaje": "Transacción no encontrada"}

@app.delete("/eliminar_transaccion/{id}")
def eliminar_transaccion(id: int):
    for index, transaccion in enumerate(transacciones):
        if transaccion.id == id:
            transacciones.pop(index)
            return {"mensaje": "Transacción eliminada"}
    return {"mensaje": "Transacción no encontrada"}
