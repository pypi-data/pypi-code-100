import pandas as pd
import yake
import dask.dataframe as dd

from dagster import InputDefinition, OutputDefinition, Field, Enum, EnumValue
from typing import List, Tuple, Union
from qdk.transform.base import TransformComponent
from qdk.dagster_types import DataFrameType


class YakeComponent(TransformComponent):
    config_schema = {
        "language": Field(
            Enum("Language", [EnumValue("en"), EnumValue("nl")]),
            default_value="nl",
            description="The language of the input text.",
        ),
        "n_grams": Field(
            int, default_value=1, description="The maximum length of keyword n-grams."
        ),
        "dedup_limit": Field(
            float, default_value=0.9, description="The deduplication limit."
        ),
        "n_keywords": Field(
            int, default_value=10, description="How many keywords to extract."
        ),
    }

    @staticmethod
    def _extract_keywords(
        text, extractor: yake.KeywordExtractor
    ) -> List[Tuple[str, float]]:
        """Extracts keywords from a string using a yake KeywordExtractor instance.

        Args:
            text (str): The text you want to extract the keywords from.
            extractor (yake.KeywordExtractor): The initialized yake keyword extractor.

        Returns:
            List[Tuple[str, float]]: Returns a list with keyword, score tuples. The scores indicates keyword relevence (the lower the better).
        """
        return extractor.extract_keywords(text)

    @classmethod
    def transform(
        cls,
        df: Union[pd.DataFrame, dd.DataFrame],
        language: str = "nl",
        n_grams: int = 1,
        dedup_limit: float = 0.9,
        n_keywords: int = 10,
    ) -> Union[pd.DataFrame, dd.DataFrame]:
        """Use the YAKE method to extract keywords from the text column in the dataframe.

        Args:
            df (Union[pd.DataFrame, dd.DataFrame]): The dataframe to perform the keyword extraction on.
            language (str, optional): Which base language to use for the keyword extraction. Defaults to "nl".
            n_grams (int, optional): The max length of the keywords. Defaults to 1.
            dedup_limit (float, optional): The deduplication limit. Defaults to 0.9.

        Returns:
            Union[pd.DataFrame, dd.DataFrame]: Returns a dataframe with a "_keywords" column.
        """
        # Create the yake keywork extractor
        extractor = yake.KeywordExtractor(
            lan=language, n=n_grams, dedupLim=dedup_limit, top=n_keywords
        )

        text_column_name = cls._get_text_column_name(df)

        # Use dask to parallelize the keyword extraction over the workers
        if type(df) == dd.DataFrame:
            df["_keywords"] = df.map_partitions(
                lambda _df: _df[text_column_name].apply(
                    cls._extract_keywords, args=(extractor,)
                )
            )
        # Pandas apply function
        else:
            df["_keywords"] = df[text_column_name].apply(
                cls._extract_keywords, args=(extractor,)
            )

        # Return the dataframe with the keywords
        return df
