from .modelos.clientes import Cliente
from .modelos.facturas import Factura
from .modelos.transacciones import Transaccion

facturas: list[Factura] = []
transacciones: list[Transaccion] = []
clientes: list[Cliente] = []