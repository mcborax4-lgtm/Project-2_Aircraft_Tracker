"""
Главный модуль программы для работы с API самолётов
"""

import sys
from typing import List

from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver
from src.nominatim_api import NominatimAPI
from src.opensky_api import OpenSkyAPI


def get_country_coordinates(country_name: str) -> dict:
    """
    Получает координаты страны через Nominatim API
    """
    api = NominatimAPI()
    try:
        coords = api.get_country_coordinates(country_name)
        print(f"✅ Координаты {country_name}: {coords}")
        return coords
    except Exception as e:
        print(f"❌ Ошибка получения координат: {e}")
        sys.exit(1)


def get_aircraft_in_area(coords: dict) -> List[Aeroplane]:
    """
    Получает и фильтрует самолёты в заданной области
    """
    api = OpenSkyAPI()
    try:
        states = api.get_aircraft_in_area(
            south=coords["south"],
            north=coords["north"],
            west=coords["west"],
            east=coords["east"]
        )

        # Если states не список или None — выходим
        if not isinstance(states, list):
            print(f"⚠️ OpenSky вернул не список: {type(states)}")
            return []

        print(f"✅ Сырых данных: {len(states)}")

        # Создаём объекты самолётов с обработкой ошибок
        aircraft = []
        for state in states:
            try:
                plane = Aeroplane.from_opensky_state(state)
                aircraft.append(plane)
            except (ValueError, TypeError) as e:
                # Пропускаем самолёты с некорректными данными
                continue

        # Фильтруем только летящие
        flying = [
            a for a in aircraft
            if a.velocity > 10.0 and a.altitude > 100.0
        ]

        print(f"📊 После фильтрации: {len(flying)} летящих самолётов")

        return flying

    except requests.exceptions.Timeout:
        print("⏰ Таймаут при запросе к OpenSky (слишком много данных)")
        return []
    except Exception as e:
        print(f"❌ Ошибка получения самолётов: {e}")
        return []


def filter_by_country(aircraft: List[Aeroplane], country: str) -> List[Aeroplane]:
    """Фильтрует самолёты по стране регистрации"""
    return [a for a in aircraft if country.lower() in a.origin_country.lower()]


def get_top_n_by_altitude(aircraft: List[Aeroplane], n: int) -> List[Aeroplane]:
    """Возвращает топ N самолётов по высоте"""
    return sorted(aircraft, reverse=True)[:n]


def print_aeroplanes(aircraft: List[Aeroplane]) -> None:
    """Красиво выводит список самолётов"""
    if not aircraft:
        print("😴 Нет самолётов для отображения")
        return

    print("\n" + "=" * 80)
    print(f"{'Позывной':<10} {'Страна':<15} {'Скорость':>10} {'Высота':>10} {'Координаты':>25}")
    print("-" * 80)
    for a in aircraft:
        coords = f"({a.latitude:.2f}, {a.longitude:.2f})" if a.latitude and a.longitude else "N/A"
        print(f"{a.callsign:<10} {a.origin_country:<15} {a.velocity:>10.1f} {a.altitude:>10.1f} {coords:>25}")
    print("=" * 80 + "\n")


def user_interaction() -> None:
    """
    Основная функция взаимодействия с пользователем
    """
    print("✈️  Добро пожаловать в программу отслеживания самолётов!")
    print("-" * 50)

    # Шаг 1: ввод страны
    country = input("Введите название страны (например, Spain): ").strip()
    if not country:
        print("❌ Название страны не может быть пустым")
        return

    # Получаем координаты
    coords = get_country_coordinates(country)

    # Получаем самолёты
    all_aircraft = get_aircraft_in_area(coords)

    if not all_aircraft:
        print("😴 В воздушном пространстве нет самолётов")
        return

    # Сохраняем в JSON
    saver = JSONSaver()
    for plane in all_aircraft:
        saver.add_aeroplane(plane)
    print("💾 Данные сохранены в файл")

    # Шаг 2: топ N по высоте
    try:
        top_n = int(input("Введите количество самолётов для вывода в топ (например, 5): "))
        top_aircraft = get_top_n_by_altitude(all_aircraft, top_n)
        print(f"\n🏆 Топ-{top_n} самолётов по высоте:")
        print_aeroplanes(top_aircraft)
    except Exception as e:
        print(f"❌ Ошибка при обработке топа: {e}")
        import traceback

        traceback.print_exc()

    # Шаг 3: фильтр по стране регистрации
    filter_country = input("Введите страну для фильтрации (или оставьте пустым): ").strip()
    if filter_country:
        filtered = filter_by_country(all_aircraft, filter_country)
        print(f"\n🎯 Самолёты, зарегистрированные в '{filter_country}':")
        print_aeroplanes(filtered)

    print("👋 Программа завершена")


if __name__ == "__main__":
    user_interaction()
