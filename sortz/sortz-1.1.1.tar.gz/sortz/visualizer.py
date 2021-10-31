import pygame
from random import randint
from .bar import Bar
from .display import Display, COLORS

class Visualizer:
    """
    Pygame based GUI for visualizing sorting algorithms.
    """

    def __init__(self, sorter, fps, font_size):
        """
        Initialize the GUI.

        Parameters
        ----------
        sorter : {"Name" : str, "TimeComplexity" : str,
                  "Description" : str, "Generator" : generator}
            A dictionary describing the sorting algorithm to be visualized.
        fps : int
            The framerate of the visualizer
        """

        # Initialize pygame and create the screen window
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        # Create list of bars as (Surface, Rect) tuples
        self.bars = []
        for _ in range(100):
            surf = pygame.Surface((8, randint(10, 600)))
            rect = surf.get_rect()
            self.bars.append(Bar(surf, rect))
        
        # Color screen and rectangles
        self.screen.fill(COLORS['black'])
        for bar in self.bars:
            bar.surf.fill(COLORS['white'])

        # Set initial position of bars on screen
        self.xcoords = []
        screen_height = self.screen.get_rect().height
        for i, bar in enumerate(self.bars):
            bar.rect.bottom = screen_height
            bar.rect.left = 8 * i
            self.xcoords.append(8 * i)

        # Initialize the sorter generator
        self.fps = fps
        self.sorter = sorter
        self.step = 1
        self.sort = self.sorter["Generator"](self.bars)
        self.is_sorted = False
        self.is_paused = True

        # Set up displays
        self.state_display = Display(font_size, {"Framerate" : self.fps,
                                                 "Step #" : self.step,
                                                 "Play/Pause" : "<space>"})
        self.pause_display = Display(font_size,
                                     {"Sorting Algorithm" : self.sorter["Name"],
                                      "Time Complexity" : self.sorter["TimeComplexity"],
                                      "Description" : self.sorter["Description"]},
                                     "green")

    def main_loop(self):
        while True:
            self._handle_input()
            self._update()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Sorting Visualizer")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.is_paused = not self.is_paused
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if self.fps == 240:
                    self.fps = 240
                elif self.fps == 1:
                    self.fps += 9
                else:
                    self.fps += 10
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if self.fps == 10:
                    self.fps -= 9
                elif self.fps == 1:
                    self.fps = 1
                else:
                    self.fps -= 10

    def _update(self):
        # Sort and update position if needed
        if not self.is_sorted and not self.is_paused:
            self.is_sorted, self.step = next(self.sort)

            for bar, xcoord in zip(self.bars, self.xcoords):
                bar.rect.left = xcoord

        # Update display text
        self.state_display.update({"Framerate" : self.fps,
                                   "Step #" : self.step,
                                   "Play/Pause" : "<space>"})

    def _draw(self):
        # Draw rects
        self.screen.fill(COLORS['black'])
        for surf, rect in self.bars:
            self.screen.blit(surf, rect)

        # Draw display
        self.screen.blit(self.state_display.surface, (0, 0))
        if self.is_paused:
            x, y = self.screen.get_size()
            dx, dy = self.pause_display.surface.get_size()
            position = (0.5 * (x - dx), 0.5 * (y - dy))
            self.screen.blit(self.pause_display.surface, position)

        # Maintain framerate
        self.clock.tick(self.fps)

        pygame.display.flip()
