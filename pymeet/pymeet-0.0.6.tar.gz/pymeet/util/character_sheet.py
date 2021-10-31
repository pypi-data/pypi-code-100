from collections import defaultdict
import os
import json

import pygame as pg
import pygame.transform


def _make_image_row_config(raw_path, image_config):
    row_image = defaultdict(list)

    for name, image in image_config.items():
        path = os.path.join(raw_path, name)
        key = name.split('.')[0]

        width, height = map(float, image['dimension'].split(','))
        x, y = map(float, image['center'].split(','))

        scale = image['scale']
        width, height, x, y = map(lambda t: int(t*scale), [width, height, x, y])

        row_image[image['row']].append({
            'key': key,
            'path': path,
            'dimension': (width, height),
            'center': (x, y),
        })

    return row_image


def _row_to_sprite_render_config(row_image):
    sprites = list()

    prev_height = 0
    for row in sorted(row_image.keys()):
        images = row_image[row]
        most_right, max_height = 0, 0
        for image in images:
            image: dict = image.copy()
            width, height = image['dimension']

            image.update({
                'position': (most_right, prev_height),
            })
            sprites.append(image)

            most_right += width
            max_height = max(max_height, height)

        prev_height += max_height

    return sprites


def _make_sprite_render_config(raw_path, config):
    row_image = _make_image_row_config(raw_path, config['images'])
    sprites = _row_to_sprite_render_config(row_image)

    return sprites


def _save_sprite_sheet(sheet_path, sprites):
    pg.init()

    max_width = max(d['position'][0]+d['dimension'][0] for d in sprites)
    max_height = max(d['position'][1]+d['dimension'][1] for d in sprites)

    pg.display.set_mode((100, 100))  # any number is fine

    surf = pg.Surface((max_width, max_height), pg.SRCALPHA)

    for sprite in sprites:
        path = sprite['path']
        img = pg.image.load(path).convert_alpha()
        pos = sprite['position']

        surf.blit(pygame.transform.scale(img, sprite['dimension']), pos)

    pg.image.save(surf, sheet_path)


def _save_mapper(mapper_path, sprites):
    mapper = dict()
    for sprite in sprites:
        key = sprite['key']
        mapper[key] = {
            'center': sprite['center'],
            'position': sprite['position'],
            'dimension': sprite['dimension'],
        }

    with open(mapper_path, 'w') as file:
        json.dump(mapper, file)


def make_sprite_sheet(raw_path, config_path, sheet_path, mapper_path):
    with open(config_path) as file:
        config = json.load(file)

    sprites = _make_sprite_render_config(raw_path, config)
    _save_sprite_sheet(sheet_path, sprites)
    _save_mapper(mapper_path, sprites)


if __name__ == '__main__':
    make_sprite_sheet('pymeet/img/character/main/raw', 'pymeet/img/character/main/raw/config.json',
                      'pymeet/img/character/main/sheet.png', 'pymeet/img/character/main/mapper.json')
