import os
import requests
from dotenv import load_dotenv

from src.abstract_api import BaseAPI

load_dotenv()


class OpenSkyAPI(BaseAPI):
    """
    Класс для работы с OpenSky Network API
    Поддерживает авторизацию через .env (если есть) и анонимный режим (если нет)
    """

    BASE_URL = "https://opensky-network.org/api/states/all"

    def __init__(self, timeout: int = 10):
        super().__init__(timeout)  # ← вызываем родительский __init__
        self._username = os.getenv("OPEN_SKY_USERNAME")
        self._password = os.getenv("OPEN_SKY_PASSWORD")
        self._auth = (self._username, self._password) if self._username and self._password else None

        if self._auth:
            print(" OpenSky: авторизованный режим")
        else:
            print(" OpenSky: анонимный режим (10 запросов/мин)")

    def get_country_coordinates(self, country_name: str) -> dict:
        """
        Заглушка (для совместимости с BaseAPI)
        """
        raise NotImplementedError("OpenSkyAPI не поддерживает поиск координат стран")

    def get_aircraft_in_area(self, south: float, north: float, west: float, east: float) -> list:
        """
        Получает список самолётов в заданной области
        """
        params = {
            "lamin": south,
            "lamax": north,
            "lomin": west,
            "lomax": east
        }

        try:
            # Используем метод _connect из BaseAPI
            response = self._connect(self.BASE_URL, params=params, auth=self._auth)

            data = response.json()

            if not isinstance(data, dict):
                return []

            if "error" in data:
                print(f"⚠️ OpenSky API ошибка: {data['error']}")
                return []

            states = data.get("states")
            return states if isinstance(states, list) else []

        except requests.exceptions.Timeout:
            print("⏰ OpenSky таймаут")
            return []
        except Exception as e:
            print(f"⚠️ OpenSky ошибка: {e}")
            return []