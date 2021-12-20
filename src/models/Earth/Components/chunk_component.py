from typing import Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from models.Earth.Components.grid_chunk import GridChunk
from units import *
import constants


class ChunkComponent:
    """
        A class to represent a component of a chunk.

        ...

        Attributes
        ----------
        chunk: GridChunk
            The reference to the parent (container) GridChunk
        mass: Mass(float)
            The Mass of the component, will be used as kg
        specific_heat_capacity:
            The amount of heat that must be added to a material to increase its temperature
            See https://en.wikipedia.org/wiki/Specific_heat_capacity
            Expressed in Joules per Kilograms per Kelvin (Water = 4184 Jkg-1K-1)
        heat_transfer_coefficient:
            Coefficient for Newton's law of Cooling
            See https://en.wikipedia.org/wiki/Heat_transfer_coefficient
            Expressed in Watt per Meter squared per Kelvin
        energy: Energy(float)
            The molecular kinetic energy of the component. It is used to store and compute the temperature of the
            component
        """
    chunk: "GridChunk" = None
    __mass: Mass
    specific_heat_capacity: float
    heat_transfer_coefficient: float
    energy: Energy = 0

    def __init__(self, mass: Mass, temperature: Temperature, *, component_type: str):
        # Information on the component
        self.component_type = component_type.upper()

        # Physical properties
        self.__mass = mass

        self.specific_heat_capacity = constants.SPECIFIC_HEAT_CAPACITY[self.component_type]
        self.heat_transfer_coefficient = constants.SPECIFIC_HEAT_CAPACITY[self.component_type]
        self.__set_temperature(temperature)

    @classmethod
    def init_default(cls, *, component_type: str):
        return cls(mass=Mass(kilograms=1000), temperature=Temperature(celsius=21),
                   component_type=component_type)

    @property
    def mass(self) -> Mass:
        return self.__mass

    @mass.setter
    def mass(self, value: Union[Mass, float]):
        diff = value - self.__mass
        self.__mass = value if isinstance(value, Mass) else Mass(kilograms=value)
        self.chunk.total_mass += diff

    def change_mass(self, value: Union[Mass, float]):
        """
        Change the mass of the component and keep the same temperature
        :param value:
        :return:
        """
        temperature = self.__get_temperature()  # Save the temperature, because the energy will remain the same in smaller mass
        self.mass = value
        self.__set_temperature(temperature)

    def __get_temperature(self):
        return Temperature(kelvin=self.energy / (self.specific_heat_capacity * self.mass))

    def __set_temperature(self, temperature: Union[Temperature, float]):
        self.energy = Energy(joules=self.specific_heat_capacity * self.mass * temperature)

    def __str__(self):
        res = f"{self.component_type} Component \n" \
              f"Mass : {self.mass} \n " \
              f"Temperature : {self.__get_temperature()} K ({self.energy} J)"
        return res
