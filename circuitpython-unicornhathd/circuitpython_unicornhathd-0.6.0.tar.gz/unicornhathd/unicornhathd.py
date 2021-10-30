# SPDX-FileCopyrightText: Copyright (c) 2021 Nathan Young
#
# SPDX-License-Identifier: MIT
"""
`unicornhathd`
================================================================================

CircuitPython framebuf based driver for Pimoroni's Unicorn HAT HD


* Author(s): Nathan Young

Implementation Notes
--------------------

**Hardware:**

* `Pimoroni's Unicorn HAT HD <https://shop.pimoroni.com/products/unicorn-hat-hd>`

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's framebuf library: https://github.com/adafruit/Adafruit_CircuitPython_framebuf
"""

# imports__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/NathanY3G/CircuitPython_Unicorn_HAT_HD.git"

from micropython import const
from adafruit_framebuf import FrameBuffer, RGB888

try:
    # Only used for type hints
    import busio
    import digitalio
except ImportError:
    pass


START_OF_FRAME = const(0x72)


class UnicornHATHD:
    def __init__(
        self,
        spi: busio.SPI,
        chip_select_pin: digitalio.DigitalInOut,
        frequency: int = 5_000_000,
    ):
        self._spi = spi
        self._frequency = frequency
        self._chip_select_pin = chip_select_pin
        self._frame_buffer = FrameBuffer(
            bytearray(self.width * self.height * 3), self.width, self.height, RGB888
        )

    @property
    def width(self) -> int:
        return 16

    @property
    def height(self) -> int:
        return 16

    @property
    def depth(self) -> int:
        return 8

    @property
    def rotation(self) -> int:
        return self._frame_buffer.rotation

    @rotation.setter
    def rotation(self, val: int) -> None:
        self._frame_buffer.rotation = val

    def fill(self, color: int) -> None:
        """Fill the entire display with the specified color."""
        self._frame_buffer.fill(color)

    def fill_rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        """Draw a rectangle at the given location, size and color. It draws both the outline and interior."""
        self._frame_buffer.fill_rect(x, y, width, height, color)

    def pixel(self, x: int, y: int, color: int = None) -> None:
        """Set the specified pixel to the given color."""
        self._frame_buffer.pixel(x, y, color)

    def hline(self, x: int, y: int, width: int, color: int) -> None:
        """Draw a horizontal line up to a given length."""
        self._frame_buffer.hline(x, y, width, color)

    def vline(self, x: int, y: int, height: int, color: int) -> None:
        """Draw a vertical line up to a given length."""
        self._frame_buffer.vline(x, y, height, color)

    def line(self, x_0: int, y_0: int, x_1: int, y_1: int, color: int) -> None:
        """Bresenham's line algorithm"""
        self._frame_buffer.line(x_0, y_0, x_1, y_1, color)

    def circle(self, center_x: int, center_y: int, radius: int, color: int) -> None:
        """Draw a circle at the given midpoint location, radius and color. It draws a 1 pixel outline."""
        self._frame_buffer.circle(center_x, center_y, radius, color)

    def rect(
        self, x: int, y: int, width: int, height: int, color: int, *, fill: bool = False
    ) -> None:
        """Draw a rectangle at the given location, size and color. It draws a 1 pixel outline."""
        self._frame_buffer.rect(x, y, width, height, color, fill=fill)

    def text(
        self,
        string: str,
        x: int,
        y: int,
        color: int,
        *,
        font_name: str = "font5x8.bin",
        size: int = 1,
    ) -> None:
        """Place text on the screen in variables sizes. Breaks on \n to next line. Does not break on line going off screen."""
        self._frame_buffer.text(string, x, y, color, font_name=font_name, size=size)

    def image(self, img) -> None:
        """Set buffer to value of Python Imaging Library image. The image should be in 1 bit mode and a size equal to the display size."""
        self._frame_buffer.image(img)

    def scroll(self, delta_x: int, delta_y: int) -> None:
        """Shifts display in x and y direction"""
        self._frame_buffer.scroll(delta_x, delta_y)

    def show(self) -> None:
        """Update the display"""
        while not self._spi.try_lock():
            pass

        self._spi.configure(baudrate=self._frequency, phase=0, polarity=0)

        self._chip_select_pin.value = False

        self._spi.write(bytearray([START_OF_FRAME]))
        self._spi.write(self._frame_buffer.buf)

        self._chip_select_pin.value = True

        self._spi.unlock()
