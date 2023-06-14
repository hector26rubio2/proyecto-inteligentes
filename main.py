from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import Config
from fastapi.staticfiles import StaticFiles
import app.controllers.dataProcessingController  as dataProcessingController
import app.controllers.trainingController  as trainingController
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

app.mount("/histograms", StaticFiles(directory="./app/documents/histograms"), name="histograms")
app.mount("/correlationMatrix", StaticFiles(directory="./app/documents/correlationMatrix"), name="correlationMatrix")

app.include_router(dataProcessingController.router, prefix='/api')
app.include_router(trainingController.router, prefix='/api')

if __name__ == '__main__':
  uvicorn.run(app)