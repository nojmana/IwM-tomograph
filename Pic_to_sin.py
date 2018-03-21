from Bresenham import Bresenham
import numpy as np
import math


class Transform:
    def __init__(self):
        self.alpha = 90
        self.detectors_amount = 2
        self.width = 180

    def get_emitter_positions(self, picture_size):
        #calculate center and radius of the circle
        x0 = picture_size / 2
        y0 = picture_size / 2
        r = int((picture_size - 1) / 2)
        radians = math.radians(self.alpha)

        #calculate all positions of emitter from 0 to 360 with alpha step
        positions = []
        for i in range(0, int(math.floor(360 / self.alpha))):
            x = round(r * math.cos(i * radians) + x0, 0)
            y = round(r * math.sin(i * radians) + y0, 0)
            positions.append((int(x), int(y)))
        return positions

    def get_detectors_positions_for_current_angle(self, picture_size, angle):
        detectors_positions = []
        # calculate center and radius of the circle
        x0 = picture_size / 2
        y0 = picture_size / 2
        r = int((picture_size - 1) / 2)
        radians_start = math.radians(angle + 180 - self.width/2)
        radians_stop = math.radians(angle + 180 + self.width/2)
        #calculate all detectors positions
        for i in np.linspace(radians_start, radians_stop, self.detectors_amount):
            x = round(r * math.cos(i) + x0, 0)
            y = round(r * math.sin(i) + y0, 0)
            detectors_positions.append((int(x), int(y)))
        return detectors_positions

    def make_sinogram(self, picture):
        picture_size = len(picture[0])
        emitter_positions = self.get_emitter_positions(picture_size)
        all_detectors = []
        for i in np.linspace(0.0, 360.0, len(emitter_positions), False):
            all_detectors.append(self.get_detectors_positions_for_current_angle(picture_size, i))
        #join all emiter positions and detectors
        all_positions = []
        for i in range(len(emitter_positions)):
            all_positions.append((emitter_positions[i], all_detectors[i]))
        #b = Bresenham.Bresenham()
        sinogram = Bresenham.algorithm(all_positions, self.detectors_amount, picture)
        return sinogram
