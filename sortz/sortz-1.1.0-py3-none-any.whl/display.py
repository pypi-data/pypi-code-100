import pygame

COLORS = {
    'black' : (0, 0, 0),
    'white' : (255, 255, 255),
    'red' : (255, 0, 0),
    'green' : (0, 255, 0),
    'blue' : (0, 0, 255)
}

class Display:
    """
    Text display class for showing text on a pygame.Surface.
    """

    def __init__(self, font_size, elements, color = 'red'):
        """
        Initialize the display.

        Parameters
        ----------
        font_size : int
            Size of font for all text in display
        elements : dict
            Dictionary of key/value pairs describing what is displayed.
        color : str
            Color of text
        """

        self.font = pygame.font.Font(None, font_size)
        self.color = color

        # Set up pygame.Surface objects for each line of display content
        self.elements = {}
        for key, value in elements.items():
            if isinstance(value, (list, tuple)):
                self.elements[key] = [self.font.render(f"{key}:",
                                                       True,
                                                       COLORS[self.color],
                                                       None)]
                for line in value:
                    self.elements[key].append(self.font.render(f"{line}",
                                                              True,
                                                              COLORS[self.color],
                                                              None))
            else:
                self.elements[key] = [self.font.render(f"{key}: {value}",
                                                       True,
                                                       COLORS[self.color],
                                                       None)]

        # Position elements on a parent pygame.Surface
        widths = []
        heights = []
        for element in self.elements.values():
            for line in element:
                widths.append(line.get_width())
                heights.append(line.get_height())
        width = max(widths) + 10
        height = sum(heights)
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect()
        self.draw()

    def draw(self):
        """
        Blit text onto Display surface.
        """

        self.surface.fill(COLORS['black'])
        y = 0
        for element in self.elements.values():
            for line in element:
                self.surface.blit(line, (0, y))
                y += line.get_height()

    def update(self, elements):
        """
        Update the dynamic display content.  The keyword arguments
        must match the elements of the display.
        """

        # Check that the keyword arguments match the elements in
        # the current display.
        if elements.keys() != self.elements.keys():
            raise Exception("Keys must match!")

        for key, value in elements.items():
            self.elements[key] = [self.font.render(f"{key}: {value}",
                                                    True,
                                                    COLORS[self.color],
                                                    None)]
        
        self.draw()
