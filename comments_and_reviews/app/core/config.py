from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "27017"
    DB_USER: str = "mongo"
    DB_PASSWORD: str = "12345"
    DB_NAME: str = "comments"

    @property
    def DB_URL(self) -> str:
        auth = f"{self.DB_USER}:{self.DB_PASSWORD}"
        connection = f"{self.DB_HOST}:{self.DB_PORT}"
        db = self.DB_NAME
        return f"mongodb://{auth}@{connection}/{db}"

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

    KAFKA_HOST: str = "localhost"
    KAFKA_PORT: str = "9092"
    KAFKA_TOPIC: str = "comments"

    @property
    def KAFKA_BOOTSTRAP_SERVERS(self) -> str:
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"

    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"


settings = Settings()
