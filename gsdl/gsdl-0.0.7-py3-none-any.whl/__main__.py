import subprocess
from .utils import *


def check_spec() -> None:
    spec = fast_read(p('buildozer.spec'))
    lines = spec.split('\n')
    for line_num in range(len(lines)):
        line = lines[line_num]
        low = line.lower().strip()
        if low.startswith('source.include_exts'):
            lines[line_num] = 'source.include_exts = py,png,jpg,kv,atlas,ttf,jpg,ico,ogg,mp3'
            continue
        if low.startswith('#source.exclude_dirs'):
            lines[line_num] = 'source.exclude_dirs = tests, bin, __pycache__, .idea, dist, build'
            continue
        if low.startswith('requirements'):
            lines[line_num] = 'requirements = python3,pygame,Pillow,gsdl'
            continue
        if low.startswith('orientation'):
            lines[line_num] = 'orientation = landscape'
            continue
        if low.startswith('# android.accept_sdk_license'):
            lines[line_num] = 'android.accept_sdk_license = True'
            continue
    fast_write(p('buildozer.spec'), '\n'.join(lines))


for x in sys.argv[1:]:
    cur = x.lower().strip()
    if cur == '--help':
        print('\n\nArgs:')
        print('--help')
        print('--build-debug')
        print('--build-release')
        sys.exit(0)
    if cur == '--init':
        subprocess.call([
            sys.executable,
            '-m',
            'buildozer',
            'init'
        ])
        check_spec()
        sys.exit(0)
    if cur == '--build-debug':
        subprocess.call([
            sys.executable,
            '-m',
            'buildozer',
            'android',
            'debug',
            'deploy',
            'run'
        ])
        sys.exit(0)
    if cur == '--build-release':
        subprocess.call([
            sys.executable,
            '-m',
            'buildozer',
            'android',
            'debug',
            'deploy',
            'run'
        ])
        sys.exit(0)
    print(f'Unknown arg: {cur}')
    sys.exit(1)
