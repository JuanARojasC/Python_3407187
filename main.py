from fastapi import FastAPI, HTTPException, status
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from modelos.facturas import Factura, FacturaCrear, FacturaEditar
from modelos.transacciones import Transaccion, TransaccionEditar, TransaccionCrear

clientes: list[Cliente] = []
facturas: list[Factura] = []
transacciones: list[Transaccion] = []

app = FastAPI()


# CLIENTES

@app.get("/clientes", response_model=list[Cliente])
async def listar_clientes():
    return clientes


@app.get("/clientes/{cliente_id}", response_model=Cliente)
async def listar_cliente(cliente_id: int):
    for i, obj_cliente in enumerate(clientes):
        if obj_cliente.id == cliente_id:
            return obj_cliente

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cliente no encontrado"
    )


@app.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = len(clientes) + 1
    clientes.append(cliente_val)
    return cliente_val


@app.patch("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(cliente_id: int, datos_cliente: ClienteEditar):
    for i, obj_cliente in enumerate(clientes):
        if obj_cliente.id == cliente_id:
            #VALIDAR CLIENTE
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = cliente_id
            clientes[i] = cliente_val
            return cliente_val

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cliente no encontrado"
    )


@app.delete("/clientes/{cliente_id}", response_model=Cliente)
async def eliminar_cliente(cliente_id: int):
    for i, obj_cliente in enumerate(clientes):
        if obj_cliente.id == cliente_id:
            cliente_eliminado = clientes.pop(i)
            return cliente_eliminado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cliente no encontrado"
    )


# FACTURAS

@app.get("/facturas", response_model=list[Factura])
async def listar_facturas():
    return facturas


@app.get("/facturas/{factura_id}", response_model=Factura)
async def obtener_factura(factura_id: int):
    for i, obj_factura in enumerate(facturas):
        if obj_factura.id == factura_id:
            return obj_factura

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Factura no encontrada"
    )


@app.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(cliente_id: int, datos_factura: FacturaCrear):
    cliente_encontrado = None

    for cliente in clientes:
        if cliente.id == cliente_id:
            cliente_encontrado = cliente

    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El cliente no existe"
        )

    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.cliente = cliente_encontrado
    factura_val.id = len(facturas) + 1

    facturas.append(factura_val)

    return factura_val


@app.put("/facturas/{factura_id}", response_model=Factura)
async def editar_factura(factura_id: int, datos_factura: FacturaEditar):
    for i, obj_factura in enumerate(facturas):
        if obj_factura.id == factura_id:
            factura_val = Factura.model_validate(datos_factura.model_dump())
            factura_val.id = factura_id
            facturas[i] = factura_val
            return factura_val

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Factura no encontrada"
    )


@app.delete("/facturas/{factura_id}", response_model=Factura)
async def eliminar_factura(factura_id: int):
    for i, obj_factura in enumerate(facturas):
        if obj_factura.id == factura_id:
            factura_eliminada = facturas.pop(i)
            return factura_eliminada

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Factura no encontrada"
    )


# TRANSACCIONES

@app.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones():
    return transacciones


@app.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def obtener_transaccion(transaccion_id: int):
    for transaccion in transacciones:
        if transaccion.id == transaccion_id:
            return transaccion

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Transacción no encontrada"
    )


@app.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionCrear
):
    factura_encontrada = None

    for factura in facturas:
        if factura.id == factura_id:
            factura_encontrada = factura

    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La factura no existe"
        )

    transaccion_val = Transaccion.model_validate(
        datos_transaccion.model_dump()
    )

    transaccion_val.factura_id = factura_id
    transaccion_val.id = len(transacciones) + 1

    factura_encontrada.transacciones.append(transaccion_val)
    transacciones.append(transaccion_val)

    return transaccion_val


@app.put("/transacciones/{transaccion_id}", response_model=Transaccion)
async def editar_transaccion(
    transaccion_id: int,
    datos_transaccion: TransaccionEditar
):
    for i, obj_transaccion in enumerate(transacciones):
        if obj_transaccion.id == transaccion_id:
            transaccion_val = Transaccion.model_validate(
                datos_transaccion.model_dump()
            )

            transaccion_val.id = transaccion_id
            transaccion_val.factura_id = obj_transaccion.factura_id

            transacciones[i] = transaccion_val

            for factura in facturas:
                if factura.id == obj_transaccion.factura_id:
                    for j, transaccion in enumerate(factura.transacciones):
                        if transaccion.id == transaccion_id:
                            factura.transacciones[j] = transaccion_val
                            break

            return transaccion_val

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Transacción no encontrada"
    )


@app.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def eliminar_transaccion(transaccion_id: int):
    for i, obj_transaccion in enumerate(transacciones):
        if obj_transaccion.id == transaccion_id:
            transaccion_eliminada = transacciones.pop(i)

            for factura in facturas:
                if factura.id == obj_transaccion.factura_id:
                    factura.transacciones = [
                        t for t in factura.transacciones
                        if t.id != transaccion_id
                    ]

            return transaccion_eliminada

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Transacción no encontrada"
    )