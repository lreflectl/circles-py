import math
Pixel = tuple[int, int]


class Circle:
    def __init__(self, center: Pixel, radius: int, figure_id: int):
        self.fig_id = figure_id
        self._x = center[0]
        self._y = center[1]
        self._r = radius
        self._pixel_array = []

        self.create_pixel_array()

    def create_pixel_array(self):
        pixels = set()

        for i in range(0, self._r - 1):
            shift = int(round(math.sqrt(math.pow(self._r - 1, 2) - math.pow(i, 2))))

            pixels.add((self._x + i, self._y + shift))
            pixels.add((self._x - i, self._y + shift))
            pixels.add((self._x + i, self._y - shift))
            pixels.add((self._x - i, self._y - shift))

            diff_shift = self._y - self._x
            pixels.add((self._y + shift - diff_shift, self._x + i + diff_shift))
            pixels.add((self._y + shift - diff_shift, self._x - i + diff_shift))
            pixels.add((self._y - shift - diff_shift, self._x + i + diff_shift))
            pixels.add((self._y - shift - diff_shift, self._x - i + diff_shift))

        self._pixel_array.extend(pixels)

    def get_pixel_array(self) -> list[Pixel]:
        return self._pixel_array
    
    def get_center(self) -> Pixel:
        return (self._x, self._y)
    
    def get_radius(self) -> int:
        return self._r


class Line:
    def __init__(self, start: Pixel, end: Pixel, figure_id: int):
        self.fig_id = figure_id
        self._start_x = start[0]
        self._start_y = start[1]
        self._end_x = end[0]
        self._end_y = end[1]
        self._pixel_array = []
        self._b = 0
        self._c = 0

        self.create_pixel_array()

    def _calc_equation_coefs(self):
        if self._end_x - self._start_x == 0:
            self._b = 0
        else:
            self._b = (self._end_y - self._start_y) / (self._end_x - self._start_x)
        self._c = self._start_y - self._b * self._start_x

    def create_pixel_array(self):
        pixels = set()

        self._calc_equation_coefs()
        x_direction = 1 if self._end_x >= self._start_x else -1
        # Going through x axis and calculating y's
        for x in range(self._start_x + x_direction, self._end_x, x_direction):
            y = self._b * x + self._c
            # Round (or strip, or ceil) calculated y
            y = round(y)
            pixels.add(Pixel((x, y)))
        
        ys_to_skip = set(p[1] for p in pixels)
        y_direction = 1 if self._end_y >= self._start_y else -1
        # Going through y axis and calculating missing x's
        for y in range(self._start_y + y_direction, self._end_y, y_direction):
            if y in ys_to_skip:
                continue
            if self._b == 0:
                x = self._start_x
            else:
                x = (y - self._c) / self._b
            # Round (or strip, or ceil) calculated x
            x = round(x)
            pixels.add(Pixel((x, y)))
        
        self._pixel_array.extend(pixels)
        self._pixel_array.append(Pixel((self._start_x, self._start_y)))
        self._pixel_array.append(Pixel((self._end_x, self._end_y)))

    def get_pixel_array(self) -> list[Pixel]:
        return self._pixel_array


