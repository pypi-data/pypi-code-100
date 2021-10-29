import os
from pathlib import Path

import click
import cv2
from colour import Color
from loguru import logger

from monochromist.opencv_version.post_editing import color_image, crop_borders

from .classes import Settings
from .find_mask import find_mask


@click.command()
@click.option("-i", "--input", type=Path, required=True, help="Input filepath")
@click.option("-o", "--output", type=Path, required=True, help="Output filepath")
@click.option(
    "-l",
    "--lower",
    type=int,
    help="Lower threshold for Candy Edge detection",
    default=100,
    show_default=True,
)
@click.option(
    "-u",
    "--upper",
    type=int,
    help="Lower threshold for Candy Edge detection",
    default=200,
    show_default=True,
)
@click.option(
    "-c",
    "--color",
    type=str,
    help="Color of result contour",
    default="black",
    show_default=True,
)
@click.option(
    "-p",
    "--crop",
    type=bool,
    help="Crop transparent pixels after converting",
    default=True,
    show_default=True,
)
def process(input: Path, output: Path, lower: int, upper: float, color: Color, crop: bool) -> None:
    """Take contour from selected file"""

    parsed_color = Color(color)

    settings = Settings(
        in_file=input,
        out_file=output,
        lower=lower,
        upper=upper,
        color=parsed_color,
        crop=crop,
    )

    initial_image = cv2.imread(str(input), cv2.IMREAD_GRAYSCALE)

    mask = find_mask(initial_image, settings)

    cropped = mask
    if settings.crop:
        cropped = crop_borders(mask)

    colored = color_image(cropped, settings)

    if os.path.exists(output):
        os.remove(output)
    cv2.imwrite(str(output), colored)

    logger.info(f"{input} --> {output}")


if __name__ == "__main__":
    process()
