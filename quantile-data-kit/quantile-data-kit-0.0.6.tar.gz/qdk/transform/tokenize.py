from dagster import InputDefinition, OutputDefinition, Field
from qdk.transform.base import TransformComponent
from qdk.dagster_types import DataFrameType


class TokenizeComponent(TransformComponent):
    input_defs = [InputDefinition("df", DataFrameType)]
    output_defs = [OutputDefinition(DataFrameType, "df")]
    config_schema = {
        "lower": Field(
            bool,
            default_value=True,
            description="Whether to transform the text to lowercase.",
        )
    }

    @classmethod
    def transform(cls, df: DataFrameType, lower: bool = True) -> DataFrameType:
        text_column_name = cls._get_text_column_name(df)
        df["_tokens"] = df[text_column_name]

        # Conditionally lowercase the text
        if lower:
            df["_tokens"] = df["_tokens"].str.lower()

        df["_tokens"] = df["_tokens"].str.split(r"\W+")

        return df
