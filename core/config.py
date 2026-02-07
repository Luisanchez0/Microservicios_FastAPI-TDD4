from pydantic_settings import BaseSettings


class UserSettings(BaseSettings):
    SERVICE_NAME: str = "users-service"
    SERVICE_PORT: int = 8001

    APP_NAME: str = "Microservicio de Usuarios"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    """
    # Base de datos (para futuro)
    DATABASE_URL: str = "sqlite:///./users.db"

    class Config:
        env_file = ".env"
    """


class OrderSettings(BaseSettings):
    SERVICE_NAME: str = "orders-service"
    SERVICE_PORT: int = 8002

    APP_NAME: str = "Microservicio de Pedidos"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True


user_settings = UserSettings()
order_settings = OrderSettings()

# Backwards compatibility
settings = user_settings
