from abc import ABC, abstractmethod
from typing import List, Optional

from src.aeroplane import Aeroplane


class BaseSaver(ABC):
    """
    Абстрактный базовый класс для сохранения и загрузки данных о самолётах
    """

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет информацию о самолёте в хранилище"""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: Optional[str] = None) -> List[Aeroplane]:
        """
        Возвращает список самолётов из хранилища
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет информацию о самолёте из хранилища"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очищает всё хранилище"""
        pass
