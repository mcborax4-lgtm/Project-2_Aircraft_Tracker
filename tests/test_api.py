from unittest.mock import MagicMock, patch

import pytest

from src.abstract_api import BaseAPI
from src.nominatim_api import NominatimAPI
from src.opensky_api import OpenSkyAPI


def test_base_api_cannot_be_instantiated():
    """Проверка, что абстрактный класс нельзя создать"""
    with pytest.raises(TypeError):
        BaseAPI()  # type: ignore


def test_nominatim_get_country_coordinates_success():
    """Тест успешного получения координат страны."""
    mock_response = MagicMock()
    mock_response.json.return_value = [{"boundingbox": ["10.0", "20.0", "30.0", "40.0"]}]
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        api = NominatimAPI()
        result = api.get_country_coordinates("Spain")

        assert result == {"south": 10.0, "north": 20.0, "west": 30.0, "east": 40.0}
        mock_get.assert_called_once()


def test_nominatim_get_country_coordinates_not_found():
    """Тест: страница не найдена."""
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        api = NominatimAPI()
        import pytest

        with pytest.raises(ValueError, match="Страна 'Atlantis' не найдена"):
            api.get_country_coordinates("Atlantis")


def test_opensky_get_aircraft_in_area_success():
    """Тест успешного получения списка самолётов."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "states": [["icao24", "callsign", "country", 123.0, 456.0, 10000.0, True, 250.0]]
    }
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        api = OpenSkyAPI()
        result = api.get_aircraft_in_area(10.0, 20.0, 30.0, 40.0)

        assert len(result) == 1
        assert result[0][1] == "callsign"


def test_opensky_get_aircraft_in_area_empty():
    """Тест: пустой ответ от API."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"states": []}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        api = OpenSkyAPI()
        result = api.get_aircraft_in_area(10.0, 20.0, 30.0, 40.0)

        assert result == []
