from Bresenham import Bresenham
import numpy as np
import math


class Position:
    def __init__(self, detectors):
        self.emitter_position = None
        self.detectors = detectors

    def set_emitter_position(self, emitter_position):
        self.emitter_position = emitter_position


class Transform:
    def __init__(self):
        self.alpha = 90
        self.detectors_amount = 2
        self.width = 180
        self.all_positions = []
        self.all_lines = []
        self.progress = 5

    def generate_all_positions(self, picture):
        picture_size = len(picture[0])
        emitter_positions = self.get_emitter_positions(picture_size)
        all_positions = []
        for i in np.linspace(0.0, 360.0, len(emitter_positions), False):
            all_positions.append(Position(self.get_detectors_positions_for_current_angle(picture_size, i)))
        for i in range(len(all_positions)):
            all_positions[i].set_emitter_position(emitter_positions[i])
        self.all_positions = all_positions
        self.all_lines = Bresenham.generate_all_lines(all_positions)

    def get_emitter_positions(self, picture_size):
        # calculate center and radius of the circle
        x0 = picture_size / 2
        y0 = picture_size / 2
        r = int((picture_size - 1) / 2)
        radians = math.radians(self.alpha)

        # calculate all positions of emitter from 0 to 360 with alpha step
        emitter_positions = []
        for i in range(0, int(math.floor(360 / self.alpha))):
            x = round(r * math.cos(i * radians) + x0, 0)
            y = round(r * math.sin(i * radians) + y0, 0)
            emitter_positions.append((int(x), int(y)))
        return emitter_positions

    def get_detectors_positions_for_current_angle(self, picture_size, angle):
        detectors_positions = []
        # calculate center and radius of the circle
        x0 = picture_size / 2
        y0 = picture_size / 2
        r = int((picture_size - 1) / 2)
        radians_start = math.radians(angle + 180 - self.width/2)
        radians_stop = math.radians(angle + 180 + self.width/2)
        # calculate all detectors positions
        for i in np.linspace(radians_start, radians_stop, self.detectors_amount):
            x = round(r * math.cos(i) + x0, 0)
            y = round(r * math.sin(i) + y0, 0)
            detectors_positions.append((int(x), int(y)))
        return detectors_positions

    def make_sinogram_iter(self, picture):
        sinogram, is_end = Bresenham.algorithm_iter(self.all_lines, self.all_positions, self.detectors_amount, picture)
        return sinogram, is_end

    def make_sinogram(self, picture):
        sinogram = Bresenham.algorithm(self.all_lines, self.all_positions, self.detectors_amount, picture, self.progress)
        return sinogram

    def restore_picture(self, sinogram, picture_size, filter_props):
        picture = Bresenham.inverse_algorithm(self.all_lines, sinogram, picture_size, filter_props)
        return picture
