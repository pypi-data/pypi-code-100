from typing import *


class Permutation:
    def __init__(self, name: str, moves: str, movement: Tuple[Union[Tuple[Union[int, int]], Tuple[Union[int, int]], str]], example: List[Union[str, str, str, str]], algTypeColor: Tuple[Union[int, int, int]]):
        self.name = name
        self.moves = [m for m in moves.split(' | ')]
        self.movesList = [m.replace('(', '').replace(')', '').split(' ') for m in self.moves]
        self.movement = movement
        self.example = example
        self.algTypeColor = algTypeColor


Permutations = [
    Permutation(
        'Aa',
        """x (R' U R') D2 (R U' R') D2 R2 x'""",
        [
            [[0, 0], [2, 0], 'R'],
            [[2, 0], [2, 2], 'D'],
            [[2, 2], [0, 0], 'UL']
        ],
        ['GOG', 'RGB', 'RRO', 'OBB'],
        (255, 200, 100)
    ),
    Permutation(
        'Ab',
        """y x' (R U' R) D2 (R' U R) D2 R2' x""",
        [
            [[0, 0], [2, 2], 'DR'],
            [[2, 2], [2, 0], 'U'],
            [[2, 0], [0, 0], 'L']
        ],
        ['ROB', 'OGO', 'RRG', 'GBB'],
        (255, 200, 100)
    ),
    Permutation(
        'E',
        """x' (R U' R' D) (R U R' D') (R U R' D) (R U' R' D') x""",
        [
            [[0, 2], [0, 0], 'U'],
            [[0, 0], [0, 2], 'D'],
            [[2, 2], [2, 0], 'U'],
            [[2, 0], [2, 2], 'D']
        ],
        ['OGR', 'BRG', 'OBR', 'BOG'],
        (255, 200, 100)
    ),
    Permutation(
        'F',
        """(R' U' F')(R U R' U')(R' F R2 U')(R' U' R U)(R' U R)""",
        [
            [[1, 2], [1, 0], 'U'],
            [[1, 0], [1, 2], 'D'],
            [[2, 2], [2, 0], 'U'],
            [[2, 0], [2, 2], 'D']
        ],
        ['GBR', 'BRG', 'BGR', 'OOO'],
        (255, 255, 127)
    ),
    Permutation(
        'Ga',
        """R2 U (R' U R' U') (R U' R2) D U' (R' U R D') U""",
        [],
        ['GBR', 'BOG', 'BRR', 'OGO'],
        (153, 255, 255)
    ),
    Permutation(
        'Gb',
        """(R' U' R U) D' R2 (U R' U R) (U' R U') R2 D""",
        [],
        ['GOR', 'BBG', 'BGR', 'ORO'],
        (153, 255, 255)
    ),
    Permutation(
        'Gc',
        """R2 U' (R U' R U) (R' U R2 D') (U R U' R') D U'""",
        [],
        ['GRR', 'BOG', 'BGR', 'OBO'],
        (153, 255, 255)
    ),
    Permutation(
        'Gd',
        """D' (R U R' U') D (R2 U' R U') (R' U R' U) R2 U""",
        [],
        ['GBR', 'BGG', 'BOR', 'ORO'],
        (153, 255, 255)
    ),
    Permutation(
        'H',
        """(M2 U M2) U2 (M2 U M2)""",
        [
            [[1, 2], [1, 0], 'U'],
            [[1, 0], [1, 2], 'D'],
            [[2, 1], [0, 1], 'L'],
            [[0, 1], [2, 1], 'R']
        ],
        ['ORO', 'GBG', 'ROR', 'BGB'],
        (255, 128, 128)
    ),
    Permutation(
        'Ja',
        """(R' U L' U2) (R U' R' U2 R) L U'""",
        [
            [[2, 0], [0, 0], 'L'],
            [[0, 0], [2, 0], 'R'],
            [[0, 1], [1, 0], 'UR'],
            [[1, 0], [0, 1], 'DL']
        ],
        ['ORR', 'BOO', 'GGG', 'BBR'],
        (255, 255, 127)
    ),
    Permutation(
        'Jb',
        """(R U R' F') (R U R' U') R' F R2 U' R' U'""",
        [
            [[2, 2], [2, 0], 'U'],
            [[2, 0], [2, 2], 'D'],
            [[1, 2], [2, 1], 'UR'],
            [[2, 1], [1, 2], 'DL']
        ],
        ['OOG', 'RRO', 'RGG', 'BBB'],
        (255, 255, 127)
    ),
    Permutation(
        'Na',
        """(R U R' U) (R U R' F') (R U R' U') R' F R2 U' R' U' (U' R U' R')""",
        [
            [[2, 0], [0, 2], 'DL'],
            [[0, 2], [2, 0], 'UR'],
            [[0, 1], [2, 1], 'R'],
            [[2, 1], [0, 1], 'L']
        ],
        ['GGB', 'OOR', 'GBB', 'ORR'],
        (200, 255, 100)
    ),
    Permutation(
        'Nb',
        """(R' U R U') (R' F' U' F) (R U R' F) R' F' (R U' R)""",
        [
            [[0, 0], [2, 2], 'DR'],
            [[2, 2], [0, 0], 'UL'],
            [[0, 1], [2, 1], 'R'],
            [[2, 1], [0, 1], 'L']
        ],
        ['GBB', 'ROO', 'BBG', 'RRO'],
        (200, 255, 100)
    ),
    Permutation(
        'Ra',
        """(R U' R' U') (R U R D) (R' U' R D') (R' U2 R') U'""",
        [
            [[2, 2], [2, 0], 'U'],
            [[2, 0], [2, 2], 'D'],
            [[1, 0], [0, 1], 'DL'],
            [[0, 1], [1, 0], 'UR']
        ],
        ['BRO', 'GOB', 'GGO', 'RBR'],
        (255, 255, 127)
    ),
    Permutation(
        'Rb',
        """(R' U2 R U2) R' F (R U R' U') R' F' R2 U'""",
        [
            [[2, 0], [0, 0], 'L'],
            [[0, 0], [2, 0], 'R'],
            [[1, 2], [2, 1], 'UR'],
            [[2, 1], [1, 2], 'DL']
        ],
        ['GOB', 'ORG', 'RGR', 'OBB'],
        (255, 255, 127)
    ),
    Permutation(
        'T',
        """(R U R' U') (R' F R2 U') R' U' (R U R' F')""",
        [
            [[2, 2], [2, 0], 'U'],
            [[2, 0], [2, 2], 'D'],
            [[0, 1], [2, 1], 'R'],
            [[2, 1], [0, 1], 'L']
        ],
        ['OOG', 'RBO', 'RRG', 'BGB'],
        (255, 255, 127)
    ),
    Permutation(
        'Ua',
        """M2 U M U2 M U M2 | (R U' R U) R U (R U' R' U') R2 | (F2 U' L R') F2 (L' R U' F2)""",
        [
            [[2, 1], [0, 1], 'L'],
            [[0, 1], [1, 2], 'DR'],
            [[1, 2], [2, 1], 'UR']
        ],
        ['BBB', 'ORO', 'GOG', 'RGR'],
        (255, 128, 128)
    ),
    Permutation(
        'Ub',
        """M2 U' M U2 M U' M2 | R2 U (R U R' U') R' U' (R' U R') | (F2 U' L R') F2 (L' R U' F2)""",
        [
            [[2, 1], [1, 2], 'DL'],
            [[1, 2], [0, 1], 'UL'],
            [[0, 1], [2, 1], 'R']
        ],
        ['BBB', 'OGO', 'GRG', 'ROR'],
        (255, 128, 128)
    ),
    Permutation(
        'V',
        """(R' U R' U') y (R' F' R2 U') (R' U R' F) R F""",
        [
            [[0, 0], [2, 2], 'DR'],
            [[2, 2], [0, 0], 'UL'],
            [[1, 0], [2, 1], 'DR'],
            [[2, 1], [1, 0], 'UL']
        ],
        ['RGO', 'GOB', 'RRO', 'GBB'],
        (200, 255, 100)
    ),
    Permutation(
        'Y',
        """F (R U' R' U') (R U R' F') (R U R' U') (R' F R F')""",
        [
            [[0, 0], [2, 2], 'DR'],
            [[2, 2], [0, 0], 'UL'],
            [[1, 0], [0, 1], 'DL'],
            [[0, 1], [1, 0], 'UR']
        ],
        ['RBO', 'GGB', 'RRO', 'GOB'],
        (200, 255, 100)
    ),
    Permutation(
        'Z',
        """(M2' U M2' U) (M' U2) (M2' U2 M') U2 | y' M' U (M2' U M2') U (M' U2 M2) U'""",
        [
            [[1, 0], [0, 1], 'DL'],
            [[0, 1], [1, 0], 'UR'],
            [[2, 1], [1, 2], 'DL'],
            [[1, 2], [2, 1], 'UR']
        ],
        ['OBO', 'GRG', 'RGR', 'BOB'],
        (255, 128, 128)
    )
]

ReversePermutations = Permutations[::-1]
SortedTypePermutations = [Permutations[n] for n in [8, 16, 17, 20, 0, 1, 2, 3, 9, 10, 13, 14, 15, 11, 12, 18, 19, 4, 5, 6, 7]]
