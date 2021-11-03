#!/usr/bin/env python3
import random 

# canvas size and subset square dimensions are predetermined
MAX_HEIGHT  = 28
INNER_DIFF  = 6
TOP_DIFF    = 4

def set_colors():
    """
    returns palette of four colors each "color" is an empty string 
    with a randomly selected color applied to its background 
    """
    bg_colors = []
    while len(bg_colors) < 4:
        num = random.randint(0,256)
        bg_color = f'\033[48;5;{num}m \033[0;0m'
        if bg_color not in bg_colors:
            bg_colors.append(bg_color)

    return bg_colors

def write_square():
    """
    sets color palette and generates the square as a fixed-dimension string 
    the square's layers are determined by their index on the square's y- (or height-) axis
    """
    first_color, second_color, third_color, fourth_color = set_colors()

    i = 0
    square = ''

    while i < MAX_HEIGHT:
        if  i >= TOP_DIFF*3 and i < MAX_HEIGHT-6: 
            row = f'{first_color * INNER_DIFF}{second_color * INNER_DIFF}{third_color * INNER_DIFF}{fourth_color * (MAX_HEIGHT * 2 - (INNER_DIFF * 6))}{third_color * INNER_DIFF}{second_color * INNER_DIFF}{first_color * INNER_DIFF}'
            square += f'{row}\n'
        
        elif  i >= TOP_DIFF*2 and i < MAX_HEIGHT-4:
            row = f'{first_color * INNER_DIFF}{second_color * INNER_DIFF}{third_color * (MAX_HEIGHT * 2 - (INNER_DIFF * 4))}{second_color * INNER_DIFF}{first_color * INNER_DIFF}'
            square += f'{row}\n' 
        
        elif  i >= TOP_DIFF and i < MAX_HEIGHT-2: 
            row = f'{first_color * INNER_DIFF}{second_color * (MAX_HEIGHT * 2 - (INNER_DIFF * 2))}{first_color * INNER_DIFF}'
            square += f'{row}\n'
        
        else: 
            row = f'{first_color * (MAX_HEIGHT * 2)}'
            square += f'{row}\n'
        
        i+=1

    return square

def main():
    square = write_square()
    print(f'\n{square}\n')


if __name__ == '__main__':
    main()

    