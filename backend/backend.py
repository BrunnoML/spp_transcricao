from fastapi import FastAPI, Form, File, UploadFile, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import whisper
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# Configuracao de CORS para permitir chamadas do frontend
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"], #permite qualquer origem com o *, para restringir digitar o ip
	allow_credentials=True,
	allow_methods=["*"], #permite todos os metodos (POST, GET, etc.)
	allow_headers=["*"], #permite todos os cabecalhos
)







security = HTTPBasic()

# Usuário e senha fixos
USER_CREDENTIALS = {"bml": "pcpe"}

# Carregar apenas os modelos base e small
print("🔹 Baixando e carregando modelo 'base' e 'small' ... (isso pode demorar na primeira vez)")
MODELS = {
    "base": whisper.load_model("base"),
    #"small": whisper.load_model("small") 
}
print("✅ Modelos carregados com sucesso!")

# Função para autenticação
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username not in USER_CREDENTIALS or USER_CREDENTIALS[credentials.username] != credentials.password:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return credentials.username

# Rota de login (simplesmente valida credenciais)
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        return {"message": "Login bem-sucedido"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

# Rota para transcrição
@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...), 
    model_size: str = Form("base"),
    username: str = Depends(authenticate_user)):

    # Carregar o modelo selecionado pelo usuário
    if model_size not in MODELS:
        raise HTTPException(status_code=400, detail="Modelo inválido. Escolha entre: base, small")

    model = MODELS[model_size]  

    # Salvar o áudio temporariamente
    temp_filename = f"temp_{file.filename}"
    
    with open(temp_filename, "wb") as temp_file:
        temp_file.write(file.file.read())

    # Iniciar medição do tempo
    start_time = time.time()

    # Transcrever o áudio
    result = model.transcribe(temp_filename)

    # Remover arquivo temporário
    os.remove(temp_filename)

    # Calcular tempo de processamento
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)  

    return {"transcription": result["text"],
    "processing_time": elapsed_time  # Enviar tempo para o frontend
    }

@app.get("/")
def home():
    return {"message": "API rodando no Google Cloud Run"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Obtém a porta do ambiente ou usa 8080 por padrão
    uvicorn.run(app, host="0.0.0.0", port=port)
