import pygame

class Button():
    def __init__(self, x, y, l, w, text, colour):
        self.x = x - int(round(l/2))
        self.y = y - int(round(w/2))
        self.l = l
        self.w = w
        self.text = text
        self.colour = colour
        self.rect = pygame.Rect(self.x, self.y, self.l, self.w)
        self.outline = pygame.Rect(self.x-5, self.y-5, self.l+10, self.w+10)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.outline)
        pygame.draw.rect(screen, self.colour, self.rect)
        base_font = pygame.font.Font(None, 32)
        text = base_font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x + int(round(self.l/2)), self.y + int(round(self.w/2))))
        screen.blit(text, text_rect)
        

    def get(self, event):
        return self.rect.collidepoint(event.pos)

class Entry():
    def __init__(self, x, y, l, w, prompt, length, upper=False, number=False, state=None):
        self.x = x - int(round(l/2))
        self.y = y - int(round(w/2))
        self.l = l
        self.w = w
        self.prompt = prompt
        self.length = length
        if not state:
            self.text = ""
        else:
            self.text = state
        self.active = False
        self.upper = upper
        self.number = number
        self.base_font = pygame.font.Font(None, w-5)
        self.rect = pygame.Rect(self.x, self.y, self.l, self.w)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        if len(self.text) != 0 or self.active:
            text_surface = self.base_font.render(self.text, True, (30, 30, 30))
        else:
            text_surface = self.base_font.render(self.prompt, True, (120, 120, 120))
        text_surface_rect = text_surface.get_rect(center=(self.x + int(round(self.l/2)), self.y + int(round(self.w/2))))
        screen.blit(text_surface, text_surface_rect)

    def get(self):
        return self.text

    def update(self, event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            self.active = True if self.rect.collidepoint(event.pos) else False
        if event.type==pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.length:
                if self.number:
                    try:
                        test = int(str(event.unicode))
                        self.text += event.unicode
                    except Exception:
                        pass
                else:
                    self.text += event.unicode
            if self.upper:
                self.text = self.text.upper()

class Text():
    def __init__(self, x, y, text, size, colour):
        self.x = x
        self.y = y
        self.text = text
        self.colour = colour
        self.base_font = pygame.font.Font(None, size)
        
    
    def draw(self, screen):
        text = self.base_font.render(self.text, True, self.colour)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

class Selector():
    def __init__(self, x, y, options, state=None):

        buffer = []
        for item in options:
            buffer.append(len(item))
        self.x = x - int(round((130 + max(buffer)*3)))
        self.y = y - int(round(25))
        if not state:
            self.pointer = 0
        else:
            self.pointer = options.index(state)
        self.options = options
        self.colour = (0, 0, 0)
        self.base_font = pygame.font.Font(None, 32)
        self.text = self.options[self.pointer]
        self.buffer = buffer

        
        self.rect = pygame.Rect(self.x, self.y, 2 * (130 + max(buffer)*3), 50)

        

        self.left = Button(x - (95 + max(buffer)*3), y, 40, 30, "<", (170, 170, 170))
        self.right = Button(x + (95 + max(buffer)*3), y, 40, 30, ">", (170, 170, 170))
    
    def draw(self, screen):
        pygame.draw.rect(screen, (170, 170, 170), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 5)
        text = self.base_font.render(self.text, True, self.colour)
        text_rect = text.get_rect(center=(self.x+(130 + max(self.buffer)*3), self.y+25))
        screen.blit(text, text_rect)
        self.left.draw(screen)
        self.right.draw(screen)
    
    def update(self, event):
        if self.left.get(event):
            if self.pointer == 0:
                self.pointer = len(self.options) - 1
            else:
                self.pointer -= 1
        
        if self.right.get(event):
            if self.pointer == len(self.options) - 1:
                self.pointer = 0
            else:
                self.pointer += 1

        self.text= self.options[self.pointer]

    def get(self):
        return self.options[self.pointer]

class Canvas():
    def __init__(self, x, y, l, w, colour, screen):
        self.x = x - int(round(l/2))
        self.y = y - int(round(w/2))
        self.l = l
        self.w = w
        self.colour = colour
        self.rect = pygame.Rect(self.x, self.y, self.l, self.w)
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def update(self, screen):
        self.screen = screen
        if pygame.mouse.get_pressed()[0] and self.in_bounds():
            pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, self.colour, pos, 20)

    def in_bounds(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x+20, y) and self.rect.collidepoint(x-20, y) and self.rect.collidepoint(x, y+20) and self.rect.collidepoint(x, y-20):
            return True
        return False

    def clear(self):
        try:
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
        except Exception:
            pass

    def get(self, screen):
        sub = screen.subsurface(self.rect)
        screenshot = pygame.Surface((self.l, self.w))
        screenshot.blit(sub, (0,0))
        pygame.image.save(screenshot, "screenshot.jpg")

class LiveText():
    def __init__(self, x, y, l, w, text, size, colour):
        self.x = x
        self.y = y
        self.l = l
        self.w = w
        self.text = text
        self.colour = colour
        self.base_font = pygame.font.Font(None, size)
        self.rect = pygame.Rect(self.x - int(round(l/2)), self.y - int(round(w/2)), self.l, self.w)
        self.outline = pygame.Rect(self.x-5 - int(round(l/2)), self.y-5 - int(round(w/2)), self.l+10, self.w+10)
        
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.outline)
        pygame.draw.rect(screen, (255,255,255), self.rect)
        text = self.base_font.render(self.text, True, self.colour)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def update(self,text):
        self.text = text