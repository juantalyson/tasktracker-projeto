# 003. Imagem `python:3.11-slim` e ordem das camadas

**Data:** 19/10/2026 · **Status:** aceita

## Contexto
A Fase 3 pede uma imagem **leve e autossuficiente**, que rode igual em qualquer máquina.

## Decisão
- Base `python:3.11-slim`: imagem oficial do Python, só com o necessário.
- Copiar o `requirements.txt` e rodar o `pip install` **antes** de copiar o código.
- `.dockerignore` tira da imagem `.venv`, `tests`, `docs`, `dados` e `*.db`.
- `CMD ["python", "src/main.py"]`: o container abre o menu do terminal por padrão.

## Consequências
- ✅ A imagem final tem cerca de 210 MB.
- ✅ Quando só o código muda, o Docker reaproveita a camada do `pip install` (cache), e o build fica rápido.
- ✅ A imagem não carrega banco nem arquivos pessoais.
- ⚠️ Os testes não ficam dentro da imagem. Para rodá-los no container, é preciso montar a pasta `tests/`.
