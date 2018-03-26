import numpy as np
from skimage import filters
from Main_view import MainWindow


class Bresenham(MainWindow):
    iter = 0
    iter_sinogram = None
    all_averages = None

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
    def generate_all_lines(position):
        emitter_positions = []
        for i in range(len(position)):  # iterate over all emitter's positions
            detectors = []
            emitter = position[i].emitter_position
            detectors_amount = len(position[i].detectors)
            for j in range(detectors_amount):  # iterate over all detectors
                detector = position[i].detectors[j]
                line = Bresenham.generate_line(emitter[0], emitter[1], detector[0], detector[1])
                detectors.append(line)
            emitter_positions.append(detectors)
        return emitter_positions

    @staticmethod
    def generate_avgs_of_lines(all_lines, picture):
        all_avgs = []
        for lines in all_lines:  # iterate over all emitter positions
            avg = []
            for line in lines:  # iterate over all detectors
                avg_temp = 0
                for x, y in line:  # calculate avg for line from emitter position to detector position
                    avg_temp = avg_temp + picture[x][y]
                avg_temp = avg_temp
                avg.append(avg_temp)
            all_avgs.append(avg)
        return all_avgs

    @staticmethod
    def generate_picture(all_lines, sinogram, picture_size):
        picture = np.ones((picture_size, picture_size))
        counter = np.zeros((picture_size, picture_size))
        for i, lines in enumerate(all_lines):  # iterate over all emitter positions
            for j, line in enumerate(lines):  # iterate over all detectors
                for x, y in line:  # add value from sinogram to every pixel of line
                    picture[x][y] += sinogram[j][i]
                    counter[x][y] += 1
        for i in range(len(counter)):
            for j in range(len(counter[i])):
                if counter[i][j] != 0:
                    picture[i][j] /= counter[i][j]
        return picture

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
    def normalize(data):
        maximum = np.amax(data)
        for i in range(len(data)):
            for j in range(len(data[i])):
                if maximum != 0:
                    data[i][j] = round(data[i][j] / maximum * 255)
        return data

    @staticmethod
    def algorithm(all_lines, all_positions, detectors_amount, picture, progress):
        all_averages = Bresenham.generate_avgs_of_lines(all_lines, picture)
        sinogram = np.ones((detectors_amount, len(all_positions)))  # matrix of size emiters_positions x detectors_amount
        for x in range(len(all_averages)):
            for y in range(len(all_averages[x])):
                sinogram[y][x] = all_averages[x][y]
            if x/len(all_averages) >= progress/5:
                break
        sinogram = Bresenham.normalize(sinogram)
        # return Bresenham.show_rays(picture, all_lines)
        return sinogram

    @staticmethod
    def algorithm_iter(all_lines, all_positions, detectors_amount, picture):
        if Bresenham.iter == 0:
            Bresenham.all_averages = Bresenham.generate_avgs_of_lines(all_lines, picture)
            Bresenham.iter_sinogram = np.ones(
                (detectors_amount, len(all_positions)))  # matrix of size emiters_positions x detectors_amount
            for y in range(len(Bresenham.all_averages[Bresenham.iter])):
                Bresenham.iter_sinogram[y][Bresenham.iter] = Bresenham.all_averages[Bresenham.iter][y]
            Bresenham.iter += 1
        elif Bresenham.iter < len(Bresenham.all_averages):
            for y in range(len(Bresenham.all_averages[Bresenham.iter])):
                Bresenham.iter_sinogram[y][Bresenham.iter] = Bresenham.all_averages[Bresenham.iter][y]
            Bresenham.iter += 1
        else:
            Bresenham.iter = 0
        sinogram = Bresenham.normalize(np.copy(Bresenham.iter_sinogram))
        return sinogram, Bresenham.iter == 0

    @staticmethod
    def inverse_algorithm(all_lines, sinogram, picture_size, filter_props):
        picture = Bresenham.generate_picture(all_lines, sinogram, picture_size)
        picture = picture ** filter_props.gamma
        picture = filters.gaussian(picture, sigma=filter_props.gauss)
        picture = Bresenham.normalize(picture)
        return picture
