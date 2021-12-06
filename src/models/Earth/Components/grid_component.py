from abc import ABC
from typing import Optional, Union

from constants import TIME_DELTA
from units import *


class GridComponent(ABC):
    index: int
    volume: Volume
    mass: Mass
    ratio: float
    __energy: Energy = 0
    __neighbours: Optional[list["GridComponent"]]

    def __init__(self, volume: Volume, mass: Mass, temperature: Temperature, *, ratio=1.0, parent=None, index: int = None):
        self.volume = volume
        self.surface = Area(meters2=(volume ** (1 / 3)) ** 2)
        self.mass = mass
        self.temperature = temperature
        self.ratio = ratio
        self.parent = parent
        # Finds yourself in the list
        self.index = index if index is not None else self.parent and self.parent.index(self)
        self.__neighbours = None

    @classmethod
    def init_default(cls, *, ratio=1.0, parent=None, index: int = None):
        return cls(volume=Volume(meters3=1), mass=Mass(kilograms=1000), temperature=Temperature(celsius=21),
                   ratio=ratio, parent=parent, index=index)

    def __str__(self):
        res = f"""{self.__class__} Component
Volume : {self.volume}
Mass : {self.mass}
Temperature : {self.temperature} ({self.__energy} J)
"""
        return res

    @property
    def temperature(self) -> Temperature:
        value = Temperature(kelvin=self.__energy / (self.specific_heat_capacity * self.mass))
        return value

    @temperature.setter
    def temperature(self, value: Temperature):
        self.__energy = Energy(joules=self.specific_heat_capacity * self.mass * value)

    @property
    def energy(self) -> Energy:
        return self.__energy

    @energy.setter
    def energy(self, value: Energy):
        self.__energy = value

    @property
    @abstractmethod
    def specific_heat_capacity(self) -> float:
        pass

    @property
    @abstractmethod
    def heat_transfer_coefficient(self) -> float:
        pass

    @property
    def neighbours(self):
        if self.__neighbours is None:
            self.__neighbours = self.parent.neighbours(self.index)
        return self.__neighbours

    @neighbours.setter
    def neighbours(self, value: list["GridComponent"]):
        self.__neighbours = value

    def get_diff(self, other: "GridComponent") -> Optional[dict[str, Unit]]:
        """
        Computes and returns the difference between the physical attributes of two GridComponent
        :param other: the other GridComponent to inspect
        :return:
        """
        if other is None:
            return None
        return {
            "temperature": (other.temperature - self.temperature),
            "volume": (other.volume - self.volume),
            "mass": (other.mass - self.mass),
        }

    def update(self):
        joule_per_time_scale = self.heat_transfer_coefficient * self.surface * TIME_DELTA
        for n in self.neighbours:
            diff = self.get_diff(n)
            if diff:
                self.energy += joule_per_time_scale * diff["temperature"] * TIME_DELTA
                n.energy -= joule_per_time_scale * diff["temperature"] * TIME_DELTA
