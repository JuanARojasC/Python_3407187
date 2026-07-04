# Sistema de Facturación — API 

API REST para la gestión de clientes, facturas y transacciones, construida con FastAPI, SQLModel y SQLite.

---

## Estructura del Proyecto

```
Python_3407187/
├── app/
│   ├── main.py
│   ├── conexion_bd.py
│   ├── listas.py
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── clientes.py
│   │   ├── facturas.py
│   │   └── transacciones.py
│   └── enrutadores/
│       ├── clientes.py
│       ├── facturas.py
│       └── transacciones.py
├── bd_clientes.sqlite3
├── requierement.txt
└── .gitignore
```

---

## Instalación y Ejecución

Clonar el repositorio:

```bash
git clone https://github.com/JuanARojasC/Python_3407187.git
cd Python_3407187
```

Crear entorno virtual:

```bash
python -m venv venv
source venv/bin/activate       
venv\Scripts\activate          
```

Instalar dependencias:

```bash
pip install -r requierement.txt
```

Ejecutar la aplicación:

```bash
uvicorn app.main:app --reload
```

Documentación interactiva (Swagger UI): http://127.0.0.1:8000/docs

---

## Comandos Git

Clonar un repositorio:

```bash
git clone https://github.com/usuario/repositorio.git
```

Ver historial de commits en una línea:

```bash
git log --oneline
```

Agregar cambios y hacer commit:

```bash
git add .
git commit -m "mensaje del commit"
```

Subir cambios al repositorio remoto:

```bash
git push origin main
```

Volver a un commit anterior sin perder los cambios actuales:

```bash
git checkout <hash-del-commit>
```

Revertir un commit creando uno nuevo que deshace sus cambios:

```bash
git revert <hash-del-commit>
```

El `<hash-del-commit>` se obtiene con `git log --oneline`.

Historial de commits de este proyecto:

```
fd9138a  RELACIONES VIRTUALES
3a00a17  Base de datos, Tablas, Relaciones y Endpoints (18)
5c84468  Enrutadores
13b63d3  Estructuracion del proyecto
f44d36d  ENDPOINTS Terminados (VIDEO10)
2405747  Main y clientes correigo
038f6d3  ID automatico (EnClase), Modelos y Requieremnt
57e2e32  Creacion de los modelos en una nueva carpeta
365aa28  GitIgnore
fb346e3  Actividad2-FacturasYTransacciones
68854e4  FASTAPI CRUD
```

---
