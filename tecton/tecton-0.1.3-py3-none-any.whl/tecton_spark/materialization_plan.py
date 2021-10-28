from typing import List
from typing import Optional
from typing import Tuple

import attr
import pendulum
from pyspark.sql import DataFrame
from pyspark.sql import functions
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType

from tecton_proto.data.new_transformation_pb2 import NewTransformation as Transformation
from tecton_proto.data.virtual_data_source_pb2 import VirtualDataSource
from tecton_spark.errors import TectonFeatureTimeError
from tecton_spark.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_spark.partial_aggregations import construct_partial_time_aggregation_df
from tecton_spark.partial_aggregations import TEMPORAL_ANCHOR_COLUMN_NAME
from tecton_spark.pipeline_helper import pipeline_to_dataframe
from tecton_spark.time_utils import convert_timedelta_for_version
from tecton_spark.time_utils import convert_timestamp_to_epoch

MATERIALIZED_RAW_DATA_END_TIME = "_materialized_raw_data_end_time"


@attr.s(auto_attribs=True)
class MaterializationPlan(object):
    offline_store_data_frame: Optional[DataFrame]
    online_store_data_frame: Optional[DataFrame]
    # should be the most recent ancestor of both online and offline so we can cache both of them easily
    base_data_frame: Optional[DataFrame]
    coalesce: int


def get_batch_materialization_plan(
    *,
    spark: SparkSession,
    feature_definition: FeatureDefinition,
    feature_data_time_limits: Optional[pendulum.Period],
    coalesce: int,
    data_sources: List[VirtualDataSource],
    called_for_online_feature_store: bool = False,
    transformations: Optional[List[Transformation]] = None,
    schedule_interval: Optional[pendulum.Duration] = None,
    validate_feature_timestamps: bool = True,
) -> MaterializationPlan:
    """
    NOTE: We rely on Spark's lazy evaluation model to infer partially materialized tile Schema during FeatureView
    creation time without actually performing any materialization.
    Please make sure to not perform any Spark operations under this function's code path that will actually execute
    the Spark query (e.g: df.count(), df.show(), etc.).
    """

    if feature_definition.is_temporal_aggregate:
        return _get_batch_materialization_plan_for_aggregate_feature_view(
            spark,
            feature_definition,
            False,
            feature_data_time_limits,
            data_sources,
            transformations or [],
            coalesce,
            validate_feature_timestamps,
            schedule_interval=schedule_interval,
        )
    elif feature_definition.is_temporal:
        assert feature_data_time_limits is not None
        return _get_batch_materialization_plan_for_temporal_feature_view(
            spark,
            feature_definition,
            False,
            feature_data_time_limits,
            data_sources,
            transformations or [],
            coalesce,
            called_for_online_feature_store,
            validate_feature_timestamps,
            schedule_interval=schedule_interval,
        )
    else:
        raise ValueError(f"Unhandled feature view: {feature_definition.fv}")


def _get_batch_materialization_plan_for_aggregate_feature_view(
    spark: SparkSession,
    feature_definition: FeatureDefinition,
    consume_streaming_data_sources: bool,
    feature_data_time_limits: Optional[pendulum.Period],
    data_sources: List[VirtualDataSource],
    transformations: List[Transformation],
    coalesce: int,
    validate_feature_timestamps: bool,
    schedule_interval: Optional[pendulum.Duration] = None,
) -> MaterializationPlan:
    df = pipeline_to_dataframe(
        spark,
        feature_definition.fv.pipeline,
        consume_streaming_data_sources,
        data_sources,
        transformations,
        feature_time_limits=feature_data_time_limits,
        schedule_interval=schedule_interval,
    )
    timestamp_key = feature_definition.timestamp_key
    spark_df = _possibly_apply_feature_time_limits(
        df, feature_data_time_limits, timestamp_key, validate_feature_timestamps
    )

    trailing_time_window_aggregation = feature_definition.trailing_time_window_aggregation
    online_store_df = offline_store_df = underlying_df = construct_partial_time_aggregation_df(
        spark_df,
        list(feature_definition.join_keys),
        trailing_time_window_aggregation,
        feature_definition.get_feature_store_format_version,
    )

    return MaterializationPlan(offline_store_df, online_store_df, underlying_df, coalesce)


def _get_batch_materialization_plan_for_temporal_feature_view(
    spark: SparkSession,
    feature_definition: FeatureDefinition,
    consume_streaming_data_sources: bool,
    feature_data_time_limits: pendulum.Period,
    data_sources: List[VirtualDataSource],
    transformations: List[Transformation],
    coalesce: int,
    called_for_online_feature_store: bool,
    validate_feature_timestamps: bool,
    schedule_interval: Optional[pendulum.Duration] = None,
):
    offline_store_df, online_store_df, underlying_df = _materialize_interval_for_temporal_feature_view(
        spark,
        feature_definition,
        feature_data_time_limits,
        data_sources,
        transformations,
        called_for_online_feature_store,
        consume_streaming_data_sources,
        validate_feature_timestamps,
        schedule_interval=schedule_interval,
    )

    return MaterializationPlan(offline_store_df, online_store_df, underlying_df, coalesce)


def _materialize_interval_for_temporal_feature_view(
    spark: SparkSession,
    fd: FeatureDefinition,
    feature_data_time_limits: pendulum.Period,
    data_sources: List[VirtualDataSource],
    transformations: List[Transformation],
    called_for_online_feature_store: bool,
    consume_streaming_data_sources: bool,
    validate_feature_timestamps: bool,
    schedule_interval: Optional[pendulum.Duration] = None,
) -> Tuple[DataFrame, DataFrame, DataFrame]:
    tile_df = pipeline_to_dataframe(
        spark,
        fd.pipeline,
        consume_streaming_data_sources,
        data_sources,
        transformations,
        feature_time_limits=feature_data_time_limits,
        schedule_interval=schedule_interval,
    )

    timestamp_key = fd.timestamp_key
    tile_df = _possibly_apply_feature_time_limits(
        tile_df, feature_data_time_limits, timestamp_key, validate_feature_timestamps
    )
    cacheable_df = tile_df

    # We infer partition column (i.e. anchor time) by looking at the feature timestamp column and grouping
    # all the features within `[anchor_time,  anchor_time + batch_schedule)` together.
    version = fd.get_feature_store_format_version
    anchor_time_val = convert_timestamp_to_epoch(functions.col(timestamp_key), version)
    batch_mat_schedule = convert_timedelta_for_version(fd.batch_materialization_schedule, version)
    offline_store_tile_df = tile_df.withColumn(
        TEMPORAL_ANCHOR_COLUMN_NAME, anchor_time_val - anchor_time_val % batch_mat_schedule
    )

    if called_for_online_feature_store:
        # Add raw data end time as a column as it's used for status reporting while writing to Online Feature Store.
        # When materializing multiple tiles, include `raw_data_end_time` per tile so that we can distribute writing
        # to Kafka into multiple partitions.
        online_store_tile_df = offline_store_tile_df.withColumn(
            MATERIALIZED_RAW_DATA_END_TIME, functions.col(TEMPORAL_ANCHOR_COLUMN_NAME) + batch_mat_schedule
        ).drop(TEMPORAL_ANCHOR_COLUMN_NAME)
    else:
        online_store_tile_df = tile_df

    return offline_store_tile_df, online_store_tile_df, cacheable_df


def _possibly_apply_feature_time_limits(
    spark_df,
    feature_data_time_limits: Optional[pendulum.Period],
    timestamp_key: Optional[str],
    validate_feature_timestamps: bool = True,
):
    # Apply time filter here if any of the DS for this FV does not contain the time column field
    # The reason being that if all DS contains time column fields then the time filter is already applied everywhere on
    # the raw data level.
    if feature_data_time_limits:
        # TODO(amargvela: 09/07/2021): Reenable time filtering checks.
        if validate_feature_timestamps:

            def validate_time_limits(ts):
                if (
                    not feature_data_time_limits.start
                    <= ts.replace(tzinfo=pendulum.timezone("UTC"))
                    < feature_data_time_limits.end
                ):
                    raise TectonFeatureTimeError(
                        timestamp_key, ts, feature_data_time_limits.start, feature_data_time_limits.end
                    )
                else:
                    return True

            udf_checker = udf(validate_time_limits, BooleanType())
            # force the output of the udf to be filtered on, so udf cannot be optimized away
            spark_df = spark_df.where(udf_checker(functions.col(timestamp_key)))

    return spark_df


def get_stream_materialization_plan(
    spark: SparkSession,
    data_sources: List[VirtualDataSource],
    transformations: List[Transformation],
    feature_definition: FeatureDefinition,
) -> MaterializationPlan:
    transformations = transformations or []

    df = None
    if feature_definition:
        df = pipeline_to_dataframe(spark, feature_definition.pipeline, True, data_sources, transformations)
        if feature_definition.is_temporal_aggregate:
            df = construct_partial_time_aggregation_df(
                df,
                list(feature_definition.join_keys),
                feature_definition.trailing_time_window_aggregation,
                feature_definition.get_feature_store_format_version,
            )

    return MaterializationPlan(None, df, df, 0)
