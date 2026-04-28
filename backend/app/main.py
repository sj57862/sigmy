from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.auth import AUTHroute

app = FastAPI()

# 1. Zdefiniuj listę dozwolonych adresów (originów)
origins = [
    "http://localhost:4200",  # Adres Twojego Angulara podczas deweloperki
    "http://127.0.0.1:4200",
]

# 2. Dodaj middleware do aplikacji
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Pozwól na te konkretne adresy
    allow_credentials=True,           # Pozwól na przesyłanie ciasteczek/autoryzacji
    allow_methods=["*"],              # Pozwól na wszystkie metody (GET, POST, PUT, itp.)
    allow_headers=["*"],              # Pozwól na wszystkie nagłówki
)

@app.get("/")
def root():
    return {"detail":"connected"}

app.include_router(AUTHroute)