from __future__ import annotations

from collections import Iterable

import numpy as np
from numpy.typing import ArrayLike

from Constants import DELTA_T


class WaterBody:
    index: int
    temperature: float
    neighbors: list[WaterBody]
    thermal_diffusivity: float = 0.143  # https://en.wikipedia.org/wiki/Thermal_diffusivity
    co2_diffusivity: float = 1  # ???
    surface = 10  # m^2

    def __init__(self, index: int, temperature: float = 300, co2_ppmv: float = 300):
        self.index = index
        self.temperature = temperature  # In °K
        self.co2_ppmv = co2_ppmv  # In Part Per Million Volume
        self.neighbors = []

    def __repr__(self):
        return str(f"Température : {round(self.temperature, 2)}, CO2 PPMV : {round(self.co2_ppmv, 2)}")

    @classmethod
    def generate_as_shape(cls: WaterBody.__class__, shape: tuple):
        res = np.empty(shape, dtype=cls)
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    index = i * shape[0] * shape[1] + j * shape[2] + k

                    wb = cls(index, np.random.normal(300, 25), np.random.normal(300, 25))
                    if i > 0:
                        wb.add_neighbor(res[i - 1, j, k])
                        res[i - 1, j, k].add_neighbor(wb)
                    if j > 0:
                        wb.add_neighbor(res[i, j - 1, k])
                        res[i, j - 1, k].add_neighbor(wb)
                    if k > 0:
                        wb.add_neighbor(res[i, j, k - 1])
                        res[i, j, k - 1].add_neighbor(wb)
                    res[i, j, k] = wb
        return res

    def add_neighbor(self, neighbor: WaterBody):
        self.neighbors.append(neighbor)

    def tick(self):
        for neighbor in self.neighbors:
            self.average_temperature(neighbor)
            self.average_co2(neighbor)

    def average_temperature(self, other: WaterBody):
        diff = abs(other.temperature - self.temperature)
        rate_of_temperature_change = WaterBody.thermal_diffusivity * WaterBody.surface * diff * DELTA_T
        if self.temperature > other.temperature:
            self.temperature -= rate_of_temperature_change
            other.temperature += rate_of_temperature_change
        else:
            self.temperature += rate_of_temperature_change
            other.temperature -= rate_of_temperature_change

    def average_co2(self, other: WaterBody):
        diff = abs(other.co2_ppmv - self.co2_ppmv)
        rate_of_co2_change = WaterBody.co2_diffusivity * WaterBody.surface * diff * DELTA_T
        if self.co2_ppmv > other.co2_ppmv:
            self.co2_ppmv -= rate_of_co2_change
            other.co2_ppmv += rate_of_co2_change
        else:
            self.co2_ppmv += rate_of_co2_change
            other.co2_ppmv -= rate_of_co2_change
