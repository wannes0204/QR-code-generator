import qrcode
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import os

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



logo_path = os.path.join("Input", "instagram_inverse.png")
logo_name = "instagram_inverse"

datas = {"payconiq" : "https://payconiq.com/MERCHANT/1/6308CFDC7E89415BD1893307",
         "website" : "https://ttckruibeke.info/",
         "instagram" : "https://www.instagram.com/ttc_kruibeke/",
         "facebook" : "https://www.facebook.com/profile.php?id=61556584527983"}

image_sizes = [1, 2, 3, 4, 5]
dot_sizes = [0.4, 0.5, 0.6, 0.7]

background_colors = ["rgba(255,255,255,255)", "rgba(255,255,255,0)", "rgba(251,252,248,255)"]
qr_colors = ["rgb(0,0,0)", "rgb(18,20,23)", "rgb(100,170,137)", "rgb(44,56,48)", "rgb(64,85,71)"]

border_fraction = 0.35
logo_franction = 1.4

show_result = True
save = False






showing = False
#for data, data_link in datas.items():
for data, data_link in [("instagram", datas["instagram"])]:
    for image_size in image_sizes:
        for dot_size in dot_sizes:
            for background_color in background_colors:
                for qr_color in qr_colors:
                    cell_radius = 10 * image_size
                    circle_radius = int(cell_radius * dot_size)

                    if save:
                        save_path = os.path.join("Output", "TTC Kruibeke", data, f"resolutie_{image_size}", f"dotsize_{dot_size}")
                        os.makedirs(save_path, exist_ok=True)
                        save_name = os.path.join(save_path, f"{logo_name}_logofrac{logo_franction}_borderfrac{border_fraction}_color{qr_color}_background{background_color}.png")

                    dot_locations = generate_dot_locations(datas[data])

                    small_square_location = find_small_square(dot_locations)
                    big_square_locations = [(0, 0), (dot_locations.shape[0]-7, 0), (0, dot_locations.shape[1]-7)]

                    width, height = dot_locations.shape[1] * (2*cell_radius), dot_locations.shape[0] * (2*cell_radius)
                    image_result = Image.new("RGBA", (int((2*border_fraction+1)*width), int((2*border_fraction+1)*height)), background_color)


                    image_logo = Image.open(logo_path).resize((int(width*logo_franction), int(height*logo_franction)))
                    image_array = np.array(image_logo)

                    if len(image_array.shape) == 2:
                        alpha_channel = image_array
                    elif len(image_array.shape) == 3:
                        if image_array.shape[2] == 4:
                            alpha_channel = image_array[:, :, 3]
                        else:
                            alpha_channel = image_array
                            
                    mask = alpha_channel > 0
                    new_color = np.array([int(color) for color in qr_color.split("(")[1].split(")")[0].split(",")] + [255])
                    image_array[mask] = new_color
                    image_logo = Image.fromarray(image_array)

                    image_result.paste(image_logo, (int((border_fraction+0.5-0.5*logo_franction)*width), int((border_fraction+0.5-0.5*logo_franction)*width)), image_logo)
                    draw = ImageDraw.Draw(image_result)

                    draw_dots(draw, cell_radius, circle_radius, width, background_color, qr_color)
                    draw_squares(draw, qr_color, background_color, cell_radius, big_square_locations, small_square_location)

                    if save:
                        image_result.save(save_name)
                    if show_result:
                        if not showing:
                            showing = True
                            image_result.show()
