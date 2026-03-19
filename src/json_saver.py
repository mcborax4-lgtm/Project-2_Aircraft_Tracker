import json
import os
from typing import List, Optional

from src.abstract_saver import BaseSaver
from src.aeroplane import Aeroplane


class JSONSaver(BaseSaver):
    """
    Сохраняет и загружает данные о самолётах в JSON-файл
    """

    def __init__(self, filename: str = "data/airplanes.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создаёт файл и папку, если их нет"""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write("[]")

    def _load_data(self) -> List[dict]:
        """Загружает данные из JSON-файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                # Проверяем, что data — список
                if not isinstance(data, list):
                    return []
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, data: List[dict]) -> None:
        """Сохраняет данные в JSON-файл"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в файл"""
        data = self._load_data()
        # Проверяем, нет ли уже такого самолёта (по callsign)
        for item in data:
            if item.get("callsign") == aeroplane.callsign:
                return  # уже есть
        data.append(
            {
                "callsign": aeroplane.callsign,
                "origin_country": aeroplane.origin_country,
                "velocity": aeroplane.velocity,
                "altitude": aeroplane.altitude,
                "longitude": aeroplane.longitude,
                "latitude": aeroplane.latitude,
            }
        )
        self._save_data(data)

    def get_aeroplanes(self, country: Optional[str] = None) -> List[Aeroplane]:
        """Возвращает список самолётов, опционально фильтруя по стране"""
        data = self._load_data()
        aeroplanes = []
        for item in data:
            if country and item["origin_country"] != country:
                continue
            aeroplanes.append(
                Aeroplane(
                    callsign=item["callsign"],
                    origin_country=item["origin_country"],
                    velocity=item["velocity"],
                    altitude=item["altitude"],
                    longitude=item["longitude"],
                    latitude=item["latitude"],
                )
            )
        return aeroplanes

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт по позывному"""
        data = self._load_data()
        data = [item for item in data if item["callsign"] != aeroplane.callsign]
        self._save_data(data)

    def clear(self) -> None:
        """Очищает фай"""
        self._save_data([])
