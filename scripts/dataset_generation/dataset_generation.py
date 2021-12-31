"""
Generate a dataset for detecting shapes
"""
import os
import random
from typing import Tuple, List

import cv2
import numpy as np

all_shapes = ['ellipse', 'circle', 'square', 'rectangle', 'line', 'arrow', 'triangle', 'star']

shape_to_index = dict(zip(all_shapes, range(len(all_shapes))))

# Generated using https://mokole.com/palette.html
colors = {
    'darkgreen': '#006400',
    'darkblue': '#00008B',
    'maroon3': '#B03060',
    'orangered': '#FF4500',
    'gold': '#FFD700',
    'lawngreen': '#7CFC00',
    'aqua': '#00FFFF',
    'fuchsia': '#FF00FF',
    'cornflower': '#6495ED',
    'peachpuff': '#FFDAB9',
}


def convert_hex_color_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hex color to RGB
    """
    red = int(hex_color[1:3], 16)
    green = int(hex_color[3:5], 16)
    blue = int(hex_color[5:7], 16)
    return red, green, blue


def create_blank_canvas(canvas_shape: Tuple[int, int], color: Tuple[int, int, int] = (0, 0, 0)):
    """
    Create a blank canvas with color
    """
    width, height = canvas_shape
    canvas = np.zeros((height, width, 3), np.uint8)
    # convert color tuple to BGR
    color = color[::-1]
    canvas[:] = color
    return canvas


def line_intersection(line1: List[Tuple[int, int]], line2: List[Tuple[int, int]]):
    """
    Find the intersection of two lines
    https://stackoverflow.com/a/20677983/7998814
    """

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def add_shape_to_canvas(canvas, shape: str, shape_center: Tuple[int, int] = (100, 100),
                        shape_size: Tuple[int, int] = (64, 64), color=(0, 0, 0),
                        stroke_width=1, draw_bounding_box=False, bounding_box_color=(0, 0, 0)):
    """
    Add a shape to a canvas with a color and stroke width and fill it with the color
    """
    # convert color tuple to BGR
    color = color[::-1]

    if shape not in all_shapes:
        raise ValueError('shape must be one of: {}'.format(all_shapes))
    if shape == 'circle':
        canvas, max_bounding_box = add_circle_to_canvas(canvas, color, shape_center, shape_size, stroke_width)
    elif shape == 'ellipse':
        canvas, max_bounding_box = add_ellipse_to_canvas(canvas, color, shape_center, shape_size)
    elif shape in {'rectangle', 'square'}:
        canvas, max_bounding_box = add_rectangle_to_canvas(canvas, color, shape_center, shape_size, stroke_width)
    elif shape == 'line':
        canvas, max_bounding_box = add_line_to_canvas(canvas, color, shape_center, shape_size, stroke_width)
    elif shape == 'arrow':
        canvas, max_bounding_box = add_arrow_to_canvas(canvas, color, shape_center, shape_size, stroke_width)
    elif shape == 'triangle':
        canvas, max_bounding_box = add_triangle_to_canvas(canvas, color, shape_center, shape_size, stroke_width)
    elif shape == 'star':
        radius = shape_size[0] // 2
        canvas, max_bounding_box = add_star_to_canvas(canvas, color, shape_center, radius)
    else:
        raise ValueError(f'Implemented shape {shape} cannot be drawn')

    stroke_width_padding = stroke_width * 2

    # Add the stroke width to the max bounding box
    max_bounding_box = (max_bounding_box[0] - stroke_width_padding, max_bounding_box[1] - stroke_width_padding,
                        max_bounding_box[2] + stroke_width_padding, max_bounding_box[3] + stroke_width_padding)

    # ensure that the max bounding box only contains ints
    max_bounding_box = (int(max_bounding_box[0]), int(max_bounding_box[1]),
                        int(max_bounding_box[2]), int(max_bounding_box[3]))

    if draw_bounding_box:
        # Draw a red bounding box around the shape using the maximum bounding box
        canvas = cv2.rectangle(canvas, (max_bounding_box[0], max_bounding_box[1]), (
            max_bounding_box[2], max_bounding_box[3]), bounding_box_color, 2)
    return canvas, max_bounding_box


def add_line_to_canvas(canvas, color, shape_center, shape_size, stroke_width):
    x1, y1 = shape_center
    x2, y2 = shape_center[0] + shape_size[0], shape_center[1] + shape_size[1]
    canvas = cv2.line(canvas, (x1, y1), (x2, y2), color, stroke_width)
    max_bounding_box = (x1, y1, x2, y2)
    return canvas, max_bounding_box


def add_circle_to_canvas(canvas: np.ndarray, color: Tuple[int, int, int], shape_center: Tuple[int, int],
                         shape_size: Tuple[int, int], stroke_width: int):
    radius = int(shape_size[0] / 2)
    center = (shape_center[0] + radius, shape_center[1] + radius)
    cv2.circle(canvas, center, radius, color, stroke_width)
    # fill the circle with the color
    cv2.circle(canvas, center, radius, color, -1)
    max_bounding_box = (center[0] - radius, center[1] - radius,
                        center[0] + radius, center[1] + radius)
    return canvas, max_bounding_box


def add_ellipse_to_canvas(canvas: np.ndarray, color: Tuple[int, int, int], shape_center: Tuple[int, int],
                          shape_size: Tuple[int, int]):
    w, h = shape_size
    center = (int(shape_center[0] + w / 2), int(shape_center[1] + h / 2))
    # fill the ellipse with the color
    cv2.ellipse(canvas, center, (w // 2, h // 2), 0, 0, 360, color, -1)
    max_bounding_box = (center[0] - w / 2, center[1] - h / 2,
                        center[0] + w / 2, center[1] + h / 2)
    return canvas, max_bounding_box


def add_rectangle_to_canvas(canvas: np.ndarray, color: Tuple[int, int, int], shape_center: Tuple[int, int],
                            shape_size: Tuple[int, int], stroke_width: int):
    x1, y1 = shape_center
    x2, y2 = shape_center[0] + shape_size[0], shape_center[1] + shape_size[1]
    canvas = cv2.rectangle(canvas, (x1, y1), (x2, y2), color, stroke_width)
    # Fill the rectangle with the color
    canvas = cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)
    max_bounding_box = (x1, y1, x2, y2)
    return canvas, max_bounding_box


def add_arrow_to_canvas(canvas: np.ndarray, color: Tuple[int, int, int], shape_center: Tuple[int, int],
                        shape_size: Tuple[int, int], stroke_width: int):
    x1, y1 = shape_center
    x2, y2 = shape_center[0] + shape_size[0], shape_center[1] + shape_size[1]
    canvas = cv2.arrowedLine(
        canvas, (x1, y1), (x2, y2), color, stroke_width)
    max_bounding_box = (x1, y1, x2, y2)
    return canvas, max_bounding_box


def add_triangle_to_canvas(canvas: np.ndarray, color: Tuple[int, int, int], shape_center: Tuple[int, int],
                           shape_size: Tuple[int, int], stroke_width: int):
    x1, y1 = shape_center
    x2, y2 = shape_center[0] + shape_size[0], shape_center[1] + shape_size[1]
    x3, y3 = shape_center[0] + shape_size[0] / 2, shape_center[1] + shape_size[1]
    pts = np.array([[x1, y1], [x2, y2], [x3, y3]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    canvas = cv2.polylines(canvas, [pts], True, color, stroke_width)
    # Fill the triangle with the color
    canvas = cv2.fillPoly(canvas, [pts], color)
    max_bounding_box = (x1, y1, x2, int(max(y2, y3)))
    return canvas, max_bounding_box


def add_star_to_canvas(canvas: np.ndarray, color: Tuple[int, int, int], center: Tuple[int, int], radius: int):
    """
    Add a star to the canvas
    """
    # convert color tuple to BGR
    color = color[::-1]

    # # Draw a blue circle at the center
    # cv2.circle(canvas, center, radius, (255,0,0), -1)

    # The following code is adopted from https://programmerall.com/article/22831425530/
    # This code was found on a few pages likely a result of pages copying each other
    # That being said, I have no idea what the code does

    # Draw a yellow pentagon star
    # The first step by means of a rotation angle to find five vertices

    # Explain the following line of code:
    # https://stackoverflow.com/a/15015748/7998814
    phi = 4 * np.pi / 5
    rotations = [[[np.cos(i * phi), -np.sin(i * phi)], [i * np.sin(phi), np.cos(i * phi)]] for i in range(1, 5)]
    pentagram = np.array([[[[0, -1]] + [np.dot(m, (0, -1)) for m in rotations]]], dtype=np.float)

    # Define the zoom multiple and the transfer vector to put the pentagonal star above the left half of the picture
    pentagram = np.round(pentagram * radius + np.array(center)).astype(np.int)

    # Draw the star using lines
    # cv2.polylines(canvas, pentagram, True, (0, 255, 255), 9)

    # End of code from https://programmerall.com/article/22831425530/

    # Get the points of the star
    pentagram_points = pentagram[0][0]

    # Create a mapping for ease of use
    star_points = {
        'top_center': pentagram_points[0],
        'bottom_right': pentagram_points[1],
        'middle_left': pentagram_points[2],
        'middle_right': pentagram_points[3],
        'bottom_left': pentagram_points[4],
    }

    # Create a mapping for ease of use
    # This dict uses the order of which lines are drawn to determine as keys
    lines_for_star = {
        1: [star_points['top_center'], star_points['bottom_right']],
        2: [star_points['bottom_right'], star_points['middle_left']],
        3: [star_points['middle_left'], star_points['middle_right']],
        4: [star_points['middle_right'], star_points['bottom_left']],
        5: [star_points['bottom_left'], star_points['top_center']],
    }
    # In a more human readable format the lines are drawn in the following order:
    # 1. Top center to bottom right
    # 2. Bottom right to middle left
    # 3. Middle left to middle right
    # 4. Middle right to bottom left
    # 5. Bottom left to top center

    # In order to draw a solid star, we need to get the points where the lines intersect
    polyfill_points = []

    polyfill_points.append(star_points['top_center'])
    top_center_to_middle_right = line_intersection(lines_for_star[1], lines_for_star[3])

    polyfill_points.append(top_center_to_middle_right)
    polyfill_points.append(star_points['middle_right'])

    middle_right_to_bottom_right = line_intersection(lines_for_star[1], lines_for_star[4])
    polyfill_points.append(middle_right_to_bottom_right)
    polyfill_points.append(star_points['bottom_right'])

    bottom_right_to_bottom_left = line_intersection(lines_for_star[2], lines_for_star[4])
    polyfill_points.append(bottom_right_to_bottom_left)
    polyfill_points.append(star_points['bottom_left'])

    bottom_left_to_middle_left = line_intersection(lines_for_star[2], lines_for_star[5])
    polyfill_points.append(bottom_left_to_middle_left)
    polyfill_points.append(star_points['middle_left'])

    middle_left_to_top_center = line_intersection(lines_for_star[3], lines_for_star[5])
    polyfill_points.append(middle_left_to_top_center)

    # Ensure that polyfill_points only contains tuples of integers
    polyfill_points = [(int(x), int(y)) for x, y in polyfill_points]

    # # Draw the points of the star for debugging
    # colors_to_use = random.sample(colors.keys(), len(colors))
    # for i, point in enumerate(polyfill_points):
    #     # color random
    #     color_label = colors_to_use[i]
    #     pt_color = convert_hex_color_to_rgb(colors[color_label])
    #     # convert color tuple to BGR
    #     pt_color = pt_color[::-1]
    #     cv2.circle(canvas, tuple(point), 9, pt_color, -1)
    #     print(f'point number {i} is {point} with color {color_label}')

    # polyfill a polygon with a purple color
    cv2.fillPoly(canvas, np.array([polyfill_points]), color)

    max_bounding_box = (star_points['middle_left'][0],  # leftmost point
                        star_points['top_center'][1],  # highest point
                        star_points['middle_right'][0],  # rightmost point
                        star_points['bottom_right'][1])  # lowest point
    return canvas, max_bounding_box


def show_image(image, window_name='image'):
    """
    Show an image
    """
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def generate_shape_size(shape: str):
    """
    Generate a random shape size
    """

    if shape not in all_shapes:
        raise ValueError('shape must be one of: {}'.format(all_shapes))

    w = np.random.randint(64, 128)
    # 1:1 ratio
    if shape in {'circle', 'square', 'star'}:
        return w, w
    # 1:2 ratio
    elif shape in {'rectangle', 'ellipse'}:
        return w * 2, w

    h = np.random.randint(64, 128)
    if shape in {'line', 'arrow', 'triangle'}:
        return w, h


def generate_shape_center(canvas_size: Tuple[int, int], shape_size: Tuple[int, int], canvas_padding: int = 20):
    """
    Generate a random shape center within the canvas with padding
    """
    w, h = canvas_size[0], canvas_size[1]
    w_min = canvas_padding
    w_max = w - canvas_padding
    h_min = canvas_padding
    h_max = h - canvas_padding
    shape_w, shape_h = shape_size
    x = np.random.randint(w_min, w_max - shape_w)
    y = np.random.randint(h_min, h_max - shape_h)
    return x, y


def make_dir_if_not_exist(path: str):
    """
    Create a directory if it doesn't exist
    """
    if not os.path.exists(path):
        os.makedirs(path)


def generate_images(canvas_size: Tuple[int, int], colors_to_use: List[str], generated_images_folder: str,
                    number_of_images_per_shape: int = 15, draw_bounding_box=False):
    """
    Generate images of size canvas_size using the colors defined in colors_to_use and saving to generated_images_folder
    """
    canvas_color_key = colors_to_use[0]
    canvas_color = convert_hex_color_to_rgb(colors[canvas_color_key])
    background_color_key = colors_to_use[1]
    background_color = convert_hex_color_to_rgb(colors[background_color_key])
    bounding_box_key = colors_to_use[2]
    bounding_box_color = convert_hex_color_to_rgb(colors[bounding_box_key])

    # parent directory for all the generated images with this canvas color
    generated_images_dir = os.path.join(generated_images_folder, canvas_color_key)
    make_dir_if_not_exist(generated_images_dir)

    for shape in all_shapes:
        for i in range(number_of_images_per_shape):
            canvas = create_blank_canvas(canvas_size, canvas_color)
            shape_size = generate_shape_size(shape)
            shape_center = generate_shape_center(canvas_size, shape_size)

            print(f'Drawing {shape} with color {background_color_key}')
            canvas, max_bounding_box = add_shape_to_canvas(
                canvas, shape, shape_center=shape_center, shape_size=shape_size, color=background_color, stroke_width=4,
                draw_bounding_box=draw_bounding_box, bounding_box_color=bounding_box_color)

            # save the canvas
            generated_image_file = f'{shape}_{background_color_key}_{i}'
            # save jpg
            cv2.imwrite(os.path.join(generated_images_dir, f'{generated_image_file}.jpg'), canvas)
            # save the max bounding box in the darknet format
            # <object-class> <x_center> <y_center> <width> <height>
            with open(os.path.join(generated_images_dir, f'{generated_image_file}.txt'), 'w') as f:
                object_class = shape_to_index[shape]
                x_center = max_bounding_box[0] + shape_size[0] / 2
                # Convert x_center to be relative to the canvas
                x_center = x_center / canvas_size[0]

                y_center = max_bounding_box[1] + shape_size[1] / 2
                # Convert y_center to be relative to the canvas
                y_center = y_center / canvas_size[1]

                width = max_bounding_box[2] - max_bounding_box[0]
                # Convert width to be relative to the canvas
                width = width / canvas_size[0]

                height = max_bounding_box[3] - max_bounding_box[1]
                # Convert height to be relative to the canvas
                height = height / canvas_size[1]

                f.write(f'{object_class} {x_center} {y_center} {width} {height}')
            print(f'Saved {generated_image_file} files to {generated_images_dir}')


def draw_all_canvas_and_shapes(canvas_size: Tuple[int, int] = (640, 480)):
    """
    Draw all the shapes on the canvas mainly used for debugging
    """
    # create folder to save the generated images
    generated_images_folder = os.path.join('all_shapes')
    make_dir_if_not_exist(generated_images_folder)

    colors_to_manipulate = list(colors.keys())

    # take the first three colors to draw the shapes
    colors_to_use = colors_to_manipulate[:3]
    generate_images(canvas_size, colors_to_use, generated_images_folder, 1, draw_bounding_box=True)


def generate_training_images(canvas_size: Tuple[int, int] = (640, 480)):
    """
    Generate training images with the size of canvas_size
    :param canvas_size: The size of the images we will generate
    """
    neural_network_name = 'shapes_neural_network'
    number_of_iterations = 1
    number_of_images_per_shape = 1

    # define our folder we will work in
    network_folder = os.path.abspath(neural_network_name)
    # make sure the folder exists
    make_dir_if_not_exist(network_folder)

    # create folder to save the generated images
    generated_images_folder = os.path.join(network_folder, 'generated_images')
    make_dir_if_not_exist(generated_images_folder)

    # create names file
    names_path = os.path.join(network_folder, f'{neural_network_name}.names')
    # write shapes to file
    with open(names_path, 'w') as f:
        f.writelines(f'{shape}\n' for shape in all_shapes)

    colors_to_manipulate = list(colors.keys())

    for _ in range(number_of_iterations):
        colors_to_use = random.sample(colors_to_manipulate, 3)
        generate_images(canvas_size, colors_to_use, generated_images_folder, number_of_images_per_shape)


if __name__ == "__main__":
    draw_all_canvas_and_shapes()
    # generate_training_images()
