import requests
from src.abstract_api import BaseAPI


class OpenSkyAPI(BaseAPI):
    """
    Класс для работы с OpenSky Network API
    """

    BASE_URL = "https://opensky-network.org/api/states/all"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def get_country_coordinates(self, country_name: str) -> dict:
        """
        Заглушка (для совместимости с BaseAPI).
        """
        raise NotImplementedError("OpenSkyAPI не поддерживает поиск координат стран")

    def get_aircraft_in_area(self, south: float, north: float, west: float, east: float) -> list:
        """
        Получает список самолётов в заданной прямоугольной области
        """
        params = {
            "lamin": south,
            "lamax": north,
            "lomin": west,
            "lomax": east
        }

        response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()
        return data.get("states", [])