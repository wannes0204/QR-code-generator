import qrcode
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np


def generate_dot_locations(data:str):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
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




data_to_encode = "https://youtu.be/dQw4w9WgXcQ"
logo_path = "rick-rolling.gif"

circle_radius = 5
cell_radius = 15

background_color = "rgb(237,229,253)"
qr_color = "rgb(51,47,49)"

border_fraction = 0.12
logo_fraction = 1
save_name = "rick_roll_qr.gif"
show_result = True


dot_locations = generate_dot_locations(data_to_encode)
small_square_location = find_small_square(dot_locations)
big_square_locations = [(0, 0), (dot_locations.shape[0]-7, 0), (0, dot_locations.shape[1]-7)]

width, height = dot_locations.shape[1] * (2*cell_radius), dot_locations.shape[0] * (2*cell_radius)



with Image.open(logo_path) as gif:
    print(gif.info['duration'])
    frames = []
    for frame_number in range(gif.n_frames):
        gif.seek(frame_number)
        current_frame = gif.copy().convert("RGBA").resize((int(width*logo_fraction), int(height*logo_fraction)))

        image_result = Image.new("RGBA", (int((2*border_fraction+1)*width), int((2*border_fraction+1)*height)), background_color)
        image_result.paste(current_frame, (int((border_fraction+0.5-0.5*logo_fraction)*width), int((border_fraction+0.5-0.5*logo_fraction)*width)), current_frame)
        draw = ImageDraw.Draw(image_result)

        draw_dots(draw, cell_radius, circle_radius, width, background_color, qr_color)
        draw_squares(draw, qr_color, background_color, cell_radius, big_square_locations, small_square_location)
        frames.append(image_result.copy())

    if save_name:
        frames[0].save(
            save_name,
            save_all=True,
            append_images=frames[1:],
            duration=gif.info['duration'],
            loop=gif.info['loop'],
        )