import random
import math
from canvas import Canvas
from figures import Circle, Line


PARAMS = {
    'CANVAS_WIDTH': 40,
    'CANVAS_HEIGHT': 40,
    'MAIN_RADIUS': 14,
    'INNER_CIRCLES': 4,
    'INNER_RADIUSES': 4,
    'INNER_ID': 2,
}


def random_pixel_in_circle(circle: Circle):
    r = circle.get_radius() * math.sqrt(random.random())
    theta = random.random() * 2 * math.pi
    center = circle.get_center()
    x = center[0] + r * math.cos(theta)
    y = center[1] + r * math.sin(theta)

    # rand_pixel_on_circle = random.choice(circle.get_pixel_array())
    # circle_center = circle.get_center()
    # rand_radius = Line(circle_center, rand_pixel_on_circle, circle).get_pixel_array()
    # distribution = (i for i in range(len()))
    return (round(x), round(y))


def run_experiment(canvas: Canvas, **kwargs):
    main_circle = Circle(canvas.get_center_xy(), kwargs['MAIN_RADIUS'], figure_id=0)
    canvas.set_pixel_array(main_circle.get_pixel_array(), main_circle.fig_id)

    # Get two random pixels on the main circle
    rand_pixels = random.sample(main_circle.get_pixel_array(), k=2)

    line = Line(rand_pixels[0], rand_pixels[1], figure_id=1)
    canvas.set_pixel_array(line.get_pixel_array(), line.fig_id)

    for _ in range(kwargs['INNER_CIRCLES']):
        rand_pixel_in_circle = random_pixel_in_circle(main_circle)

        inner_circle = Circle(rand_pixel_in_circle, kwargs['INNER_RADIUSES'], figure_id=kwargs['INNER_ID'])
        canvas.set_pixel_array(inner_circle.get_pixel_array(), inner_circle.fig_id)


def main():
    canvas = Canvas(PARAMS['CANVAS_WIDTH'], PARAMS['CANVAS_HEIGHT'])

    hits = 0
    shots = 0

    # for experiment in range(10_000):
    #     run_experiment(canvas, **PARAMS)
        
    #     # print("Times inner circles overlapped line =", canvas.line_overlaps)
    #     # print("Total inner circles =", INNER_CIRCLES)
    #     # print(f"Road hit probability = {canvas.line_overlaps/INNER_CIRCLES:.2%}")

    #     hits += canvas.line_overlaps
    #     shots += PARAMS['INNER_CIRCLES']

    #     canvas.erase()

    # print("Times inner circles overlapped line =", hits)
    # print("Total inner circles =", shots)
    # print(f"Road hit probability = {hits/shots:.2%}")

    run_experiment(canvas, **PARAMS)
    canvas.print_to_console()



if __name__ == "__main__":
    main()