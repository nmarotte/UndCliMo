from modelsv2.physical_class.sun import Sun
from modelsv2.ABC.ticking_model import TickingModel
from modelsv2.utils import EnergyRadiation


class TickingSun(Sun, TickingModel):
    @TickingModel.on_tick
    def radiate_energy_outwards(self):
        """
        Update function for the Sun.

        Behavior :
            Updates the amount of energy contained in the sun
            Radiate that energy outward
        :return:
        """
        energy_per_time_delta = self.energy_radiated_per_second * self.get_universe().TIME_DELTA
        self.get_universe().radiate_inside(EnergyRadiation(self, energy_per_time_delta))
