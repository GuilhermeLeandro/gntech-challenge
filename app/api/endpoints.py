from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List, Optional # Import Optional
from ..db import schemas, models # Import models aqui também
from ..db.database import get_db
from ..services import weather_service # Importa o módulo de serviço

router = APIRouter(
    prefix="/weather", # Prefixo para todas as rotas neste router
    tags=["Weather Data"] # Agrupa na documentação Swagger
)

@router.post("/{city}",
             response_model=schemas.WeatherData, # Retorna o dado salvo
             status_code=status.HTTP_201_CREATED, # Status para criação bem-sucedida
             summary="Fetch weather and save to DB",
             description="Fetches current weather data for a city from OpenWeatherMap and stores it in the database.")
def fetch_and_save_weather(
    city: str = Path(..., title="City Name", description="The name of the city to fetch weather data for (e.g., London)", min_length=2),
    db: Session = Depends(get_db)
    ):
    """
    Busca os dados climáticos atuais para a cidade informada na API OpenWeatherMap,
    salva no banco de dados e retorna o registro criado.
    """
    # 1. Buscar da API Externa
    api_data = weather_service.fetch_weather_data_from_api(city)
    # A função fetch já lança HTTPException em caso de erro, então não precisamos checar None aqui

    # 2. Parsear os dados para o schema Pydantic
    weather_to_save = weather_service.parse_weather_data(api_data, city)

    # 3. Salvar no Banco de Dados
    saved_data = weather_service.save_weather_data(db, weather_schema=weather_to_save)
    return saved_data # FastAPI converterá automaticamente para o JSON usando o response_model


@router.get("/",
            response_model=List[schemas.WeatherData], # Retorna uma lista de dados
            summary="Get all stored weather data",
            description="Retrieves all weather data records stored in the database, ordered by fetch time descending.")
def get_all_weather_data(
    db: Session = Depends(get_db)
    ):
    """
    Retorna todos os registros de dados climáticos armazenados no banco.
    """
    all_data = weather_service.get_weather_from_db(db)
    return all_data

@router.get("/{city}",
            response_model=List[schemas.WeatherData], # Pode retornar múltiplos registros para a mesma cidade
            summary="Get stored weather data for a specific city",
            description="Retrieves all stored weather data records for a specific city, ordered by fetch time descending.")
def get_city_weather_data(
    city: str = Path(..., title="City Name", description="The name of the city to retrieve stored data for"),
    db: Session = Depends(get_db)
    ):
    """
    Retorna todos os registros de dados climáticos armazenados para uma cidade específica.
    """
    city_data = weather_service.get_weather_from_db(db, city=city)
    if not city_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No stored weather data found for city '{city}'"
        )
    return city_data

@router.get("/latest/{city}",
            response_model=schemas.WeatherData, # Retorna um único registro
            summary="Get the latest stored weather data for a specific city",
            description="Retrieves the most recent weather data record stored for a specific city.")
def get_latest_city_weather_data(
    city: str = Path(..., title="City Name", description="The name of the city to retrieve the latest stored data for"),
    db: Session = Depends(get_db)
):
    """
    Retorna o registro mais recente de dados climáticos armazenados para uma cidade específica.
    """
    latest_data = weather_service.get_latest_weather_from_db(db, city=city)
    if not latest_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No stored weather data found for city '{city}'"
        )
    return latest_data