from fastapi import FastAPI
from User.routers import router as user_router
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Incluir as rotas relacionadas ao usuário
app.include_router(user_router, prefix="/user", tags=["users"])


@app.get("/openapi.json")
async def get_open_api_endpoint():
    return JSONResponse(get_openapi(title="Your Project Name", version="1.0", routes=app.routes))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitações de todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)