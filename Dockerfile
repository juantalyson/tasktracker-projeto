# Imagem base leve com Python 3.11
FROM python:3.11-slim

# Pasta de trabalho dentro do container
WORKDIR /app

# Mostra os prints na hora (sem guardar em buffer)
ENV PYTHONUNBUFFERED=1
# Fuso de Brasília (sem isso o container usa UTC e "vence hoje" erra depois das 21h)
ENV TZ=America/Sao_Paulo
# Onde o banco SQLite fica (o docker-compose liga essa pasta à pasta dados/ do projeto)
ENV TASKTRACKER_DB=/app/dados/tasktracker.db

# Instala as dependências primeiro (o Docker reaproveita essa etapa se nada mudar)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY src/ /app/src/

# Porta usada pelo site (só quando o serviço web for iniciado)
EXPOSE 8000

# Por padrão, abre o menu do terminal
CMD ["python", "src/main.py"]
