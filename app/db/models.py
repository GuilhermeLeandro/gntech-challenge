from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func # para usar funções SQL como NOW()
from .database import Base # Importa o Base do mesmo diretório (db)

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    temperature = Column(Float, nullable=False)
    feels_like = Column(Float) # Temperatura sentida
    description = Column(String)
    humidity = Column(Integer)
    wind_speed = Column(Float) # Velocidade do Vento
    # Timestamp da coleta dos dados na API
    data_timestamp = Column(DateTime(timezone=True), nullable=True)
    # Timestamp de quando o registro foi inserido no banco
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())

    # Você pode adicionar mais campos conforme a API do OpenWeather retornar
    # Ex: pressure = Column(Integer)
    # Ex: icon = Column(String)