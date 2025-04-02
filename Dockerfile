# Dockerfile

# 1. Usar uma imagem base oficial do Python
FROM python:3.9-slim

# 2. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copiar o arquivo de dependências primeiro (para aproveitar o cache do Docker)
COPY requirements.txt ./

# 4. Instalar as dependências Python
#    --no-cache-dir reduz o tamanho da imagem
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o restante do código da aplicação para o diretório de trabalho
COPY . .

# 6. Expor a porta que a aplicação Flask usará dentro do container
EXPOSE 5000

# 7. Definir variáveis de ambiente (padrões, podem ser sobrescritas no docker-compose.yml)
#    Não coloque senhas aqui! Use docker-compose.yml ou segredos do Docker.
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# DB_HOST será definido no docker-compose.yml para apontar para o container do DB

# 8. Comando para rodar a aplicação quando o container iniciar
#    Usamos 'flask run' ou diretamente 'python app.py'
#    Se usar 'flask run', certifique-se que FLASK_APP está definido.
#    Executar diretamente python app.py garante que o if __name__ == '__main__': seja executado.
CMD ["python", "app.py"]