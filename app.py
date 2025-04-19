import json
import os
from fastapi import FastAPI
from autotopo.main import gerar_topologia
from autotopo.grafo import montar_topologia
from fastapi.responses import HTMLResponse

app = FastAPI()

#Mostrar Topologia.png

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
        <h2>AutoTopo está no ar!</h2>
        <p>Clique abaixo para ver a topologia criada:</p>
        <a href="/teste" target="_blank">Ver topologia</a>
    """

@app.get("/teste")
def get_topologia():
    return """
        <h2>Te amo moquinha ❤️!</h2>
    """