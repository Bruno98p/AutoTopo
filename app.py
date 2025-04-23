from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from run import executar_pipeline
from datetime import datetime
from fastapi.responses import JSONResponse
import shutil, os

app = FastAPI()

# Servir arquivos estáticos
app.mount("/Produtos", StaticFiles(directory="Produtos"), name="produtos")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuração de templates
templates = Jinja2Templates(directory="templates")

# Rota Home
@app.get("/", response_class=HTMLResponse)
def home(request: Request, status: str = "", tipo: str = ""):
    img_path = "Produtos/topologia.png"

    if os.path.exists(img_path):
        timestamp = datetime.now().timestamp()
        topologia_img = f"/Produtos/topologia.png?{timestamp}"
    else:
        topologia_img = None

    return templates.TemplateResponse("home.html", {
        "request": request,
        "topologia_img": topologia_img,
        "status": status,
        "tipo": tipo
    })

# Rota para gerar topologia
@app.get("/gerar")
def gerar_topologia():
    try:
        # Verificar se a pasta configs está vazia
        if not os.path.exists("configs") or not any(os.listdir("configs")):
            return RedirectResponse(url="/?status=Não%20há%20arquivos%20de%20configuração%20para%20gerar%20a%20topologia.&tipo=erro", status_code=303)

        # Se a pasta não estiver vazia, prosseguir com a execução do pipeline
        executar_pipeline()

        # Se a topologia for gerada com sucesso
        return RedirectResponse(url="/?status=Topologia%20gerada%20com%20sucesso!&tipo=sucesso", status_code=303)

    except Exception as e:
        # Em caso de erro na execução
        return RedirectResponse(url=f"/?status={str(e)}&tipo=erro", status_code=303)

# Rota para fazer upload de arquivos
@app.get("/upload", response_class=HTMLResponse)
def form_upload(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload_files(request: Request, files: list[UploadFile] = File(...)):
    try:
        for f in os.listdir("configs"):
            os.remove(os.path.join("configs", f))

        for file in files:
            file_path = os.path.join("configs", file.filename)
            file_bytes = await file.read()
            with open(file_path, "wb") as f:
                f.write(file_bytes)

        executar_pipeline()
        return RedirectResponse(url="/", status_code=303)

    except Exception as e:
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "erro": str(e)
        })


# Rota para limpar arquivos
@app.post("/limpar_arquivos")
def limpar_arquivos():
    try:
        for pasta in ["configs", "Produtos"]:
            caminho = os.path.join(os.getcwd(), pasta)
            for arquivo in os.listdir(caminho):
                caminho_arquivo = os.path.join(caminho, arquivo)
                if os.path.isfile(caminho_arquivo):
                    os.remove(caminho_arquivo)
        return JSONResponse(content={"sucesso": True, "mensagem": "Arquivos apagados com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"sucesso": False, "mensagem": f"Erro ao apagar arquivos: {e}"})

# Rota para carregar arquivos de teste
@app.post("/carregar_testes")
def carregar_testes():
    try:
        origem = os.path.join(os.getcwd(), "teste")
        destino = os.path.join(os.getcwd(), "configs")

        if not os.path.exists(origem):
            return JSONResponse(content={"sucesso": False, "mensagem": "Pasta de teste não encontrada."})

        for arquivo in os.listdir(origem):
            origem_arquivo = os.path.join(origem, arquivo)
            destino_arquivo = os.path.join(destino, arquivo)
            if os.path.isfile(origem_arquivo):
                shutil.copy(origem_arquivo, destino_arquivo)

        return JSONResponse(content={"sucesso": True, "mensagem": "Arquivos de teste carregados!"})
    except Exception as e:
        return JSONResponse(content={"sucesso": False, "mensagem": f"Erro ao copiar arquivos: {e}"})
