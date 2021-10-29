import os
from pathlib import Path

import click
from colour import Color
from loguru import logger
from PIL import Image

from monochromist.math_version.clean import erase
from monochromist.math_version.postprocess import color_and_crop

from .classes import ImageInfo, Settings


@click.command()
@click.option(
    "-i", "--input", type=click.Path(exists=True, dir_okay=False), required=True, help="Input file"
)
@click.option(
    "-o",
    "--output",
    type=click.Path(writable=True, dir_okay=False),
    required=True,
    help="Output file",
)
@click.option(
    "-s",
    "--saving",
    type=click.IntRange(min=0, max=100),
    help="How much pixels to save, from 0 (erase all) to 100 (save all). "
    "If not defined then empirical algorithm will be used",
)
@click.option(
    "-t",
    "--thickness",
    type=int,
    help="Thickness of the line",
    default=3,
    show_default=True,
)
@click.option(
    "-c",
    "--color",
    type=str,
    help="Name of the color or it's HEX code (ex. #CC573E)",
    default="black",
    show_default=True,
)
@click.option(
    "-r",
    "--crop",
    type=bool,
    help="Drop transparent pixels after image processing",
    default=True,
    show_default=True,
)
def process(
    input: Path, output: Path, saving: int, thickness: int, color: Color, crop: bool
) -> None:
    """Take contour from selected file"""

    parsed_color = Color(color)

    settings = Settings(
        thickness=thickness,
        saving=saving,
        color=parsed_color,
        crop=crop,
    )

    process_file(input, output, settings)


def process_file(input: Path, output: Path, settings: Settings) -> ImageInfo:
    """Take contour from selected file"""
    initial_image = Image.open(input)
    new_image, image_info = process_image(initial_image, settings)

    if os.path.exists(output):
        os.remove(output)
    new_image.save(output)

    logger.info(f"Convert <{input}> to <{output}>")
    logger.info(f"Used settings: {image_info.settings}")
    if settings.saving is None:
        logger.info("To better result try to vary saving parameter"
                    "by adding `-s <from 0 to 100>` to the end of the command")
    return image_info


def process_image(initial_image: Image, settings: Settings) -> tuple[Image, ImageInfo]:
    image_info = erase(initial_image, settings)
    new_image = color_and_crop(image_info)
    return new_image, image_info


if __name__ == "__main__":
    process()
