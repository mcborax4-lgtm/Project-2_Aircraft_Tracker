import pytest
from src.abstract_api import BaseAPI


def test_base_api_cannot_be_instantiated():
    """Проверка, что абстрактный класс нельзя создать"""
    with pytest.raises(TypeError):
        BaseAPI()  # type: ignore


from unittest.mock import patch, MagicMock
from src.nominatim_api import NominatimAPI


def test_nominatim_get_country_coordinates_success():
    """Тест успешного получения координат страны."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"boundingbox": ["10.0", "20.0", "30.0", "40.0"]}
    ]
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        api = NominatimAPI()
        result = api.get_country_coordinates("Spain")

        assert result == {
            "south": 10.0,
            "north": 20.0,
            "west": 30.0,
            "east": 40.0
        }
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