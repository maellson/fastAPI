from fastapi import FastAPI
from app.routes import user_router, test_router


app = FastAPI()

# Define a rota raiz.


@app.get("/")
def health_check():
    return {"Hello": "World"}


# Registra as rotas no aplicativo.
app.include_router(user_router)
app.include_router(test_router)
