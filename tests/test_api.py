import pytest
from src.abstract_api import BaseAPI


def test_base_api_cannot_be_instantiated():
    """Проверка, что абстрактный класс нельзя создать"""
    with pytest.raises(TypeError):
        BaseAPI()  # type: ignore