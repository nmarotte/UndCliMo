import math
from abc import abstractmethod
from typing import TYPE_CHECKING

import modelsv2.physical_class as ph_class
if TYPE_CHECKING:
    from modelsv2.physical_class.universe import Universe


class CelestialBody:
    __universe: "Universe" = None
    radius: float
    objects_in_line_of_sight: list["CelestialBody"]

    def __init__(self, radius: float):
        self.radius = radius
        self.objects_in_line_of_sight = []
        self.objects_out_of_line_of_sight = []

    @staticmethod
    def get_universe() -> "Universe":
        if CelestialBody.__universe is None:
            from modelsv2.physical_class import universe
            # Reimport exactly the same once at run time when the rest of the program has been built
            CelestialBody.__universe = universe.Universe()
        return CelestialBody.__universe

    @abstractmethod
    def receive_radiation(self, energy: float):
        """
        Defines the behavior of the object when receiving a certain amount of radiation
        :return:
        """

    def solid_angle(self, other: "CelestialBody"):
        """
        Returns the solid angle of the other object as seen from self
        :param other:
        :return: the solid angle in steradians unit
        """
        return math.pi * (other.radius ** 2) / (self.get_universe().distance_between(self, other) ** 2)

    def discover(self, other: "CelestialBody"):
        """
        Update the objects_in_line_of_sight list
        :param other:
        :return:
        """
        if isinstance(self, ph_class.earth.Earth) and isinstance(other, ph_class.sun.Sun) or \
                isinstance(self, ph_class.sun.Sun) and isinstance(other, ph_class.earth.Earth):
            self.objects_in_line_of_sight.append(other)
            other.objects_in_line_of_sight.append(self)
        else:
            self.objects_out_of_line_of_sight.append(other)
            other.objects_out_of_line_of_sight.append(self)

    def sees(self, other: "CelestialBody"):
        """
        Check if the two objects see each other or not
        :param other:
        :return:
        """
        if other in self.objects_in_line_of_sight:
            return True
        else:
            if other in self.objects_out_of_line_of_sight:
                return False
            else:
                self.discover(other)
                return self.sees(other)
