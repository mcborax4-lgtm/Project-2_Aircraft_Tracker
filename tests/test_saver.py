import os
import tempfile

import pytest

from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver


@pytest.fixture
def temp_saver():
    """Создаёт временный JSON-файл для тестов."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp.write("[]")
        tmp_path = tmp.name
    saver = JSONSaver(tmp_path)
    yield saver
    os.unlink(tmp_path)


def test_add_and_get_aeroplane(temp_saver):
    plane = Aeroplane("TEST123", "Russia", 250.0, 5000.0)
    temp_saver.add_aeroplane(plane)

    result = temp_saver.get_aeroplanes()
    assert len(result) == 1
    assert result[0].callsign == "TEST123"
    assert result[0].origin_country == "Russia"


def test_add_duplicate(temp_saver):
    plane1 = Aeroplane("TEST123", "Russia", 250.0, 5000.0)
    plane2 = Aeroplane("TEST123", "Russia", 300.0, 6000.0)

    temp_saver.add_aeroplane(plane1)
    temp_saver.add_aeroplane(plane2)  # дубликат не добавится

    result = temp_saver.get_aeroplanes()
    assert len(result) == 1


def test_filter_by_country(temp_saver):
    plane1 = Aeroplane("RU123", "Russia", 250.0, 5000.0)
    plane2 = Aeroplane("US456", "USA", 300.0, 6000.0)

    temp_saver.add_aeroplane(plane1)
    temp_saver.add_aeroplane(plane2)

    russian = temp_saver.get_aeroplanes(country="Russia")
    assert len(russian) == 1
    assert russian[0].callsign == "RU123"


def test_delete_aeroplane(temp_saver):
    plane = Aeroplane("DEL123", "Russia", 250.0, 5000.0)
    temp_saver.add_aeroplane(plane)

    temp_saver.delete_aeroplane(plane)
    result = temp_saver.get_aeroplanes()
    assert len(result) == 0


def test_clear(temp_saver):
    plane1 = Aeroplane("A", "Russia", 250.0, 5000.0)
    plane2 = Aeroplane("B", "USA", 300.0, 6000.0)

    temp_saver.add_aeroplane(plane1)
    temp_saver.add_aeroplane(plane2)

    temp_saver.clear()
    result = temp_saver.get_aeroplanes()
    assert len(result) == 0
