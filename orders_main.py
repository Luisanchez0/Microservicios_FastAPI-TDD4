from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.api import order_routes
from core.config import order_settings

app = FastAPI(
    title=order_settings.APP_NAME,
    description="API CRUD de pedidos",
    version=order_settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_routes.router)


@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "Microservicio de Pedidos",
        "status": "running",
        "version": order_settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "orders"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "orders_main:app",
        host="0.0.0.0",
        port=order_settings.SERVICE_PORT,
        reload=True,
    )
