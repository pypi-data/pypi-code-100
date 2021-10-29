# Import
import os
import math
import time
import pickle
import pygame

from _pickle import UnpicklingError

from cube_practicer.PLL import *

# Initialisation
curr_path = os.path.dirname(__file__)
resource_path = os.path.join(curr_path, 'resources')

screen = pygame.display.set_mode((1050, 600))
pygame.display.set_caption('Cube Practicer')

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

tinyFont = pygame.font.Font(os.path.join(resource_path, 'UbuntuMono-R.ttf'), 17)
font = pygame.font.Font(os.path.join(resource_path, 'UbuntuMono-R.ttf'), 20)
mediumFont = pygame.font.Font(os.path.join(resource_path, 'UbuntuMono-R.ttf'), 30)
largeFont = pygame.font.Font(os.path.join(resource_path, 'UbuntuMono-R.ttf'), 75)

MaxFPS = 100
colors = {
    'W': (255, 255, 255),
    'R': (255, 0, 0),
    'B': (0, 0, 255),
    'Y': (255, 255, 0),
    'G': (0, 255, 0),
    'O': (255, 127, 0)
}
coordChanges = {
    'U': [(-5, 5), (5, 5)],
    'D': [(-5, -5), (5, -5)],
    'L': [(5, -5), (5, 5)],
    'R': [(-5, -5), (-5, 5)],
    'UL': [(7, 0), (0, 7)],
    'UR': [(-7, 0), (0, 7)],
    'DL': [(0, -7), (7, 0)],
    'DR': [(0, -7), (-7, 0)]
}


# Classes
class Data:
    def __init__(self):
        self.status = 'mainMenu'
        self.displayData = None
        self.solves = {
            'PLL': {}
        }
        self.pllLibrarySorting = 'A - Z'


# Save/Load
def save() -> None:
    open(os.path.join(curr_path, os.pardir, 'save.txt'), 'w')
    pickle.dump(data, open(os.path.join(curr_path, os.pardir, 'save.txt'), 'wb'))


def load() -> None:
    global data

    try:
        data = pickle.load(open(os.path.join(curr_path, os.pardir, 'save.txt'), 'rb'))

    except FileNotFoundError:
        open(os.path.join(curr_path, os.pardir, 'save.txt'), 'w')

    except (EOFError, UnpicklingError):
        pass


# Screen Printing Functions
def leftAlignPrint(font: pygame.font.Font, text: str, pos: Tuple[int], color: Tuple[Union[int, int, int]] = (0, 0, 0)) -> None:
    textObj = font.render(text, True, color)
    screen.blit(textObj, textObj.get_rect(center=[pos[0] + font.size(text)[0] / 2, pos[1]]))


def centredPrint(font: pygame.font.Font, text: str, pos: Tuple[int], color: Tuple[Union[int, int, int]] = (0, 0, 0)) -> None:
    textObj = font.render(text, True, color)
    screen.blit(textObj, textObj.get_rect(center=pos))


def rightAlignPrint(font: pygame.font.Font, text: str, pos: Tuple[int], color: Tuple[Union[int, int, int]] = (0, 0, 0)) -> None:
    textObj = font.render(text, True, color)
    screen.blit(textObj, textObj.get_rect(center=[pos[0] - font.size(text)[0] / 2, pos[1]]))


def drawGraph(d: list, rect: Tuple[Union[int, int, int, int]], *, backgroundColor: Optional[Tuple[Union[int, int, int]]] = (200, 200, 200), borderColor: Optional[Tuple[Union[int, int, int]]] = None, borderWidth: Optional[int] = None, lineColor: Optional[Tuple[Union[int, int, int]]] = (0, 0, 0), lineWidth: Optional[int] = 5) -> None:
    mx, my = pygame.mouse.get_pos()

    if borderWidth is not None and borderColor is not None:
        pygame.draw.rect(screen, borderColor, (rect[0] - borderWidth, rect[1] - borderWidth, rect[2] + 2 * borderWidth, rect[3] + 2 * borderWidth))
    pygame.draw.rect(screen, backgroundColor, rect)

    highest = max(d) * 1.1
    dataLength = len(d)

    if dataLength == 1:
        pygame.draw.circle(screen, lineColor, (rect[0] + rect[2] / 2, rect[1] + rect[3] * (1 - d[0] / highest)), lineWidth / 2)
    else:
        for n in range(dataLength - 1):
            pos = (rect[0] + n / (dataLength - 1) * rect[2], rect[1] + rect[3] * (1 - d[n] / highest))
            pygame.draw.line(screen, lineColor, pos, (rect[0] + (n + 1) / (dataLength - 1) * rect[2], rect[1] + rect[3] * (1 - d[n + 1] / highest)), lineWidth)

    if borderWidth is not None and borderColor is not None:
        pygame.draw.rect(screen, borderColor, rect, borderWidth * 2)

    gap = highest * 50 / rect[3]
    for n in range(rect[3] // 50 + 1):
        pygame.draw.line(screen, (128, 128, 128), (rect[0] - 5, rect[1] + rect[3] - n * 50), (rect[0] + 5, rect[1] + rect[3] - n * 50), 3)
        rightAlignPrint(tinyFont, durationToStr(round(gap * n, 2)), (rect[0] - 10, rect[1] + rect[3] - n * 50))

    if rect[0] <= mx <= rect[0] + rect[2] and rect[1] <= my <= rect[1] + rect[3]:
        if dataLength == 1:
            pygame.draw.line(screen, (128, 128, 128), (rect[0] + rect[2] / 2, rect[1]), (rect[0] + rect[2] / 2, rect[1] + rect[3]), 3)
            centredPrint(tinyFont, str(durationToStr(round(d[0], 2))), (rect[0] + rect[2] / 2, rect[1] + rect[3] + 10))

        else:
            dataIndex = round((mx - rect[0]) / (rect[2] / (dataLength - 1)))
            x = rect[0] + rect[2] * (dataIndex - 0) / (dataLength - 1)
            pygame.draw.line(screen, (128, 128, 128), (x, rect[1] + 4), (x, rect[1] + rect[3] - 4), 3)

            centredPrint(tinyFont, str(durationToStr(round(d[dataIndex], 2))), (x, rect[1] + rect[3] + 10))


# Functions
def reverseAlgorithm(moveList: List[str]) -> List[str]:
    toReturn = []

    for move in moveList:
        if '2' in move:
            toReturn.append(move)
        elif '\'' in move:
            toReturn.append(move[:-1])
        else:
            toReturn.append(move + '\'')

    return toReturn


def twoDecimalPlaces(num: float) -> str:
    num = str(round(num, 2))
    if '.' in num:
        a, b = num.split('.')

        if len(b) == 1:
            return f'{a}.{b}0'
        return f'{a}.{b}'

    else:
        return f'{num}.00'


def durationToStr(duration: float) -> str:
    if duration > 60:
        return f'{round(duration // 60)}:{duration % 60}'
    return str(duration)


data = Data()
load()


def app():
    while True:
        if data.status == 'mainMenu':
            while True:
                mx, my = pygame.mouse.get_pos()

                screen.fill((100, 100, 100))

                centredPrint(mediumFont, 'Main Menu', (525, 50))

                pygame.draw.rect(screen, (200, 200, 200), (25, 100, 950, 30))
                leftAlignPrint(font, 'PLL Library', (40, 115))
                if 25 <= mx <= 975 and 100 <= my <= 130:
                    pygame.draw.rect(screen, (64, 64, 64), (25, 100, 950, 30), 3)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (25, 100, 950, 30), 3)

                cont = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save()
                        quit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if 25 <= my <= 975 and 100 <= my <= 130:
                                data.status = 'pllLibrary'
                                cont = False

                if not cont:
                    break

                pygame.display.update()
                clock.tick(MaxFPS)

        elif data.status == 'pllLibrary':
            scroll = 0
            while True:
                mx, my = pygame.mouse.get_pos()

                screen.fill((100, 100, 100))

                pygame.draw.rect(screen, (100, 100, 100), (0, 0, 1050, 80))

                centredPrint(mediumFont, 'PLL Library', (525, 40 - scroll))

                permutations = {
                    'A - Z': Permutations,
                    'Z - A': ReversePermutations,
                    'Type': SortedTypePermutations
                }[data.pllLibrarySorting]

                for y in range(math.ceil(len(permutations))):
                    for x in range(5):
                        if x + y * 5 < len(permutations):
                            Perm = permutations[x + y * 5]

                            if x * 200 + 50 <= mx <= x * 200 + 200 and y * 200 + 100 - scroll <= my <= y * 200 + 250 - scroll and 80 <= my <= 550:
                                pygame.draw.rect(screen, (200, 200, 200), (x * 200 + 47, y * 200 + 97 - scroll, 156, 156))
                            else:
                                pygame.draw.rect(screen, (0, 0, 0), (x * 200 + 47, y * 200 + 97 - scroll, 156, 156))
                            if data.pllLibrarySorting == 'Type':
                                pygame.draw.rect(screen, Perm.algTypeColor, (x * 200 + 50, y * 200 + 100 - scroll, 150, 150))
                            else:
                                pygame.draw.rect(screen, (64, 64, 64), (x * 200 + 50, y * 200 + 100 - scroll, 150, 150))
                            centredPrint(font, f'{Perm.name} Perm', (x * 200 + 125, y * 200 + 270 - scroll))

                            pygame.draw.rect(screen, (255, 255, 0), (x * 200 + 80, y * 200 + 130 - scroll, 90, 90))
                            for n in range(4):
                                pygame.draw.line(screen, (0, 0, 0), (x * 200 + 80 + n * 30, y * 200 + 130 - scroll), (x * 200 + 80 + n * 30, y * 200 + 220 - scroll), 3)
                                pygame.draw.line(screen, (0, 0, 0), (x * 200 + 80, y * 200 + 130 - scroll + n * 30), (x * 200 + 170, y * 200 + 130 - scroll + n * 30), 3)

                            for n in range(3):
                                pygame.draw.line(screen, colors[Perm.example[0][n]], (x * 200 + 83 + n * 30, y * 200 + 120 - scroll), (x * 200 + 107 + n * 30, y * 200 + 120 - scroll), 3)
                                pygame.draw.line(screen, colors[Perm.example[1][n]], (x * 200 + 180, y * 200 + 133 + n * 30 - scroll), (x * 200 + 180, y * 200 + 157 + n * 30 - scroll), 3)
                                pygame.draw.line(screen, colors[Perm.example[2][n]], (x * 200 + 83 + n * 30, y * 200 + 230 - scroll), (x * 200 + 107 + n * 30, y * 200 + 230 - scroll), 3)
                                pygame.draw.line(screen, colors[Perm.example[3][n]], (x * 200 + 70, y * 200 + 133 - scroll + n * 30), (x * 200 + 70, y * 200 + 157 - scroll + n * 30), 3)

                            for movement in Perm.movement:
                                lineWidth = 4 if movement[0][0] != movement[1][0] and movement[0][1] != movement[1][1] else 3
                                starting = (x * 200 + 95 + movement[0][0] * 30, y * 200 + 145 + movement[0][1] * 30 - scroll)
                                destination = (x * 200 + 95 + movement[1][0] * 30, y * 200 + 145 + movement[1][1] * 30 - scroll)
                                pygame.draw.line(screen, (32, 32, 32), starting, destination, lineWidth)

                                coordChange = coordChanges[movement[2]]
                                pygame.draw.polygon(screen, (32, 32, 32), [destination, (destination[0] + coordChange[0][0], destination[1] + coordChange[0][1]), (destination[0] + coordChange[1][0], destination[1] + coordChange[1][1])])

                pygame.draw.rect(screen, (100, 100, 100), (0, 550, 1050, 50))

                pygame.draw.rect(screen, (255, 0, 0), (50, 560, 100, 30))
                centredPrint(font, 'Exit', (100, 575))
                if 50 <= mx <= 150 and 560 <= my <= 590:
                    pygame.draw.rect(screen, (64, 64, 64), (50, 560, 100, 30), 3)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (50, 560, 100, 30), 3)

                pygame.draw.rect(screen, (200, 200, 200), (900, 560, 100, 30))
                centredPrint(font, data.pllLibrarySorting, (950, 575))
                if 900 <= mx <= 1000 and 560 <= my <= 590:
                    pygame.draw.rect(screen, (64, 64, 64), (900, 560, 100, 30), 3)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (900, 560, 100, 30), 3)

                cont = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save()
                        quit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if 50 <= mx <= 150 and 560 <= my <= 590:
                                data.status = 'mainMenu'
                                cont = False

                            elif 900 <= mx <= 1000 and 560 <= my <= 590:
                                pllLibrarySortingCycle = ['A - Z', 'Z - A', 'Type', 'A - Z']
                                data.pllLibrarySorting = pllLibrarySortingCycle[pllLibrarySortingCycle.index(data.pllLibrarySorting) + 1]

                            for y in range(math.ceil(len(permutations))):
                                for x in range(5):
                                    if x + y * 5 < len(permutations):
                                        if x * 200 + 50 <= mx <= x * 200 + 200 and y * 200 + 100 - scroll <= my <= y * 200 + 250 - scroll and 80 <= my <= 550:
                                            data.status = 'pllInspect'
                                            data.displayData = permutations[x + y * 5]
                                            cont = False

                        elif event.button == 4:
                            scroll = max(0, scroll - 20)

                        elif event.button == 5:
                            scroll = min(600, scroll + 20)

                if not cont:
                    break

                pygame.display.update()
                clock.tick(MaxFPS)

        elif data.status == 'pllInspect':
            while True:
                mx, my = pygame.mouse.get_pos()

                screen.fill((100, 100, 100))

                centredPrint(mediumFont, f'{data.displayData.name} Perm', (525, 40))

                pygame.draw.rect(screen, (200, 200, 200), (50, 560, 100, 30))
                centredPrint(font, 'Back', (100, 575))
                if 50 <= mx <= 150 and 560 <= my <= 590:
                    pygame.draw.rect(screen, (64, 64, 64), (50, 560, 100, 30), 3)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (50, 560, 100, 30), 3)

                pygame.draw.rect(screen, (200, 200, 200), (200, 560, 150, 30))
                centredPrint(font, 'Practise', (275, 575))
                if 200 <= mx <= 350 and 560 <= my <= 590:
                    pygame.draw.rect(screen, (64, 64, 64), (200, 560, 150, 30), 3)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (200, 560, 150, 30), 3)

                pygame.draw.rect(screen, (200, 200, 200), (100, 420, 200, 30))
                centredPrint(font, 'Remove Last Solve', (200, 435))
                if 100 <= mx <= 300 and 420 <= my <= 450:
                    pygame.draw.rect(screen, (64, 64, 64), (100, 420, 200, 30), 3)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (100, 420, 200, 30), 3)

                pygame.draw.rect(screen, (200, 200, 200), (400, 420, 200, 30))
                centredPrint(font, '+2 For Last Solve', (500, 435))
                if 400 <= mx <= 600 and 420 <= my <= 450:
                    pygame.draw.rect(screen, (64, 64, 64), (400, 420, 200, 30), 3)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (400, 420, 200, 30), 3)

                if data.displayData.name in data.solves['PLL'].keys():
                    drawGraph(data.solves['PLL'][data.displayData.name], (100, 100, 500, 300), borderColor=(0, 0, 0), borderWidth=3, lineColor=(255, 0, 0))
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (97, 97, 506, 306))
                    pygame.draw.rect(screen, (200, 200, 200), (100, 100, 500, 300))
                    centredPrint(font, f'You have no {data.displayData.name} Perm solves!', (350, 250))

                pygame.draw.rect(screen, (255, 255, 0), (675, 100, 300, 300))

                for n in range(4):
                    pygame.draw.line(screen, (0, 0, 0), (675 + 100 * n, 100), (675 + 100 * n, 400), 5)
                    pygame.draw.line(screen, (0, 0, 0), (675, 100 + 100 * n), (975, 100 + 100 * n), 5)

                for n in range(3):
                    pygame.draw.line(screen, colors[data.displayData.example[0][n]], (685 + 100 * n, 85), (765 + 100 * n, 85), 9)
                    pygame.draw.line(screen, colors[data.displayData.example[1][n]], (990, 110 + 100 * n), (990, 190 + 100 * n), 9)
                    pygame.draw.line(screen, colors[data.displayData.example[2][n]], (685 + 100 * n, 415), (765 + 100 * n, 415), 9)
                    pygame.draw.line(screen, colors[data.displayData.example[3][n]], (660, 110 + 100 * n), (660, 190 + 100 * n), 9)

                for movement in data.displayData.movement:
                    lineWidth = 6 if movement[0][0] != movement[1][0] and movement[0][1] != movement[1][1] else 5

                    starting = (725 + movement[0][0] * 100, 150 + movement[0][1] * 100)
                    destination = (725 + movement[1][0] * 100, 150 + movement[1][1] * 100)
                    pygame.draw.line(screen, (32, 32, 32), starting, destination, lineWidth)

                    coordChange = coordChanges[movement[2]]
                    pygame.draw.polygon(screen, (32, 32, 32), [destination, (destination[0] + coordChange[0][0] * 3, destination[1] + coordChange[0][1] * 3), (destination[0] + coordChange[1][0] * 3, destination[1] + coordChange[1][1] * 3)])

                for m in range(len(data.displayData.moves)):
                    centredPrint(font, data.displayData.moves[m], (525, 478 + m * 30))

                cont = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save()
                        quit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if 50 <= mx <= 150 and 560 <= my <= 590:
                                data.status = 'pllLibrary'
                                cont = False

                            elif 200 <= mx <= 350 and 560 <= my <= 590:
                                data.status = 'pllPractise'
                                cont = False

                            elif 100 <= mx <= 300 and 420 <= my <= 450:
                                try:
                                    data.solves['PLL'][data.displayData.name] = data.solves['PLL'][data.displayData.name][:-1]
                                except (KeyError, IndexError):
                                    pass

                            elif 400 <= mx <= 600 and 420 <= my <= 450:
                                try:
                                    data.solves['PLL'][data.displayData.name][-1] = data.solves['PLL'][data.displayData.name][-1] + 2
                                except (KeyError, IndexError):
                                    pass

                if not cont:
                    break

                pygame.display.update()
                clock.tick(MaxFPS)

        elif data.status == 'pllPractise':
            solving = False
            startTime = None
            solveTime = 0
            while True:
                mx, my = pygame.mouse.get_pos()

                screen.fill((100, 100, 100))

                centredPrint(mediumFont, f'{data.displayData.name} Perm', (525, 40))

                pygame.draw.rect(screen, (200, 200, 200), (50, 560, 100, 30))
                centredPrint(font, 'Back', (100, 575))
                if 50 <= mx <= 150 and 560 <= my <= 590:
                    pygame.draw.rect(screen, (64, 64, 64), (50, 560, 100, 30), 3)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (50, 560, 100, 30), 3)

                if not solving:
                    centredPrint(font, f'Scramble: {" ".join(reverseAlgorithm(data.displayData.movesList[0]))}', (525, 80))

                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                        color = (0, 255, 0)
                    else:
                        color = (0, 0, 0)

                    centredPrint(largeFont, twoDecimalPlaces(solveTime), (525, 150), color)

                else:
                    centredPrint(largeFont, twoDecimalPlaces(time.time() - startTime), (525, 150), (255, 0, 0))

                cont = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save()
                        quit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if 50 <= mx <= 150 and 560 <= my <= 590:
                                data.status = 'pllInspect'
                                cont = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if solving:
                                solveTime = round(time.time() - startTime, 2)
                                try:
                                    data.solves['PLL'][data.displayData.name].append(solveTime)
                                except KeyError:
                                    data.solves['PLL'][data.displayData.name] = [solveTime]

                            else:
                                solveTime = 0

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            if not solving:
                                startTime = time.time()
                            solving = not solving

                if not cont:
                    break

                pygame.display.update()
                clock.tick(MaxFPS)


if __name__ == '__main__':
    app()
