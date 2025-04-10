from fastapi import FastAPI
from .db.database import engine, Base
from .api import endpoints # Importa o router

# --- Cria as tabelas no banco de dados (se não existirem) ---
# Em produção, é melhor usar ferramentas de migração como Alembic
print("Tentando criar tabelas no banco de dados...")
try:
    Base.metadata.create_all(bind=engine)
    print("Tabelas verificadas/criadas com sucesso.")
except Exception as e:
    print(f"Erro ao criar tabelas: {e}")
    # Você pode querer tratar isso de forma mais robusta
    # dependendo se a aplicação DEVE parar se o DB não estiver acessível.

# --- Instância da Aplicação FastAPI ---
app = FastAPI(
    title="Gntech Weather API",
    description="API para buscar dados climáticos e armazená-los. Teste técnico.",
    version="0.1.0",
    # Adiciona informações de contato ou licença se desejar
    # contact={
    #     "name": "Guilherme",
    #     "email": "seu_email@example.com",
    # },
)

# --- Inclui o router dos endpoints ---
# Todas as rotas definidas em endpoints.py serão adicionadas à app
# com o prefixo /weather definido no router.
app.include_router(endpoints.router)

# --- Rota Raiz (Opcional, bom para health check) ---
@app.get("/", tags=["Root"], summary="API Root/Health Check")
async def read_root():
    """Retorna uma mensagem de boas-vindas."""
    return {"message": "Bem-vindo à API de Clima da Gntech!"}

# --- (Opcional) Eventos de startup/shutdown ---
# @app.on_event("startup")
# async def startup_event():
#     print("Aplicação iniciando...")
#     # Aqui você poderia conectar a outros serviços, se necessário

# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Aplicação encerrando...")