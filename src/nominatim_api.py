import requests
from src.abstract_api import BaseAPI


class NominatimAPI(BaseAPI):
    """
    Класс для работы с Nominatim API (получение координат страны)
    """

    BASE_URL = "https://nominatim.openstreetmap.org/search"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def get_country_coordinates(self, country_name: str) -> dict:
        """
        Получает boundingbox страны по её названию
        """
        params = {
            "q": country_name,
            "format": "json",
            "limit": 1
        }

        response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()
        if not data:
            raise ValueError(f"Страна '{country_name}' не найдена")

        box = data[0]["boundingbox"]
        return {
            "south": float(box[0]),
            "north": float(box[1]),
            "west": float(box[2]),
            "east": float(box[3])
        }

    def get_aircraft_in_area(self, south: float, north: float, west: float, east: float) -> list:
        """
        Заглушка (для совместимости с BaseAPI).
        """
        raise NotImplementedError("NominatimAPI не поддерживает поиск самолётов")