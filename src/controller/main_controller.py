import math
import threading
from typing import Optional

from PyQt5 import QtWidgets
import qtawesome as qta

from models.Earth.earth import Earth
from models.model import Model
from sun import Sun
from views.main_view import MainView
from constants import CANVAS_SIZE, ICON_SIZE
from controller.CanvasArea.canvas_area_controller import CanvasAreaController
from controller.ToolbarArea.toolbar_area_controller import ToolbarController
from controller.exception_controller import MessageController
from messages import MessageToProcess
from models.Earth.Components.chunk_component import ChunkComponent
from models.Earth.Components.grid_chunk import GridChunk
from universe import Universe


class MainController:
    model: Universe
    simulation_thread: Optional[threading.Thread] = None

    def __init__(self):
        self.model = Universe()
        self.model.earth = Earth(shape=CANVAS_SIZE, parent=self.model)
        self.model.sun = Sun()
        self.message_controller = MessageController(parent_controller=self)
        self.toolbar_controller = ToolbarController(parent_controller=self)
        self.canvas_controller = CanvasAreaController(parent_controller=self)
        self.view = MainView(controller=self)

    def clear_pressed(self):
        self.canvas_controller.clear_canvas()
        self.model = Universe()
        self.model.earth = Earth(shape=CANVAS_SIZE, parent=self.model)
        self.model.sun = Sun()

    def start_pressed(self):
        self.canvas_controller.set_canvas_enabled(False)
        self.__start_simulation()

    def update_pressed(self):
        self.simulation_thread = threading.Thread(target=self.model.update, args=())
        self.simulation_thread.start()

    def pause_pressed(self):
        self.canvas_controller.set_canvas_enabled(True)
        self.__pause_simulation()

    def resume_pressed(self):
        self.canvas_controller.set_canvas_enabled(False)
        self.__resume_simulation()

    def stop_pressed(self):
        self.canvas_controller.set_canvas_enabled(True)
        self.__stop_simulation()

    def __start_simulation(self):
        self.simulation_thread = threading.Thread(target=self.model.start_simulation, args=())
        self.simulation_thread.start()

    def __pause_simulation(self):
        self.model.pause_updating()

    def __resume_simulation(self):
        self.simulation_thread = threading.Thread(target=self.model.resume_updating, args=())
        self.simulation_thread.start()

    def __stop_simulation(self):
        self.model.stop_updating()
        self.simulation_thread = None

    def get_brush_width(self):
        return self.toolbar_controller.get_brush_width()

    def finish_process_message(self, message: type[MessageToProcess]):
        self.message_controller.pop_message(message)

    def process_message(self, message: MessageToProcess):
        self.message_controller.push_message(message)

    def is_message_processing(self, exception: type[MessageToProcess]):
        return any(isinstance(e, exception) for e in self.message_controller.message_stack)

    def components_painted(self, *positions: tuple[int, int]):
        for x, y in set(positions):
            chunk = self.toolbar_controller.select_component_controller.get_grid_chunk().deep_copy()
            chunk.index = x + y * self.model.earth.shape[1]
            chunk.parent = self.model.earth
            chunk.neighbours = chunk.parent.neighbours(chunk.index)
            self.model.earth.set_component_at(chunk, x, y)

    def get_ratios(self):
        return self.toolbar_controller.select_component_controller.get_ratios()

    def get_grid_chunk(self):
        return self.toolbar_controller.select_component_controller.get_grid_chunk()

    def set_sun_energy_per_second(self, energy_per_second: float):
        self.model.sun.energy_radiated_per_second = energy_per_second

    def set_earth_radiation_ratio(self, earth_radiation_ratio: float):
        self.model.sun.earth_radiation_ratio = earth_radiation_ratio

    def get_energy_per_second(self):
        return self.model.sun.energy_radiated_per_second

    def get_earth_radiation_ratio(self):
        return self.model.sun.earth_radiation_ratio

    def get_time_delta(self):
        return self.model.universe.TIME_DELTA


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    controller = MainController()

    controller.view.show()
    app.exec_()
