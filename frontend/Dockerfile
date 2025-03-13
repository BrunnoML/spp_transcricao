# Usa a imagem oficial do Nginx como base
FROM nginx:alpine

# Define o diretório de trabalho
WORKDIR /usr/share/nginx/html

# Cria a pasta e define permissões antes de copiar
RUN mkdir -p /usr/share/nginx/html && chmod 755 /usr/share/nginx/html

# Copia os arquivos do frontend para o container
COPY index.html .

# Garante que o Nginx possa ler o arquivo corretamente
RUN chmod 644 /usr/share/nginx/html/index.html

# Expõe a porta 80
EXPOSE 80

# Inicia o Nginx
CMD ["nginx", "-g", "daemon off;"]
