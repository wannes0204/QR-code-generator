"""Generate QR codes that sit over a logo image."""

from __future__ import annotations

import os
from typing import Iterable, Sequence

import numpy as np
import qrcode
from PIL import Image, ImageDraw

FINDER_PATTERN = (
    (True, True, True, True, True),
    (True, False, False, False, True),
    (True, False, True, False, True),
    (True, False, False, False, True),
    (True, True, True, True, True),
)


def generate_dot_locations(data: str) -> np.ndarray:
    """Create the QR dot grid for a string payload."""
    qr = qrcode.QRCode(
        error_correction=qrcode.ERROR_CORRECT_M,
        box_size=1,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    return ~np.array(qr_image).astype(bool)


def find_small_square(dot_locations: np.ndarray) -> tuple[int, int] | None:
    """Return the top-left position of the small finder pattern."""
    for row in range(dot_locations.shape[0] - 4):
        for col in range(dot_locations.shape[1] - 4):
            window = dot_locations[row : row + 5, col : col + 5]
            if (window == FINDER_PATTERN).all():
                return row, col
    return None


def draw_dots(
    draw: ImageDraw.ImageDraw,
    dot_locations: np.ndarray,
    *,
    cell_radius: int,
    circle_radius: int,
    background_color: tuple[int, int, int],
    qr_color: tuple[int, int, int],
    border_fraction: float,
    width: int,
) -> None:
    """Draw each QR dot as a filled circle."""
    border_offset = int(border_fraction * width)

    for row_index in range(dot_locations.shape[0]):
        for col_index in range(dot_locations.shape[1]):
            circle_center = (
                col_index * 2 * cell_radius + cell_radius + border_offset,
                row_index * 2 * cell_radius + cell_radius + border_offset,
            )
            fill = qr_color if dot_locations[row_index, col_index] else background_color
            draw.ellipse(
                (
                    circle_center[0] - circle_radius,
                    circle_center[1] - circle_radius,
                    circle_center[0] + circle_radius,
                    circle_center[1] + circle_radius,
                ),
                fill=fill,
                outline=None,
            )


def _draw_finder_square(
    draw: ImageDraw.ImageDraw,
    origin: tuple[int, int],
    *,
    cell_radius: int,
    square_color: tuple[int, int, int],
    background_color: tuple[int, int, int],
    border_offset: int,
) -> None:
    """Draw one finder-square pattern in alternating color bands."""
    origin_x, origin_y = origin
    base_x = origin_x * 2 * cell_radius + border_offset
    base_y = origin_y * 2 * cell_radius + border_offset

    layers: Sequence[tuple[float, float, tuple[int, int, int]]] = (
        (-2.0, 16.0, background_color),
        (0.0, 14.0, square_color),
        (2.0, 12.0, background_color),
        (4.0, 10.0, square_color),
    )

    for left_offset, right_offset, fill_color in layers:
        draw.rounded_rectangle(
            (
                base_x + left_offset * cell_radius,
                base_y + left_offset * cell_radius,
                base_x + right_offset * cell_radius,
                base_y + right_offset * cell_radius,
            ),
            fill=fill_color,
            outline=None,
            radius=cell_radius * 2,
        )


def draw_finder_squares(
    draw: ImageDraw.ImageDraw,
    *,
    cell_radius: int,
    square_color: tuple[int, int, int],
    background_color: tuple[int, int, int],
    bigger_squares: Iterable[tuple[int, int]],
    small_square: tuple[int, int] | None,
    border_fraction: float,
    width: int,
) -> None:
    """Draw the three large finder squares and the small one."""
    border_offset = int(border_fraction * width)

    for top_left in bigger_squares:
        _draw_finder_square(
            draw,
            top_left,
            cell_radius=cell_radius,
            square_color=square_color,
            background_color=background_color,
            border_offset=border_offset,
        )

    if small_square is not None:
        _draw_finder_square(
            draw,
            small_square,
            cell_radius=cell_radius,
            square_color=square_color,
            background_color=background_color,
            border_offset=border_offset,
        )


def _apply_logo_color(logo_image: Image.Image, qr_color: tuple[int, int, int]) -> Image.Image:
    """Replace the opaque parts of a logo with the QR color while preserving alpha."""
    image_array = np.array(logo_image.convert("RGBA"))
    alpha_mask = image_array[:, :, 3] > 0
    image_array[alpha_mask, :3] = qr_color
    return Image.fromarray(image_array)


def generate_many_ttc_qrs() -> None:
    """Generate a matrix of QR logo variants for experimentation."""
    logo_name = "payconiq"
    data_map = {
        "payconiq": "https://payconiq.com/MERCHANT/1/6308CFDC7E89415BD1893307",
        "website": "https://ttckruibeke.info/",
        "instagram": "https://www.instagram.com/ttc_kruibeke/",
        "facebook": "https://www.facebook.com/profile.php?id=61556584527983",
    }

    image_sizes = [600, 900, 1200, 1600]
    dot_sizes = [0.4, 0.5, 0.6, 0.7]
    background_colors = [(255, 255, 255), (255, 255, 255), (251, 252, 248)]
    qr_colors = [(0, 0, 0), (18, 20, 23), (100, 170, 137), (44, 56, 48), (64, 85, 71)]

    border_fraction = 0.15
    logo_fraction = 0.85
    logo_path = os.path.join("Input", f"{logo_name}.png")

    for data_name, data_value in [("payconiq", data_map["payconiq"])]:
        for image_size in image_sizes:
            for dot_size in dot_sizes:
                for background_color in background_colors:
                    for qr_color in qr_colors:
                        output_path = os.path.join(
                            "Output",
                            "TTC Kruibeke",
                            data_name,
                            f"resolutie_{image_size}",
                            f"dotsize_{dot_size}",
                            f"{logo_name}_logofrac{logo_fraction}_borderfrac{border_fraction}_color{qr_color}_background{background_color}.png",
                        )
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)

                        qr_over_logo(
                            data=data_value,
                            logo_path=logo_path,
                            output_path=output_path,
                            qr_color=qr_color,
                            background_color=background_color,
                            dot_size=dot_size,
                            border_fraction=border_fraction,
                            logo_fraction=logo_fraction,
                            image_size=image_size,
                        )


def qr_over_logo(
    data: str,
    logo_path: str,
    output_path: str,
    qr_color: tuple[int, int, int],
    background_color: tuple[int, int, int],
    dot_size: float = 0.8,
    border_fraction: float = 0,
    logo_fraction: float = 1,
    image_size: int = 1200,
) -> Image.Image:
    """Create one QR code image layered over a logo.

    The image_size parameter is the target width in pixels for the QR code itself,
    not a multiplier for the cell radius.
    """
    dot_locations = generate_dot_locations(data)

    module_count = dot_locations.shape[1]
    cell_step = max(1, image_size / module_count)
    cell_radius = cell_step / 2
    circle_radius = max(1, int(cell_radius * dot_size))
    small_square_location = find_small_square(dot_locations)
    big_square_locations = [(0, 0), (dot_locations.shape[0] - 7, 0), (0, dot_locations.shape[1] - 7)]

    width = int(module_count * cell_step)
    height = int(dot_locations.shape[0] * cell_step)
    image_result = Image.new(
        "RGBA",
        (int((2 * border_fraction + 1) * width), int((2 * border_fraction + 1) * height)),
        (*background_color, 255),
    )

    logo_size = (int(width * logo_fraction), int(height * logo_fraction))
    with Image.open(logo_path) as logo_image:
        resized_logo = logo_image.resize(logo_size)
        logo_overlay = _apply_logo_color(resized_logo, qr_color)

        logo_position = (
            int((border_fraction + 0.5 - 0.5 * logo_fraction) * width),
            int((border_fraction + 0.5 - 0.5 * logo_fraction) * height),
        )
        image_result.paste(logo_overlay, logo_position, logo_overlay)

    draw = ImageDraw.Draw(image_result)
    draw_dots(
        draw,
        dot_locations,
        cell_radius=cell_radius,
        circle_radius=circle_radius,
        background_color=background_color,
        qr_color=qr_color,
        border_fraction=border_fraction,
        width=width,
    )
    draw_finder_squares(
        draw,
        cell_radius=cell_radius,
        square_color=qr_color,
        background_color=background_color,
        bigger_squares=big_square_locations,
        small_square=small_square_location,
        border_fraction=border_fraction,
        width=width,
    )

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    image_result.save(output_path)
    return image_result

