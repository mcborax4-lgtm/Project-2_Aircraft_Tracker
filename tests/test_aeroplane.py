import pytest
from src.aeroplane import Aeroplane


def test_aeroplane_creation():
    plane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
    assert plane.callsign == "UAL1621"
    assert plane.origin_country == "United States"
    assert plane.velocity == 268.79
    assert plane.altitude == 10203.18


def test_aeroplane_invalid_velocity():
    with pytest.raises(ValueError, match="Скорость не может быть отрицательной"):
        Aeroplane("TEST", "Russia", -10.0, 1000.0)


def test_aeroplane_invalid_altitude():
    with pytest.raises(ValueError, match="Высота не может быть отрицательной"):
        Aeroplane("TEST", "Russia", 100.0, -500.0)


def test_aeroplane_comparison():
    low = Aeroplane("LOW", "A", 100.0, 1000.0)
    high = Aeroplane("HIGH", "B", 200.0, 5000.0)

    assert low < high
    assert high > low
    assert not (low > high)
    assert low <= high
    assert high >= low


def test_from_opensky_state():
    state = [
        "abc123", "UAL1621", "United States", 123456, 123456,
        10.5, 20.3, 10203.18, False, 268.79, 0.0, 0.0, None, None, None, False, 0
    ]
    plane = Aeroplane.from_opensky_state(state)

    assert plane.callsign == "UAL1621"
    assert plane.origin_country == "United States"
    assert plane.velocity == 268.79
    assert plane.altitude == 10203.18
    assert plane.longitude == 10.5
    assert plane.latitude == 20.3


def test_from_opensky_state_with_none():
    state = [
        "abc123", None, "Russia", 123456, 123456,
        None, None, None, False, None, 0.0, 0.0, None, None, None, False, 0
    ]
    plane = Aeroplane.from_opensky_state(state)

    assert plane.callsign == "N/A"
    assert plane.velocity == 0.0
    assert plane.altitude == 0.0