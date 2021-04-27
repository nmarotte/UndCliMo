from abc import ABC


class MassBody(ABC):
    def __init__(self, mass: float, energy: float):
        self.mass: float = mass  # [kg]
        self.energy: float = energy  # [J]

    def set_energy(self, new_energy):
        self.energy = new_energy
