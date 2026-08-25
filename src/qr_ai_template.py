"""
Draws very simple QR codes that can be used for AI image generation.
"""

import qrcode
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_dot_locations(data:str):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        #error_correction=qrcode.constants.ERROR_CORRECT_H,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return ~np.array(img).astype(bool)

def find_small_square(dot_locations: np.ndarray):
    # Look for smaller square
    target_square = [[True, True, True, True, True],
                     [True, False, False, False, True],
                     [True, False, True, False, True],
                     [True, False, False, False, True],
                     [True, True, True, True, True]]
    for i in range(dot_locations.shape[0]-4):
        for j in range(dot_locations.shape[1]-4):
            smaller_square = dot_locations[i:i+5, j:j+5]
            if (smaller_square == target_square).all():
                top_corner = (i, j)
                return top_corner

def draw_dots(draw:ImageDraw, cell_radius:int, circle_radius:int, size:int, background_color, qr_color):
    for i in range(dot_locations.shape[0]):
        for j in range(dot_locations.shape[1]):
            # Calculate circle center
            circle_center = (j * 2 * cell_radius + cell_radius + int(border_fraction*width), i * 2 * cell_radius + cell_radius + int(border_fraction*width))

            # Draw circle on the image
            draw.ellipse(
                (
                    circle_center[0] - circle_radius,
                    circle_center[1] - circle_radius,
                    circle_center[0] + circle_radius,
                    circle_center[1] + circle_radius,
                ),
                fill=qr_color if dot_locations[i, j] else background_color,
                outline=None,
            )

def draw_squares(draw, square_color, background_color, cell_radius, big_square_locations, small_square_location):
    # big squares
    for left_up_corner in big_square_locations:
        draw.rounded_rectangle(
            (
                left_up_corner[0] * 2 * cell_radius - 2*cell_radius + int(border_fraction*width),
                left_up_corner[1] * 2 * cell_radius - 2*cell_radius + int(border_fraction*width),
                left_up_corner[0] * 2 * cell_radius+16*cell_radius + int(border_fraction*width),
                left_up_corner[1] * 2 * cell_radius+16*cell_radius + int(border_fraction*width),
            ),
            fill=background_color,
            outline=None,
            radius=cell_radius*2
        )
        draw.rounded_rectangle(
            (
                left_up_corner[0] * 2 * cell_radius + int(border_fraction*width),
                left_up_corner[1] * 2 * cell_radius + int(border_fraction*width),
                left_up_corner[0] * 2 * cell_radius+14*cell_radius + int(border_fraction*width),
                left_up_corner[1] * 2 * cell_radius+14*cell_radius + int(border_fraction*width),
            ),
            fill=square_color,
            outline=None,
            radius=cell_radius*2
        )
        draw.rounded_rectangle(
            (
                left_up_corner[0] * 2 * cell_radius+2*cell_radius + int(border_fraction*width),
                left_up_corner[1] * 2 * cell_radius+2*cell_radius + int(border_fraction*width),
                left_up_corner[0] * 2 * cell_radius+12*cell_radius + int(border_fraction*width),
                left_up_corner[1] * 2 * cell_radius+12*cell_radius + int(border_fraction*width),
            ),
            fill=background_color,
            outline=None,
            radius=cell_radius*2
        )
        draw.rounded_rectangle(
            (
                left_up_corner[0] * 2 * cell_radius+4*cell_radius + int(border_fraction*width),
                left_up_corner[1] * 2 * cell_radius+4*cell_radius + int(border_fraction*width),
                left_up_corner[0] * 2 * cell_radius+10*cell_radius + int(border_fraction*width),
                left_up_corner[1] * 2 * cell_radius+10*cell_radius + int(border_fraction*width),
            ),
            fill=square_color,
            outline=None,
            radius=cell_radius*2
        )
    # small squre
    draw.rounded_rectangle(
        (
            small_square_location[0] * 2 * cell_radius + int(border_fraction*width),
            small_square_location[1] * 2 * cell_radius + int(border_fraction*width),
            small_square_location[0] * 2 * cell_radius + 10*cell_radius + int(border_fraction*width),
            small_square_location[1] * 2 * cell_radius + 10*cell_radius + int(border_fraction*width),
        ),
        fill=square_color,
        outline=None,
        radius=cell_radius*2
    )
    draw.rounded_rectangle(
        (
            small_square_location[0] * 2 * cell_radius + 2*cell_radius + int(border_fraction*width),
            small_square_location[1] * 2 * cell_radius + 2*cell_radius + int(border_fraction*width),
            small_square_location[0] * 2 * cell_radius + 8*cell_radius + int(border_fraction*width),
            small_square_location[1] * 2 * cell_radius + 8*cell_radius + int(border_fraction*width),
        ),
        fill=background_color,
        outline=None,
        radius=cell_radius*2
    )
    draw.rounded_rectangle(
        (
            small_square_location[0] * 2 * cell_radius + 4*cell_radius + int(border_fraction*width),
            small_square_location[1] * 2 * cell_radius + 4*cell_radius + int(border_fraction*width),
            small_square_location[0] * 2 * cell_radius + 6*cell_radius + int(border_fraction*width),
            small_square_location[1] * 2 * cell_radius + 6*cell_radius + int(border_fraction*width),
        ),
        fill=square_color,
        outline=None,
        radius=cell_radius*2
    )


data_link = "https://ttckruibeke.info/"

border_fraction = 0.1

image_size = 3
dot_size = 0.1

show_result = False
save = True


background_color = "rgb(255, 255, 255)"

qr_color = "rgb(0, 0, 0)"


cell_radius = 10 * image_size
circle_radius = int(cell_radius * dot_size)

if save:
    save_path = os.path.join("Output")
    os.makedirs(save_path, exist_ok=True)
    save_name = os.path.join(save_path, "ai_template.png")

dot_locations = generate_dot_locations(data_link)

small_square_location = find_small_square(dot_locations)
big_square_locations = [(0, 0), (dot_locations.shape[0]-7, 0), (0, dot_locations.shape[1]-7)]

width, height = dot_locations.shape[1] * (2*cell_radius), dot_locations.shape[0] * (2*cell_radius)
image_result = Image.new("RGBA", (int((2*border_fraction+1)*width), int((2*border_fraction+1)*height)), "rgba(255, 255, 255, 0)")

draw = ImageDraw.Draw(image_result)

draw_dots(draw, cell_radius, circle_radius, width, background_color, qr_color)
draw_squares(draw, qr_color, background_color, cell_radius, big_square_locations, small_square_location)

if save:
    image_result.save(save_name)
if show_result:
    image_result.show()
