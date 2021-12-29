"""
Generate a dataset for detecting shapes
"""
import os
import random
from typing import Tuple, List

import cv2
import numpy as np

all_shapes = ['ellipse', 'circle', 'square', 'rectangle', 'line', 'arrow', 'triangle']

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
    height, width = canvas_shape
    canvas = np.zeros((height, width, 3), np.uint8)
    # convert color tuple to BGR
    color = color[::-1]
    canvas[:] = color
    return canvas


def add_shape_to_canvas(canvas, shape: str, shape_center: Tuple[int, int] = (100, 100),
                        shape_size: Tuple[int, int] = (64, 64), color=(0, 0, 0),
                        stroke_width=1, draw_bounding_box=False, bounding_box_color=(0, 0, 0)):
    """
    Add a shape to a canvas with a color and stroke width and fill it with the color
    """
    # for the maximum bounding box of the shape we just drew
    max_bounding_box = (0, 0, 0, 0)

    # convert color tuple to BGR
    color = color[::-1]

    if shape not in all_shapes:
        raise ValueError('shape must be one of: {}'.format(all_shapes))
    if shape == 'circle':
        radius = int(shape_size[0] / 2)
        center = (shape_center[0] + radius, shape_center[1] + radius)
        cv2.circle(canvas, center, radius, color, stroke_width)
        # fill the circle with the color
        cv2.circle(canvas, center, radius, color, -1)

        max_bounding_box = (center[0] - radius, center[1] - radius,
                            center[0] + radius, center[1] + radius)
    elif shape == 'ellipse':
        w, h = shape_size
        center = (int(shape_center[0] + w / 2), int(shape_center[1] + h / 2))
        # fill the ellipse with the color
        cv2.ellipse(canvas, center, (w // 2, h // 2), 0, 0, 360, color, -1)

        max_bounding_box = (center[0] - w / 2, center[1] - h / 2,
                            center[0] + w / 2, center[1] + h / 2)

    elif shape in {'rectangle', 'square'}:
        x1, y1 = shape_center
        x2, y2 = shape_center[0] + shape_size[0], shape_center[1] + shape_size[1]
        canvas = cv2.rectangle(canvas, (x1, y1), (x2, y2), color, stroke_width)
        # Fill the rectangle with the color
        canvas = cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)

        max_bounding_box = (x1, y1, x2, y2)
    elif shape == 'line':
        x1, y1 = shape_center
        x2, y2 = shape_center[0] + shape_size[0], shape_center[1] + shape_size[1]
        canvas = cv2.line(canvas, (x1, y1), (x2, y2), color, stroke_width)

        max_bounding_box = (x1, y1, x2, y2)
    elif shape == 'arrow':
        x1, y1 = shape_center
        x2, y2 = shape_center[0] + shape_size[0], shape_center[1] + shape_size[1]
        canvas = cv2.arrowedLine(
            canvas, (x1, y1), (x2, y2), color, stroke_width)

        max_bounding_box = (x1, y1, x2, y2)
    elif shape == 'triangle':
        x1, y1 = shape_center
        x2, y2 = shape_center[0] + shape_size[0], shape_center[1] + shape_size[1]
        x3, y3 = shape_center[0] + shape_size[0] / 2, shape_center[1] + shape_size[1]
        pts = np.array([[x1, y1], [x2, y2], [x3, y3]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        canvas = cv2.polylines(canvas, [pts], True, color, stroke_width)
        # Fill the triangle with the color
        canvas = cv2.fillPoly(canvas, [pts], color)

        max_bounding_box = (x1, y1, x2, int(max(y2, y3)))

    # Add the stroke width to the max bounding box
    max_bounding_box = (max_bounding_box[0], max_bounding_box[1],
                        max_bounding_box[2] + stroke_width * 3, max_bounding_box[3] + stroke_width * 3)

    # ensure that the max bounding box only contains ints
    max_bounding_box = (int(max_bounding_box[0]), int(max_bounding_box[1]),
                        int(max_bounding_box[2]), int(max_bounding_box[3]))

    if draw_bounding_box:
        # Draw a red bounding box around the shape using the maximum bounding box
        canvas = cv2.rectangle(canvas, (max_bounding_box[0], max_bounding_box[1]), (
            max_bounding_box[2], max_bounding_box[3]), bounding_box_color, 2)
    return canvas, max_bounding_box


def draw_all_canvas_and_shapes(canvas: Tuple[int, int], shapes: List[str], shape_center: Tuple[int, int],
                               shape_size: Tuple[int, int]):
    """
    Draw all the shapes on the canvas
    """
    for shape in shapes:
        canvas, max_bounding_box = add_shape_to_canvas(
            canvas, shape, shape_center, shape_size)
        # show_image(canvas)


def generate_shape_size(shape: str):
    """
    Generate a random shape size
    """
    w = np.random.randint(64, 128)
    # 1:1 ratio
    if shape in {'circle', 'square'}:
        return w, w
    # 1:2 ratio
    elif shape in {'rectangle', 'ellipse'}:
        return w * 2, w

    h = np.random.randint(64, 128)
    if shape in {'line', 'arrow', 'triangle'}:
        return w, h


def generate_shape_center(canvas_size: Tuple[int, int], shape_size: Tuple[int, int], canvas_padding: int = 10):
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


def generate_images(canvas_size: Tuple[int, int], colors_to_use: List[str], generated_images_folder: str):
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

    print(f'Canvas color: {canvas_color_key} {canvas_color}')
    for shape in all_shapes:

        for i in range(15):
            canvas = create_blank_canvas(canvas_size, canvas_color)
            shape_size = generate_shape_size(shape)
            shape_center = generate_shape_center(canvas_size, shape_size)

            print(f'Drawing {shape} with color {background_color_key}')
            canvas, max_bounding_box = add_shape_to_canvas(
                canvas, shape, shape_center=shape_center, shape_size=shape_size, color=background_color, stroke_width=4,
                draw_bounding_box=False, bounding_box_color=bounding_box_color)

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


def generate_training_images(canvas_size: Tuple[int, int] = (640, 480)):
    """
    Generate training images with the size of canvas_size
    :param canvas_size: The size of the images we will generate
    """
    neural_network_name = 'shapes_neural_network'
    number_of_iterations = 50

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
        generate_images(canvas_size, colors_to_use, generated_images_folder)


if __name__ == "__main__":
    generate_training_images()
