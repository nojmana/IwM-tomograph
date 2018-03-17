import copy
import numpy as np

class Bresenham:
    def draw_line(self, x1, y1, x2, y2):
        kx = 1 if x1 <= x2 else -1
        ky = 1 if y1 <= y2 else -1

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        line = [[x1, y1]]

        if dx >= dy:
            error = dx / 2
            for i in range(0, dx):
                x1 = x1 + kx
                error = error - dy
                if error < 0:
                    y1 = y1 + ky
                    error = error + dx
                line.append([x1, y1])
        else:
            error = dy / 2
            for i in range(0, dy):
                y1 = y1 + ky
                error = error - dx
                if error < 0:
                    x1 = x1 + kx
                    error = error + dy
                line.append([x1, y1])
        return line

    def algorithm(self, data, detectors_amount, picture):
        all_lines = []
        #iterate over all emitter's positions
        for i in range(len(data)):
            lines = []
            emitter = data[i][0]
            #iterate over all detectors
            for j in range(detectors_amount):
                detector = data[i][1][j]
                line = self.draw_line(emitter[0], emitter[1], detector[0], detector[1])
                lines.append(line)
            all_lines.append(lines)


        #show all lines
        picture2 = copy.copy(picture)
        for i in range(len(picture)):
            for j in range(len(picture)):
                picture2[i][j] = 0
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                x = lines[i][j][0]
                y = lines[i][j][1]
                picture2[x][y] = 255
        return picture2