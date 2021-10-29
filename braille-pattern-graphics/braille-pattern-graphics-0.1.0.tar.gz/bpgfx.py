# Braille Dot Numbering
# ---------------------
#   1 4
#   2 3
#   3 6
#   7 8
#
# Unicode Braille Patterns Block
# ------------------------------
# https://en.wikipedia.org/wiki/Braille_Patterns
# https://www.unicode.org/charts/PDF/U2800.pdf
#
#        | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F
# U+280x | ⠀ | ⠁ | ⠂ | ⠃ | ⠄ | ⠅ | ⠆ | ⠇ | ⠈ | ⠉ | ⠊ | ⠋ | ⠌ | ⠍ | ⠎ | ⠏
# U+281x | ⠐ | ⠑ | ⠒ | ⠓ | ⠔ | ⠕ | ⠖ | ⠗ | ⠘ | ⠙ | ⠚ | ⠛ | ⠜ | ⠝ | ⠞ | ⠟
# U+282x | ⠠ | ⠡ | ⠢ | ⠣ | ⠤ | ⠥ | ⠦ | ⠧ | ⠨ | ⠩ | ⠪ | ⠫ | ⠬ | ⠭ | ⠮ | ⠯
# U+283x | ⠰ | ⠱ | ⠲ | ⠳ | ⠴ | ⠵ | ⠶ | ⠷ | ⠸ | ⠹ | ⠺ | ⠻ | ⠼ | ⠽ | ⠾ | ⠿
# U+284x | ⡀ | ⡁ | ⡂ | ⡃ | ⡄ | ⡅ | ⡆ | ⡇ | ⡈ | ⡉ | ⡊ | ⡋ | ⡌ | ⡍ | ⡎ | ⡏
# U+285x | ⡐ | ⡑ | ⡒ | ⡓ | ⡔ | ⡕ | ⡖ | ⡗ | ⡘ | ⡙ | ⡚ | ⡛ | ⡜ | ⡝ | ⡞ | ⡟
# U+286x | ⡠ | ⡡ | ⡢ | ⡣ | ⡤ | ⡥ | ⡦ | ⡧ | ⡨ | ⡩ | ⡪ | ⡫ | ⡬ | ⡭ | ⡮ | ⡯
# U+287x | ⡰ | ⡱ | ⡲ | ⡳ | ⡴ | ⡵ | ⡶ | ⡷ | ⡸ | ⡹ | ⡺ | ⡻ | ⡼ | ⡽ | ⡾ | ⡿
# U+288x | ⢀ | ⢁ | ⢂ | ⢃ | ⢄ | ⢅ | ⢆ | ⢇ | ⢈ | ⢉ | ⢊ | ⢋ | ⢌ | ⢍ | ⢎ | ⢏
# U+289x | ⢐ | ⢑ | ⢒ | ⢓ | ⢔ | ⢕ | ⢖ | ⢗ | ⢘ | ⢙ | ⢚ | ⢛ | ⢜ | ⢝ | ⢞ | ⢟
# U+28Ax | ⢠ | ⢡ | ⢢ | ⢣ | ⢤ | ⢥ | ⢦ | ⢧ | ⢨ | ⢩ | ⢪ | ⢫ | ⢬ | ⢭ | ⢮ | ⢯
# U+28Bx | ⢰ | ⢱ | ⢲ | ⢳ | ⢴ | ⢵ | ⢶ | ⢷ | ⢸ | ⢹ | ⢺ | ⢻ | ⢼ | ⢽ | ⢾ | ⢿
# U+28Cx | ⣀ | ⣁ | ⣂ | ⣃ | ⣄ | ⣅ | ⣆ | ⣇ | ⣈ | ⣉ | ⣊ | ⣋ | ⣌ | ⣍ | ⣎ | ⣏
# U+28Dx | ⣐ | ⣑ | ⣒ | ⣓ | ⣔ | ⣕ | ⣖ | ⣗ | ⣘ | ⣙ | ⣚ | ⣛ | ⣜ | ⣝ | ⣞ | ⣟
# U+28Ex | ⣠ | ⣡ | ⣢ | ⣣ | ⣤ | ⣥ | ⣦ | ⣧ | ⣨ | ⣩ | ⣪ | ⣫ | ⣬ | ⣭ | ⣮ | ⣯
# U+28Fx | ⣰ | ⣱ | ⣲ | ⣳ | ⣴ | ⣵ | ⣶ | ⣷ | ⣸ | ⣹ | ⣺ | ⣻ | ⣼ | ⣽ | ⣾ | ⣿

from typing import List, Optional
import math

# ANSI escape sequence for "move cursor home" followed by "clear screen".
# Printing this escape sequence to the terminal will clear the screen and
# reposition the cursor on the top-left of the terminal in terminal emulators
# with support for ANSI escape codes.
CLEAR: str = f"\N{ESCAPE}[H\N{ESCAPE}[2J"


class Canvas:
    """
    Two-dimensional surface of width x height virtual dot-pixels. The canvas
    represents an image using one-bit graphics backed by a two-dimensional
    array of bool where True represents a dot-pixel in the "raised" state and
    False represents a dot-pixel is the "not raised" state.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Create a new width x height canvas object with all virtual dot-pixels
        initially set to the not raised state.
        """
        if width < 0 or height < 0:
            name: str = type(self).__name__
            raise ValueError(f"Invalid {name} size {width} x {height}")
        self._width: int = width
        self._height: int = height
        dots_w = int(math.ceil(width / 2) * 2)
        dots_h = int(math.ceil(height / 4) * 4)
        self._dots: List[List[bool]] = [
            [False for _ in range(dots_w)] for _ in range(dots_h)
        ]

    @property
    def width(self) -> int:
        """
        Width of the canvas.
        """
        return self._width

    @property
    def height(self) -> int:
        """
        Height of the canvas.
        """
        return self._height

    def get(self, x: int, y: int) -> bool:
        """
        Get the state of the dot-pixel at the provided (x, y) position.
        Attempting to retrieve a dot-pixel outside of the canvas bounds will
        always return not raised (False).

        Returns True if the dot-pixel is raised (pixel on) or False if the
        dot-pixel is not raised (pixel off).
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            # off-canvas
            return False
        return self._dots[y][x]

    def set(self, x: int, y: int, raised: bool = True) -> None:
        """
        Set the state of the dot-pixel at the provided (x, y) position to
        raised (True) or not raised (False).
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            # off-canvas
            return
        self._dots[y][x] = raised

    def clear(self, raised: bool = False) -> None:
        """
        Set all pixels on the canvas to the provided state (default not
        raised).
        """
        for y in range(self.height):
            for x in range(self.width):
                self._dots[y][x] = raised

    def draw(self, drawable) -> None:
        """
        Invoke the provided object's draw method passing self as the canvas
        parameter. Any object that implements the draw method:
            obj.draw(canvas)
        is considered "drawable".
        """
        drawable.draw(self)

    def __repr__(self) -> str:
        """
        Returns repr(self).
        """
        name: str = type(self).__name__
        dots: str = repr(self._dots)
        return f"{name}({self.width} x {self.height}, {dots})"

    def __str__(self) -> str:
        """
        Returns str(self).

        The function call:
            str(canvas)
        will encode the virtual dot-pixels of the canvas as a string of braille
        pattern characters suitable for "rendering" to a terminal or text field
        with a monospace font.

        Example:
            canvas = Canvas(9, 9)
            for y in range(canvas.height):
                for x in range(canvas.width):
                    canvas.set(x, y, x % 2 == y % 2)
            print(canvas, end="")

            ⢕⢕⢕⢕⠅
            ⢕⢕⢕⢕⠅
            ⠁⠁⠁⠁⠁
        """
        s = ""
        for y in range(0, self.height, 4):
            for x in range(0, self.width, 2):
                bits = 0b00000000
                if self._dots[y + 0][x + 0]:
                    bits |= 0b00000001
                if self._dots[y + 1][x + 0]:
                    bits |= 0b00000010
                if self._dots[y + 2][x + 0]:
                    bits |= 0b00000100
                if self._dots[y + 0][x + 1]:
                    bits |= 0b00001000
                if self._dots[y + 1][x + 1]:
                    bits |= 0b00010000
                if self._dots[y + 2][x + 1]:
                    bits |= 0b00100000
                if self._dots[y + 3][x + 0]:
                    bits |= 0b01000000
                if self._dots[y + 3][x + 1]:
                    bits |= 0b10000000
                s += chr(0x2800 | bits)
            s += "\n"
        return s


class Texture:
    """
    Two-dimensional width x height image of virtual dot-pixels with
    transparency. The texture is backed by a two-dimensional array of
    Optional[bool] where True represents a dot-pixel in the "raised" state,
    False represents a dot-pixel is the "not raised" state, and None represents
    a transparent pixel.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Create a new width x height texture object with all virtual dot-pixels
        initially transparent.
        """
        if width < 0 or height < 0:
            name: str = type(self).__name__
            raise ValueError(f"Invalid {name} size {width} x {height}")
        self._width: int = width
        self._height: int = height
        self._dots: List[List[Optional[bool]]] = [
            [None for _ in range(width)] for _ in range(height)
        ]

    @property
    def width(self) -> int:
        """
        Width of the texture.
        """
        return self._width

    @property
    def height(self) -> int:
        """
        Height of the texture.
        """
        return self._height

    def get(self, x: int, y: int) -> Optional[bool]:
        """
        Get the state of the dot-pixel at the provided (x, y) position.
        Attempting to retrieve a dot-pixel outside of the texture bounds will
        always return transparent (None).

        Returns True if the dot-pixel is raised (pixel on), False if the
        dot-pixel is not raised (pixel off), or None if the dot-pixel is
        transparent.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            # off-texture
            return None
        return self._dots[y][x]

    def set(self, x: int, y: int, value: Optional[bool] = True) -> None:
        """
        Set the state of the dot-pixel at the provided (x, y) position to
        raised (True), not raised (False), or transparent (None).
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            # off-texture
            return
        self._dots[y][x] = value


class Point:
    """
    Point at position (x, y).
    """

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def draw(self, canvas: Canvas) -> None:
        canvas.set(self.x, self.y, True)


class Line:
    """
    Line from position (x1, y1) to position (x2, y2).
    """

    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1: int = x1
        self.y1: int = y1
        self.x2: int = x2
        self.y2: int = y2

    def draw(self, canvas: Canvas) -> None:
        # Optimized line function from the article "Line drawing on a grid"
        # written by Red Blob Games, ported from C#.
        # https://www.redblobgames.com/grids/line-drawing.html
        #
        # The number of steps to take is exactly the diagonal distance between
        # (x1, y1) and (x2, y2).
        dx: int = self.x2 - self.x1
        dy: int = self.y2 - self.y1
        abs_dx: int = abs(dx)
        abs_dy: int = abs(dy)
        nsteps: int = abs_dx if abs_dx > abs_dy else abs_dy
        # Calculate the x and y step distance per step-iteration.
        nsteps_inverse: float = 1.0 / nsteps
        xstep: float = dx * nsteps_inverse
        ystep: float = dy * nsteps_inverse
        # Draw each (x, y) dot from (x1, y1) to (x2, y2). These dots are
        # connected by either an dot edge edge (e.g. ⠆) or a corner between the
        # two dots (e.g. ⠊).
        x: float = float(self.x1)
        y: float = float(self.y1)
        for i in range(nsteps + 1):
            canvas.set(int(round(x)), int(round(y)), True)
            x += xstep
            y += ystep


class Rectangle:
    """
    Axis-aligned rectangle with upper-left corner at position (x, y).
    """

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        if width < 0 or height < 0:
            name: str = type(self).__name__
            raise ValueError(f"Invalid {name} size {width} x {height}")
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

    def draw(self, canvas: Canvas) -> None:
        x1 = self.x
        y1 = self.y
        x2 = x1 + self.width - 1
        y2 = x1 + self.height - 1
        canvas.draw(Line(x1, y1, x2, y1))
        canvas.draw(Line(x1, y2, x2, y2))
        canvas.draw(Line(x1, y1, x1, y2))
        canvas.draw(Line(x2, y1, x2, y2))


class Sprite:
    """
    Axis-aligned texture mapping with upper-left corner at position (x, y).
    """

    def __init__(self, x: int, y: int, texture: Texture) -> None:
        self.x: int = x
        self.y: int = y
        self.texture: Texture = texture

    def draw(self, canvas: Canvas) -> None:
        for y in range(0, self.texture.height):
            for x in range(0, self.texture.width):
                value = self.texture.get(x, y)
                if value is None:
                    # transparent
                    continue
                canvas.set(self.x + x, self.y + y, value)
