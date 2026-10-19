# Imagem base leve com Python 3.11
FROM python:3.11-slim

# Pasta de trabalho dentro do container
WORKDIR /app

# Mostra os prints na hora (sem guardar em buffer)
ENV PYTHONUNBUFFERED=1

# Copia o código da aplicação
COPY src/ /app/src/

# Comando que roda quando o container inicia
CMD ["python", "src/main.py"]
