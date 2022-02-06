import math
from typing import TYPE_CHECKING

from modelsv2.physical_class.sun import Sun

if TYPE_CHECKING:
    from modelsv2.ABC.celestial_body import CelestialBody
from modelsv2.base_class.universe_base import UniverseBase
from modelsv2.ABC.ticking_model import TickingModel
from modelsv2.physical_class.earth import Earth
from modelsv2.utils import EnergyRadiation


class Universe(UniverseBase, TickingModel):
    """
    Singleton class that will contain all other models
    """
    TIME_DELTA: float = 0.01
    EVAPORATION_RATE: float = 0.0001

    def __str__(self):
        res = ""
        if self.sun is not None:
            res += f"{self.sun.__str__()}\n"
        if self.earth is not None:
            res += f"{self.earth.__str__()}\n"
        return res

    def discover_everything(self):
        """
        Exchange 1 virtual photon with every celestial body contained in the universe so that we can know if they can
        see each other in a direct line of sight or not
        :return:
        """
        for obj1 in self:
            for obj2 in self:
                if obj1 is obj2:
                    continue
                obj1.discover(obj2)

    def get_component_at(self, x: int, y=0, z=0):
        return self.earth.get_component_at(x, y, z)

    @staticmethod
    def radiate_inside(energy_radiation: EnergyRadiation):
        for celestial_body in energy_radiation.source.objects_in_line_of_sight:
            solid_angle = energy_radiation.source.solid_angle(celestial_body)
            celestial_body.receive_radiation(energy_radiation.amount_per_time_delta * solid_angle/(4*math.pi))

    @staticmethod
    def distance_between(object1: "CelestialBody", object2: "CelestialBody"):
        if isinstance(object1, Sun) and isinstance(object2, Earth) or isinstance(object1, Earth) and isinstance(object2, Sun):
            return 1.496e11
