from pathlib import Path
from typing import Callable, Optional

from .h5_dataset import H5Dataset


class ColossalSet224x224(H5Dataset):
    """
    Mixture of different histopathological datasets
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

    @classmethod
    def from_avocado(cls, sub_set: str = 'train', transform: Optional[Callable] = None, transform_target: Optional[Callable] = None):
        return cls(root='/data/ldap/histopathologic/processed_read_only/Histo_PreTrainDataset_224', 
                   sub_set=sub_set,
                   transform=transform, 
                   transform_target=transform_target
                  )
