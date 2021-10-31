from mammut.common.corpus.corpus_operations import CorpusOperations
from typing import List, Dict
from abc import abstractmethod
import datasets
from datasets import DatasetDict, Dataset
import os
from pathlib import Path


class HuggingFaceDatasetCorpus(CorpusOperations):
    """Generic interface for any type of curriculum training corpus
    based on a Hugging Face datasets.Dataset.

    Any concrete HuggingFaceDatasetCorpus known how to transform itself
    to a datasets.Dataset. By doing so, it straightforward to use it as
    training dataset of a Hugging Face model wrapper.

    This type of corpus doesn't form part of Mammut Corpus class hierarchy.
    However, It would be possible to create a Mammut Corpus class that implements
    the transformation to a datasets.Dataset. If so, this interface should be used.

    Currently, this kind of corpus isn't indexable or annotable.
    """

    def __init__(self, package_spreadhseet_id: str, corpus_id: str):
        """
        Args:
            package_spreadhseet_id:
                Package spreadsheet ID.
            corpus_id:
                ID assigned to this corpus in the CorpusMap column.
        """
        self.corpus_id = corpus_id
        self.spreadsheet_id = package_spreadhseet_id

    def get_events_as_strings(self) -> List[str]:
        raise NotImplementedError

    @property
    def indexable(self) -> bool:
        """This Corpus isn't considered for mammut-py indexing process."""
        return False

    @property
    def annotable(self) -> bool:
        """This Corpus isn't considered for mammut-py annotation process."""
        return False

    @abstractmethod
    def get_hf_dataset(self) -> datasets.Dataset:
        """Return a datasets.Dataset that can be used as training data for
        a hugging face model integration.
        """
        pass


class HuggingFaceFixedCorpus(HuggingFaceDatasetCorpus):
    """HuggingFace corpus for any fixed dataset provided as it is in
    datasets hub.

    The term fixed implies that the get_hf_dataset will return the
    downloaded dataset preserving the dataset.DatasetInfo configuration.

    If there's a requirement for changing the dataset.DatasetInfo, try to
    specify those operations in:
        - A specific child class of HuggingFaceDatasetCorpus. (Recommended).
        - In the curriculum Lesson/Model class that is intended to use the corpus.
    """

    def __init__(
        self, package_spreadsheet_id: str, corpus_id: str, config_kwargs: Dict
    ):
        """
        Args:
            package_spreadsheet_id:
                Package spreadsheet ID.
            corpus_id:
                ID assigned to this corpus in the CorpusMap column.
            config_kwargs:
                Dictionary to forward as the datasets.load_dataset.

        """
        super(HuggingFaceFixedCorpus, self).__init__(
            package_spreadsheet_id, corpus_id
        )

        if "dataset_build_args" not in config_kwargs:
            raise RuntimeError(
                f"HuggingFace fixed corpus without dataset_build_args. CorpusID: {corpus_id}"
            )

        build_args = config_kwargs["dataset_build_args"]
        self._base_dataset = datasets.load_dataset(**build_args)

        if "rename_columns" in config_kwargs:
            columns_rename_dict: Dict[str, str] = config_kwargs[
                "rename_columns"
            ]
            self._rename_dataset_columns(columns_rename_dict)

    def get_hf_dataset(self) -> datasets.Dataset:
        return self._base_dataset

    def _rename_dataset_columns(self, columns_rename_dict: Dict[str, str]):
        """Renames the columns in the self._dataset.

        Args:
            columns_rename_dict: A dictionary of Keys as the current column name,
                and the corresponding Values as the desired column name.

        Raises:
            ValueError if some Key isn't found in the dataset columns.

        Returns:
            None. This method renames the columns as a side effect.
        """
        for column_old_name, column_new_name in columns_rename_dict.items():
            if self._base_dataset == Dataset:
                dataset_columns = self._base_dataset.column_names
                self._base_dataset.rename_column_(
                    column_old_name, column_new_name
                )
                if column_old_name not in dataset_columns:
                    raise ValueError(
                        f'HuggingFace Fixed corpus rename error. Column "{column_old_name}" not found in '
                        f"dataset."
                    )
            if self._base_dataset == DatasetDict:
                dataset_columns = self._base_dataset["train"].column_names
                self._base_dataset.rename_column_(
                    column_old_name, column_new_name
                )
                if column_old_name not in dataset_columns:
                    raise ValueError(
                        f'HuggingFace Fixed corpus rename error. Column "{column_old_name}" not found in '
                        f"dataset."
                    )


class HuggingFaceFixedCorpusTest(HuggingFaceDatasetCorpus):
    """HuggingFace corpus to perform tests with local datasets hosted in
    tests/curriculum/resources directory as csv files with small samples of huggingface datasets.
    In order to avoid downloading the datasets from the huggingface hub.
    """

    def __init__(
        self, package_spreadsheet_id: str, corpus_id: str, config_kwargs
    ):
        """
        Args:
            package_spreadsheet_id:
                Package spreadsheet ID.
            corpus_id:
                ID assigned to this corpus in the CorpusMap column.
            config_kwargs:
                Dictionary to forward as the datasets.load_dataset. In this case,
                the local "name" csv file.

        """
        current_directory = os.path.dirname(os.path.realpath(__file__))
        HuggingFaceDatasetCorpus.__init__(
            self, package_spreadsheet_id, corpus_id
        )
        name_path = config_kwargs["dataset_build_args"]["local_folder"]
        current_directory_path = Path(current_directory).parents[3]
        dataset_local_path = os.path.join(current_directory_path, 'tests', 'curriculum', 'resources', name_path)

        self._base_dataset = datasets.load_from_disk(dataset_local_path)
        if "rename_columns" in config_kwargs:
            columns_rename_dict: Dict[str, str] = config_kwargs[
                "rename_columns"
            ]
            self._rename_dataset_columns(columns_rename_dict)

    def _rename_dataset_columns(self, columns_rename_dict: Dict[str, str]):
        """Renames the columns in the self._dataset.

        Args:
            columns_rename_dict: A dictionary of Keys as the current column name,
                and the corresponding Values as the desired column name.

        Raises:
            ValueError if some Key isn't found in the dataset columns.

        Returns:
            None. This method renames the columns as a side effect.
        """
        for column_old_name, column_new_name in columns_rename_dict.items():
            if self._base_dataset == Dataset:
                dataset_columns = self._base_dataset.column_names
                self._base_dataset.rename_column_(
                    column_old_name, column_new_name
                )
                if column_old_name not in dataset_columns:
                    raise ValueError(
                        f'HuggingFace Fixed corpus rename error. Column "{column_old_name}" not found in '
                        f"dataset."
                    )
            if self._base_dataset == DatasetDict:
                dataset_columns = self._base_dataset["train"].column_names
                self._base_dataset.rename_column_(
                    column_old_name, column_new_name
                )
                if column_old_name not in dataset_columns:
                    raise ValueError(
                        f'HuggingFace Fixed corpus rename error. Column "{column_old_name}" not found in '
                        f"dataset."
                    )

    def get_hf_dataset(self) -> datasets.Dataset:
        return self._base_dataset
