import requests
from typing import Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime, timezone # Import timezone
from ..config import settings
from ..db import models, schemas
from fastapi import HTTPException # Para retornar erros HTTP

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data_from_api(city: str) -> Optional[dict]:
    """Busca dados climáticos da API OpenWeatherMap."""
    params = {
        'q': city,
        'appid': settings.OPENWEATHER_API_KEY,
        'units': 'metric', # Para obter temperatura em Celsius
        'lang': 'pt_br'   # Para obter descrição em português
    }
    try:
        response = requests.get(OPENWEATHER_URL, params=params, timeout=10) # Adiciona timeout
        response.raise_for_status() # Lança exceção para erros HTTP (4xx ou 5xx)
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Erro: Timeout ao buscar dados para {city}")
        raise HTTPException(status_code=408, detail=f"Timeout ao buscar dados para {city}")
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ao buscar dados para {city}: {http_err} - {response.status_code} - {response.text}")
        if response.status_code == 401:
             raise HTTPException(status_code=401, detail="Chave de API inválida ou não autorizada.")
        if response.status_code == 404:
             raise HTTPException(status_code=404, detail=f"Cidade '{city}' não encontrada.")
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Erro na API externa: {response.text}")
    except requests.exceptions.RequestException as req_err:
         print(f"Erro de requisição ao buscar dados para {city}: {req_err}")
         raise HTTPException(status_code=503, detail=f"Erro ao conectar com a API externa: {req_err}")
    except Exception as e:
        print(f"Erro inesperado ao buscar dados para {city}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado no servidor ao buscar dados: {e}")


def parse_weather_data(api_data: dict, city_name: str) -> schemas.WeatherDataCreate:
    """Converte a resposta da API para o schema Pydantic."""
    try:
        # Converte o timestamp UNIX (dt) para datetime UTC
        data_dt = datetime.fromtimestamp(api_data.get('dt', 0), tz=timezone.utc) if api_data.get('dt') else None

        weather_info = schemas.WeatherDataCreate(
            city=city_name, # Usa o nome da cidade fornecido, pois a API pode retornar variações
            temperature=api_data.get('main', {}).get('temp'),
            feels_like=api_data.get('main', {}).get('feels_like'),
            description=api_data.get('weather', [{}])[0].get('description'),
            humidity=api_data.get('main', {}).get('humidity'),
            wind_speed=api_data.get('wind', {}).get('speed'),
            data_timestamp=data_dt # Adiciona o timestamp da coleta
            # Adicione outros campos se necessário (ex: pressure, icon)
        )
        return weather_info
    except KeyError as e:
         print(f"Erro ao parsear dados da API: chave ausente {e}")
         raise HTTPException(status_code=500, detail=f"Formato inesperado da resposta da API: chave ausente {e}")
    except Exception as e:
        print(f"Erro inesperado ao parsear dados da API: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao processar resposta da API: {e}")


def save_weather_data(db: Session, weather_schema: schemas.WeatherDataCreate) -> models.WeatherData:
    """Salva os dados climáticos no banco de dados."""
    db_weather = models.WeatherData(**weather_schema.model_dump()) # Desempacota o schema
    db.add(db_weather)
    try:
        db.commit()
        db.refresh(db_weather) # Atualiza o objeto com dados do DB (como ID e fetched_at)
        return db_weather
    except Exception as e:
        db.rollback() # Desfaz a transação em caso de erro
        print(f"Erro ao salvar no banco de dados: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar dados no banco: {e}")

def get_weather_from_db(db: Session, city: Optional[str] = None) -> list[models.WeatherData]:
    """Busca dados climáticos armazenados no banco, opcionalmente filtrando por cidade."""
    query = db.query(models.WeatherData)
    if city:
        # Faz a comparação case-insensitive
        query = query.filter(models.WeatherData.city.ilike(f"%{city}%"))
    # Ordena pelos mais recentes primeiro (pelo timestamp de inserção)
    return query.order_by(models.WeatherData.fetched_at.desc()).all()

def get_latest_weather_from_db(db: Session, city: str) -> Optional[models.WeatherData]:
    """Busca o registro mais recente para uma cidade específica."""
    return db.query(models.WeatherData)\
             .filter(models.WeatherData.city.ilike(city))\
             .order_by(models.WeatherData.fetched_at.desc())\
             .first()