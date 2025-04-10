# Dockerfile

# Fase 1: Imagem Base
# Usar uma imagem oficial do Python. 'slim' é menor. Python 3.9 conforme sua versão.
FROM python:3.9-slim

# Definir variáveis de ambiente úteis para Python em Docker
ENV PYTHONDONTWRITEBYTECODE 1  # Impede o Python de criar arquivos .pyc
ENV PYTHONUNBUFFERED 1         # Garante que logs (print) sejam enviados diretamente para o terminal Docker

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Opcional: Instalar dependências do sistema se psycopg2-binary falhar (raro)
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar as dependências Python
# --no-cache-dir ajuda a reduzir o tamanho da imagem final
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação (a pasta 'app') para o diretório de trabalho no container
COPY ./app /app/app

# Expor a porta que o Uvicorn usará dentro do container (a porta 8000 interna)
EXPOSE 8000

# Comando para rodar a aplicação Uvicorn quando o container iniciar
# Use "0.0.0.0" para que o servidor escute em todas as interfaces de rede dentro do container,
# permitindo que o mapeamento de portas do Docker funcione corretamente.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]