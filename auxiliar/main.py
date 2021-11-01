#Paso 1: importa FastAPI
from fastapi import FastAPI

#Paso 2: crea un "instance" de FastAPI
app = FastAPI() 

# Para ejecutar el servidor:
# uvicorn main:app --reload
# http://127.0.0.1:8000

#Paso 3: crea un operación de path
# Métodos de HTTP
# POST:   para crear datos
# GET:    para leer datos
# PUT:    para actualizar datos
# DELETE: para borrar datos
# -----
# OPTIONS
# HEAD
# PATCH
# TRACE

# @app.post()
# @app.put()
# @app.delete()
# @app.options()
# @app.head()
# @app.patch()
# @app.trace()

#Paso 4: define la función de la operación de path
@app.get("/")  #decorador
async def root():
#Paso 5: devuelve el contenido    
    return {"message": "Hello World"}

# Repaso
#    Importa FastAPI
#    Crea un instance de app
#    Escribe un decorador de operación de path (como @app.get("/"))
#    Escribe una función de la operación de path (como def root(): ... arriba)
#    Corre el servidor de desarrollo (como uvicorn main:app --reload)

#uvicorn main:app --reload
#http://127.0.0.1:8000