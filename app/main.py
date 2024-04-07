from fastapi import FastAPI
from app.routes import router


app = FastAPI()

# Define a rota raiz.


@app.get("/")
def health_check():
    return {"Hello": "World"}


# Registra as rotas no aplicativo.
app.include_router(router)
