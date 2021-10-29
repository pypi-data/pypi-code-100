import argparse
import json
import os
import glob

from road_collisions import logger
from road_collisions.models.collision import Collision


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--raw-dir',
        dest='raw_dir',
        default=None
    )
    parser.add_argument(
        '--out-file',
        dest='out_file',
        default='/tmp/road_collisions_clean.json'
    )
    args = parser.parse_args()

    if args.raw_dir is None:
        raise Exception('Muse include --raw-dir')

    data = {}

    for filename in glob.iglob(f'{args.raw_dir}/**', recursive=True):
        if os.path.splitext(filename)[-1] != '.json':
            continue

        file_data = json.loads(open(filename).read())
        clean_data = file_data['controls'][3]['layers'][0]['features']

        if len(clean_data) == 0:
            continue

        for d in clean_data:
            point = Collision(d['data'], d['geometry'])
            data[point.id] = d

    list_data = data.values()
    logger.info('Resulted in %s datapoints', len(list_data))

    with open(args.out_file, 'w') as f:
        f.write(json.dumps(list(data.values())))


if __name__ == '__main__':
    main()
