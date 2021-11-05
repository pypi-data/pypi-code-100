"Style for prompts"

from questionary import Style

style = Style([
    ('question', 'bg:orange fg:black'),
    ('answer', 'fg:default nobold'),
    ('selected', 'fg:orange'),
])
