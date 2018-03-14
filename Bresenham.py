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


    def algorithm(self, data, detectors_amount):
        lines = []
        for i in range(len(data)):
            emitter = data[i][0]
            for j in range(detectors_amount):
                detector = data[i][1][j]
                line = self.draw_line(emitter[0], emitter[1], detector[0], detector[1])
                lines.append(line)
