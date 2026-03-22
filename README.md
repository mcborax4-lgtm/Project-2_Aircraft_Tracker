# Курсовая работа: Aircraft Tracker

## Описание проекта
Программа для отслеживания самолётов в воздушном пространстве различных стран.  
Использует открытые API для получения координат стран и данных о самолётах.

## Функционал
- Получение географических координат страны через Nominatim API
- Получение данных о самолётах в заданной области через OpenSky Network API
- Сохранение информации о самолётах в JSON-файл
- Вывод топа N самолётов по высоте
- Фильтрация самолётов по стране регистрации

## Структура проекта
```coursework/
├── data/                      # JSON-файлы с данными
├── src/
│   ├── __init__.py
│   ├── abstract_api.py        # Абстрактный класс для API
│   ├── nominatim_api.py       # Получение координат стран
│   ├── opensky_api.py         # Получение данных о самолётах
│   ├── aeroplane.py           # Класс самолёта
│   ├── abstract_saver.py      # Абстрактный класс для сохранения
│   ├── json_saver.py          # Сохранение в JSON
│   └── utils.py               # Вспомогательные функции
├── tests/                      # Тесты
│   ├── __init__.py
│   ├── test_aeroplane.py
│   ├── test_api.py
│   └── test_saver.py
├── main.py                     # Точка входа
├── .env.example                # Пример переменных окружения
└── README.md
```
## Установка и запуск

### 1. Клонирование репозитория
git clone <url-репозитория>
cd coursework

### 2. Создание виртуального окружения
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Linux/Mac

### 3. Установка зависимостей
`pip install requests python-dotenv pytest pytest-cov black isort flake8 mypy`

### 4. Настройка переменных окружения
Создайте файл .env на основе .env.example:

`USER_EMAIL=ваш_email@example.com`

`OPEN_SKY_USERNAME=your_username`    # опционально 

`OPEN_SKY_PASSWORD=your_password`    # опционально

### 5. Запуск программы
`python main.py`

## Использование
1. Введите название страны (например, Spain, Russia, France)
2. Программа получит координаты и найдёт все самолёты в воздушном пространстве
3. Данные сохранятся в data/airplanes.json
4. Введите количество самолётов для вывода в топ по высоте
5. При желании отфильтруйте по стране регистрации

## Тестирование
`pytest tests/ -v`

`pytest --cov=src tests/ --cov-report=term-missing`

## Форматирование и линтинг
black .
isort .
flake8 .
mypy . 

## Основные компоненты

### API классы
- BaseAPI — абстрактный базовый класс
- NominatimAPI — получение координат страны (требует User-Agent с email)
- OpenSkyAPI — получение данных о самолётах (поддержка авторизации)

### Модель данных Aeroplane
- callsign — позывной
- origin_country — страна регистрации
- velocity — скорость (м/с)
- altitude — высота (м)
- longitude, latitude — координаты
- Поддерживает сравнение по высоте (<, >, <=, >=, ==)

### Работа с файлами
- BaseSaver — абстрактный класс
- JSONSaver — сохранение/загрузка данных в JSON

## Требования к окружению
- Python 3.13+
- requests
- python-dotenv
- pytest (для тестов)
- black, isort, flake8, mypy (для разработки)

## Примечания
- OpenSky API без авторизации — 10 запросов в минуту
- С аутентификацией — 20 запросов в минуту
- Для больших стран (Россия, Франция) количество самолётов может превышать 10 000 — программа автоматически ограничивает выборку