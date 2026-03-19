from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """
    Абстрактный базовый класс для работы с API
    """

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> dict:
        """
        Получает координаты страны (boundingbox) от nominatim.
        """
        pass

    @abstractmethod
    def get_aircraft_in_area(self, south: float, north: float, west: float, east: float) -> list:
        """
        Получает список самолётов в заданной прямоугольной области от opensky
        """
        pass
