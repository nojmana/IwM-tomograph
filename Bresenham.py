import numpy as np


class Bresenham:

    @staticmethod
    def generate_line(x1, y1, x2, y2):
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

    @staticmethod
    def generate_all_lines( data, detectors_amount):
        emitter_positions = []
        for i in range(len(data)):  # iterate over all emitter's positions
            detectors = []
            emitter = data[i][0]
            for j in range(detectors_amount):  # iterate over all detectors
                detector = data[i][1][j]
                line = Bresenham.generate_line(emitter[0], emitter[1], detector[0], detector[1])
                detectors.append(line)
            emitter_positions.append(detectors)
        return emitter_positions

    @staticmethod
    def generate_avgs_of_lines(all_lines, picture):
        all_avgs = []
        for lines in all_lines: #iterate over all emitter positions
            avg = []
            for line in lines: #iterate over all detectors
                avg_temp = 0
                for x, y in line: #calculate avg for line from emiter position to detector position
                    avg_temp = avg_temp + picture[x][y]
                avg_temp = avg_temp
                avg.append(avg_temp)
            all_avgs.append(avg)
        return all_avgs

    @staticmethod
    def show_rays(picture, all_lines):
        for line in all_lines:
            for i in range(len(picture)):
                for j in range(len(picture)):
                        picture[i][j] = 0
                for i in range(len(line)):
                    for j in range(len(line[i])):
                        x = line[i][j][0]
                        y = line[i][j][1]
                        picture[x][y] = 255
        return picture

    @staticmethod
    def normalize_sinogram(sinogram):
        maximum = np.amax(sinogram)
        for i in range(len(sinogram)):
            for j in range(len(sinogram[i])):
                if maximum != 0:
                    sinogram[i][j] = round(sinogram[i][j] / maximum * 255)
        return sinogram

    @staticmethod
    def algorithm(data, detectors_amount, picture):
        all_lines = Bresenham.generate_all_lines(data, detectors_amount)
        all_averages = Bresenham.generate_avgs_of_lines(all_lines, picture)
        sinogram = np.ones((detectors_amount, len(data))) #sinogram will be matrix of size emiters_positions x detectors_amount
        for x in range(len(all_averages)):
            for y in range(len(all_averages[x])):
                sinogram[y][x] = all_averages[x][y]

        sinogram = Bresenham.normalize_sinogram(sinogram)
        #return self.show_rays(picture, all_lines)
        return sinogram