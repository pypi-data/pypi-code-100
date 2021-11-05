from dataclasses import make_dataclass
import random
from argparse import ArgumentParser

from colour import Color, COLOR_NAME_TO_RGB
from rich.repr import T
from gradient_figlet import print_with_gradient
from pyfiglet import Figlet, FigletFont, figlet_format

from .pleasing_items import good_gradients, good_fonts

parser = ArgumentParser()
parser.add_argument("text", help="The text to print")
parser.add_argument("-c", "--color", help="The colors for the gradient (comma seperated)")
parser.add_argument("-f", "--font", help="The font for the figlet", default=random.choice(good_fonts))
parser.add_argument("-F", "--all-fonts", help="Shows all the available fonts", action="store_true")
parser.add_argument("-p", "--pager", help="Whether to use a pager or not", action="store_true")
args = parser.parse_args()

if args.all_fonts:
    from rich.console import Console
    from rich.columns import Columns
    from rich.panel import Panel
    from rich.text import Text
    from rich.box import ASCII, ROUNDED
    from rich.progress import track
    from rich.markdown import Markdown

    console = Console()
    all_fonts = FigletFont.getFonts()
    num_of_fonts = len(all_fonts)
    colors1 = map(Color, random.choices(list(map(lambda i: i[0], good_gradients.values())), k=num_of_fonts))
    colors2 = map(Color, random.choices(list(map(lambda i: i[1], good_gradients.values())), k=num_of_fonts))

    items = []
    for font, color1, color2 in track(
        zip(all_fonts, colors1, colors2), total=num_of_fonts, description="Formatting fonts", transient=True
    ):
        figlet_text = figlet_format(args.text or "Test", font)
        text = Text()
        lines = figlet_text.splitlines()
        try:
            gradient_colors = list(color1.range_to(color2, len(lines)))
        except ValueError:
            continue
        for c, l in zip(gradient_colors, lines):
            text.append(l + "\n", style=c.hex_l)
        items.append(
            Panel(
                text,
                box=ASCII if args.pager else ROUNDED,
                title=font,
                subtitle=f"[white on {color1.hex_l}]{color1.hex_l}[/] -> [white on {color2.hex_l}]{color2.hex_l}[/]",
            )
        )
    print("\n")
    if args.pager:
        with console.pager():
            console.print(Columns(items))
    else:
        console.print(Columns(items))
    print("\n")
    if console.is_terminal and not args.pager:
        console.print(
            Markdown(
                "**Note:** Consider piping the output to a file or using a pager (`--pager`) for a better viewing experience "
            )
        )
    exit(0)

# The default colors are cyan to green
default_colors = [Color("cyan"), Color("green")]
colors = [Color(h) for h in args.color.split(",")] if args.color else default_colors
f = Figlet(font=args.font)

print_with_gradient(f.renderText(args.text), *colors)
print(f"Font Used: {args.font}")
