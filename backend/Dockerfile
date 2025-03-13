# Usa a imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos do backend para o container
COPY backend.py requirements.txt /app/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Instala o FFmpeg antes das dependências do Python
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*


# Define a variável de ambiente para a porta
ENV PORT=8080

# Expõe a porta 8080
EXPOSE 8080

# Comando para rodar a aplicação
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8080"]