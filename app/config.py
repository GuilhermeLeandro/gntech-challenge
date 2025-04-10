from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    DATABASE_URL: str

    # Carrega variáveis do arquivo .env
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()