from pathlib import Path
from typing import Callable, Optional

from .h5_dataset import H5Dataset

# TODO how to handle multiple resolution? Could use different "from_avocado" methods but then the API will differ between classes.

class Kather96x96(H5Dataset):
    """
    Kather dataset, more information can be found at https://zenodo.org/record/1214456
    """

    def __init__(self, root: str, sub_set: str, transform: Optional[Callable] = None, transform_target: Optional[Callable] = None):
        assert sub_set in ['train', 'valid', 'test']

        super().__init__(data_path=Path(root) / f'{sub_set}.h5',
                         data_key='image',
                         target_path=Path(
                             root) / f'{sub_set}.h5',
                         target_key='label',
                         transform=transform,
                         transform_target=transform_target)

        self.classes = ['ADI', 'BACK', 'DEB', 'LYM', 'MUC', 'MUS', 'NORM', 'STR', 'TUM']

    @classmethod
    def from_avocado(cls, sub_set: str = 'train', transform: Optional[Callable] = None, transform_target: Optional[Callable] = None):
        return cls('/data/ldap/histopathologic/processed_read_only/Kather_H5/res96', sub_set, transform,transform_target)


class Kather224x224(H5Dataset):
    """
    Kather dataset, more information can be found at https://zenodo.org/record/1214456
    """

    def __init__(self, root: str, sub_set: str, transform: Optional[Callable] = None, transform_target: Optional[Callable] = None):
        assert sub_set in ['train', 'valid', 'test']

        super().__init__(data_path=Path(root) / f'{sub_set}.h5',
                         data_key='image',
                         target_path=Path(
                             root) / f'{sub_set}.h5',
                         target_key='label',
                         transform=transform,
                         transform_target=transform_target)

        self.classes = ['ADI', 'BACK', 'DEB', 'LYM', 'MUC', 'MUS', 'NORM', 'STR', 'TUM']

    @classmethod
    def from_avocado(cls, sub_set: str = 'train', transform: Optional[Callable] = None, transform_target: Optional[Callable] = None):
        return cls('/data/ldap/histopathologic/processed_read_only/Kather_H5/res224', sub_set, transform, transform_target)
