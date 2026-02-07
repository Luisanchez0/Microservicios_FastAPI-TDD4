from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.api import user_routes
from core.config import user_settings

app = FastAPI(
    title=user_settings.APP_NAME,
    description="API CRUD de usuarios",
    version=user_settings.APP_VERSION,
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

app.include_router(user_routes.router)


@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "Microservicio de Usuarios",
        "status": "running",
        "version": user_settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "users"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "users_main:app",
        host="0.0.0.0",
        port=user_settings.SERVICE_PORT,
        reload=True,
    )
