# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.api import user_routes, order_routes

app = FastAPI(
    title="Hexagonal Architecture API",
    description="API CRUD de usuarios y pedidos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de usuarios
app.include_router(user_routes.router)

# Incluir rutas de pedidos
app.include_router(order_routes.router)

@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "API con Arquitectura Hexagonal",
        "status": "running",
        "version": "1.0.0",
        "services": ["users", "orders"],
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "services": {
            "users": "active",
            "orders": "active"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )