from pydantic import BaseSettings, EmailStr



class Settings(BaseSettings):

    DATABASE_URI: str
    MONGO_INITDB_DATABASE: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    ACCESS_TOKEN_EXPIRES_IN: int
    REFRESH_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str
    EMAIL_USERNAME: str



    class Config:
        env_file='./.env'

settings = Settings()
