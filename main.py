from fastapi import FastAPI
from routes.userRoutes import user
from routes.prestamos import prestamo
from routes.materiales import material
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Example S.A de C.V",
    description="API de prueba para almacenar usuarios"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://front-prestamos-react.vercel.app"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(prestamo)
app.include_router(material)

@app.get ("/")
def root():
    a="a"
    b="b" + a
    return {"hello world": b}

app.include_router(user)

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 10000)) 
    uvicorn.run("main:app", host="0.0.0.0", port=port)


