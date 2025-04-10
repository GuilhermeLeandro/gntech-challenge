from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional # Para campos opcionais

# Schema base com campos comuns
class WeatherDataBase(BaseModel):
    city: str = Field(..., example="Florianopolis")
    temperature: float = Field(..., example=25.5)
    description: Optional[str] = Field(None, example="céu limpo")
    humidity: Optional[int] = Field(None, example=70)
    feels_like: Optional[float] = Field(None, example=26.1)
    wind_speed: Optional[float] = Field(None, example=3.5)
    data_timestamp: Optional[datetime] = Field(None, example="2023-10-27T10:00:00Z")

# Schema para criar dados (pode ser igual ao Base ou ter validações extras)
class WeatherDataCreate(WeatherDataBase):
    pass # Herda todos os campos de WeatherDataBase

# Schema para ler dados da API (inclui campos gerados pelo DB como id e fetched_at)
class WeatherData(WeatherDataBase):
    id: int
    fetched_at: datetime

    # Habilita o modo ORM para que o Pydantic possa ler dados
    # diretamente de objetos SQLAlchemy
    class Config:
        from_attributes = True # Anteriormente orm_mode = True