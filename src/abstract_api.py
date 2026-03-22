from abc import ABC, abstractmethod
import requests


class BaseAPI(ABC):
    """Абстрактный базовый класс для работы с API"""

    def __init__(self, timeout: int = 10):
        self._timeout = timeout
        self._session = requests.Session()

    def _connect(self, url: str, params: dict = None, headers: dict = None) -> requests.Response:
        """Приватный метод для выполнения запроса с проверкой статуса"""
        response = self._session.get(url, params=params, headers=headers, timeout=self._timeout)
        response.raise_for_status()
        return response

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> dict:
        pass

    @abstractmethod
    def get_aircraft_in_area(self, south: float, north: float, west: float, east: float) -> list:
        pass
