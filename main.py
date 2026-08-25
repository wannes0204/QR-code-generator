"""
By: De Vleeschouwer Wannes
Email: wannes.devleeschouwer@gmail.com

Created: 25/08/2026 (dd-mm-yyyy)
Last modification: 25/08/2026 (dd-mm-yyyy)

Description: Main file to run the project.
"""

import os

from src.qr_over_logo import qr_over_logo
from src.utils import input_dir, output_dir


def main() -> None:
    qr_over_logo(
        data="https://www.amie-be.org/wat-doen-we/projecten/zoodo",
        logo_path=os.path.join(input_dir, "web2.png"),
        output_path=os.path.join(output_dir, "burkindi_website.png"),
        qr_color=(0, 0, 0),
        background_color=(255, 255, 255),
        dot_size=0.8,
        border_fraction=0,
        logo_fraction=1,
        image_size=1200,
    )


if __name__ == "__main__":
    main()