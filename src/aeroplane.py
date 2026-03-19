from typing import Optional


class Aeroplane:
    """
    Класс, представляющий самолёт
    """

    def __init__(
            self,
            callsign: Optional[str],
            origin_country: str,
            velocity: Optional[float],
            altitude: Optional[float],
            longitude: Optional[float] = None,
            latitude: Optional[float] = None,
    ):
        self.callsign = callsign.strip() if callsign else "N/A"
        self.origin_country = origin_country

        if velocity is not None and velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")
        self.velocity = float(velocity) if velocity is not None else 0.0

        if altitude is not None and altitude < 0:
            raise ValueError("Высота не может быть отрицательной")
        self.altitude = float(altitude) if altitude is not None else 0.0

        self.longitude = float(longitude) if longitude is not None else 0.0
        self.latitude = float(latitude) if latitude is not None else 0.0

    def __lt__(self, other: "Aeroplane") -> bool:
        return self.altitude < other.altitude

    def __le__(self, other: "Aeroplane") -> bool:
        return self.altitude <= other.altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        return self.altitude > other.altitude

    def __ge__(self, other: "Aeroplane") -> bool:
        return self.altitude >= other.altitude

    def __eq__(self, other: "Aeroplane") -> bool:
        return self.altitude == other.altitude

    def __repr__(self) -> str:
        return (
            f"Aeroplane(callsign={self.callsign}, "
            f"country={self.origin_country}, "
            f"altitude={self.altitude:.1f} м, "
            f"velocity={self.velocity:.1f} м/с)"
        )

    @classmethod
    def from_opensky_state(cls, state: list) -> "Aeroplane":
        """
        Создаёт объект самолёта из сырых данных OpenSky API
        """
        return cls(
            callsign=state[1] if len(state) > 1 else None,
            origin_country=state[2] if len(state) > 2 else "Unknown",
            velocity=state[9] if len(state) > 9 else None,
            altitude=state[7] if len(state) > 7 else None,
            longitude=state[5] if len(state) > 5 else None,
            latitude=state[6] if len(state) > 6 else None,
        )
