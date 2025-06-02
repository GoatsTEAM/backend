from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "12345"
    POSTGRES_DB: str = "orders"

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        auth = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
        connection = f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
        db = self.POSTGRES_DB
        return  f"postgresql+asyncpg://{auth}@{connection}/{db}"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = "12345"
    REDIS_DB: str = "0"
    
    @property
    def REDIS_URL(self) -> str:
        auth = f"{self.REDIS_USER}:{self.REDIS_PASSWORD}"
        connection = f"{self.REDIS_HOST}:{self.REDIS_PORT}"
        db = self.REDIS_DB
        return f"redis://{auth}@{connection}/{db}"


    JWT_SECRET: str = "secret_key"
    JWT_ALGORITHM: str = "HS256"


settings = Settings()