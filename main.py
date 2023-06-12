from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import Config
import app.controllers.dataProcessing  as dataProcessing
import uvicorn

app = FastAPI()
app.config = Config()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dataProcessing.router, prefix='/api')

if __name__ == '__main__':
  uvicorn.run(app)