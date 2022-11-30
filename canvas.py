import time
import random
import os
from figures import Circle, Line

Pixel = tuple[int, int]


class Canvas:
    def __init__(self, size_x: int, size_y: int):
        self._x = size_x
        self._y = size_y
        self._canvas = [['.' for _ in range(self._x)] for _ in range(self._y)]
        self.line_overlaps = 0

    def get_center_xy(self) -> Pixel:
        return int(self._x / 2), int(self._y / 2)
    
    # Checks if pixel of a new figure overlaps with another
    # Return index of figure which collides
    def detect_collision(self, x: int, y: int):
        if not (0 <= x <= self._x and 0 <= y <= self._y):
            raise Exception('Pixel coordinates out of bounds!')
        if self._canvas[y][x] == '*':
            return '*'
        elif self._canvas[y][x] != '.':
            return int(self._canvas[y][x])
            
    def set_pixel(self, x: int, y: int, mark: str):
        if 0 <= x <= self._x and 0 <= y <= self._y:
            self._canvas[y][x] = mark
        else:
            raise Exception('Pixel coordinates out of bounds!')
    
    # Set pixels according to their collision and count line overlaps
    def set_pixel_array(self, group: list[Pixel], figure_id: int):
        inner_overlapped_line = False
        for pixel in group:
            overlapped_figure_id = self.detect_collision(*pixel)
            if overlapped_figure_id == None:
                self.set_pixel(*pixel, str(figure_id))
            elif overlapped_figure_id == 1:
                if not inner_overlapped_line:
                    self.line_overlaps += 1
                    inner_overlapped_line = True
            elif overlapped_figure_id == 0 and figure_id == 1:
                self.set_pixel(*pixel, str(figure_id))
            else:
                self.set_pixel(*pixel, '*')

    def erase(self):
        self._canvas = [['.' for _ in range(self._x)] for _ in range(self._y)]
        self.line_overlaps = 0

    def print_to_console(self):
        # Clear canva
        os.system('cls')
        for y in range(self._y - 1, -1, -1):
            for x in range(self._x):
                print(self._canvas[y][x], end='  ')
            print()
    
    def get_pixel_array(self):
        return self._canvas


if __name__ == '__main__':
    canvas1 = Canvas(31, 31)

    circle = Circle((15, 15), 9, figure_id=0)
    canvas1.set_pixel_array(circle.get_pixel_array(), circle.fig_id)
    canvas1.print_to_console()

    rand_pixels = random.choices(circle.get_pixel_array(), k=2)

    line = Line(rand_pixels[0], rand_pixels[1], figure_id=1)
    canvas1.set_pixel_array(line.get_pixel_array(), line.fig_id)
    canvas1.print_to_console()
    
