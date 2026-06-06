from fastapi import FastAPI
from modelos.clientes import Cliente, ClienteAU
from modelos.facturas import Factura
from modelos.transacciones import Transaccion

app = FastAPI()

clientes = []
facturas = []
transacciones = []

@app.get("/clientes")
def listar_clientes():
    return clientes

@app.get("/cliente/{id}")
def obtener_cliente(id: int):
    for cliente in clientes:
        if cliente.id == id:
            return cliente
    return {"mensaje": "Cliente no encontrado"}

@app.post("/crear_cliente", response_model=Cliente)
def crear_cliente(datos_cliente: ClienteAU):

    nuevo_cliente = Cliente(
        id=len(clientes) + 1,
        nombre=datos_cliente.nombre,
        descripcion=datos_cliente.descripcion
    )
    clientes.append(nuevo_cliente)
    return nuevo_cliente

@app.put("/editar_cliente/{id}", response_model=Cliente)
def editar_cliente(id: int, datos_actualizados: Cliente):

    for i, cliente in enumerate(clientes):
        if cliente.id == id:
            cliente_editado = Cliente(
                id=id,
                nombre=datos_actualizados.nombre,
                descripcion=datos_actualizados.descripcion
            )
            clientes[i] = cliente_editado
            return cliente_editado
    return {"mensaje": "Cliente no encontrado"}

@app.delete("/eliminar_cliente/{id}")
def eliminar_cliente(id: int):

    for i, cliente in enumerate(clientes):
        if cliente.id == id:
            clientes.pop(i)
            return {"mensaje": "Cliente eliminado"}
    return {"mensaje": "Cliente no encontrado"}

@app.get("/facturas")
def listar_facturas():
    return facturas

@app.get("/factura/{id}")
def obtener_factura(id: int):

    for factura in facturas:
        if factura.id == id:
            return factura
    return {"mensaje": "Factura no encontrada"}

@app.post("/crear_factura", response_model=Factura)
def crear_factura(datos_factura: Factura):

    facturas.append(datos_factura)
    return datos_factura

@app.put("/editar_factura/{id}", response_model=Factura)
def editar_factura(id: int, datos_actualizados: Factura):

    for i, factura in enumerate(facturas):
        if factura.id == id:
            facturas[i] = datos_actualizados
            return datos_actualizados
    return {"mensaje": "Factura no encontrada"}

@app.delete("/eliminar_factura/{id}")
def eliminar_factura(id: int):

    for i, factura in enumerate(facturas):
        if factura.id == id:
            facturas.pop(i)
            return {"mensaje": "Factura eliminada"}

    return {"mensaje": "Factura no encontrada"}

@app.get("/transacciones")
def listar_transacciones():
    return transacciones

@app.get("/transaccion/{id}")
def obtener_transaccion(id: int):

    for transaccion in transacciones:
        if transaccion.id == id:
            return transaccion
    return {"mensaje": "Transacción no encontrada"}

@app.post("/crear_transaccion", response_model=Transaccion)
def crear_transaccion(datos_transaccion: Transaccion):
    transacciones.append(datos_transaccion)
    return datos_transaccion

@app.put("/editar_transaccion/{id}", response_model=Transaccion)
def editar_transaccion(id: int, datos_actualizados: Transaccion):

    for i, transaccion in enumerate(transacciones):
        if transaccion.id == id:
            transacciones[i] = datos_actualizados
            return datos_actualizados
    return {"mensaje": "Transacción no encontrada"}
@app.delete("/eliminar_transaccion/{id}")
def eliminar_transaccion(id: int):

    for i, transaccion in enumerate(transacciones):
        if transaccion.id == id:
            transacciones.pop(i)
            return {"mensaje": "Transacción eliminada"}

    return {"mensaje": "Transacción no encontrada"}