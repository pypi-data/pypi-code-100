from datetime import datetime
from typing import Dict
from typing import Optional
from typing import Union

import pandas
import pendulum
from pyspark.sql import DataFrame

import tecton
from tecton._internals import errors
from tecton.tecton_context import TectonContext
from tecton_proto.args.feature_view_pb2 import BackfillConfigMode
from tecton_proto.data import feature_view_pb2
from tecton_spark import materialization_plan
from tecton_spark import time_utils
from tecton_spark.aggregation_plans import get_aggregation_plan
from tecton_spark.aggregation_utils import get_aggregation_function_name
from tecton_spark.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_spark.id_helper import IdHelper
from tecton_spark.partial_aggregations import construct_partial_time_aggregation_df
from tecton_spark.pipeline_helper import get_all_input_ds_id_map
from tecton_spark.pipeline_helper import get_all_input_keys
from tecton_spark.pipeline_helper import pipeline_to_dataframe
from tecton_spark.pipeline_helper import run_mock_pandas_pipeline
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


def run_batch(
    fv_proto: feature_view_pb2.FeatureView,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_end_time: Optional[Union[pendulum.DateTime, datetime]],
    mock_inputs: Dict[str, Union[pandas.DataFrame, DataFrame]],
    aggregate_tiles: bool = None,
) -> "tecton.interactive.data_frame.DataFrame":
    spark = TectonContext.get_instance()._spark
    # Validate that mock_inputs' keys.
    input_ds_id_map = get_all_input_ds_id_map(fv_proto.pipeline.root)
    _validate_batch_mock_inputs_keys(mock_inputs, fv_proto)

    schedule_interval = time_utils.proto_to_duration(fv_proto.materialization_params.schedule_interval)
    # Smart default feature_start_time and feature_end_time if unset.
    if feature_end_time is None:
        feature_end_time = pendulum.now()
    if feature_start_time is None:
        feature_start_time = feature_end_time - schedule_interval
    feature_time_limits_aligned = _align_times(feature_start_time, feature_end_time, fv_proto, schedule_interval)

    _validate_feature_time_for_backfill_config(
        fv_proto, feature_start_time, feature_end_time, feature_time_limits_aligned
    )

    # Convert any Pandas dataFrame mock_inputs to Spark, validate schema columns.
    # TODO(raviphol): Consider refactor this under pipeline_helper._node_to_value
    for key in mock_inputs.keys():
        ds = _get_ds_by_id(fv_proto.enrichments.virtual_data_sources, input_ds_id_map[key])
        spark_schema = _get_spark_schema(ds)

        if isinstance(mock_inputs[key], pandas.DataFrame):
            mock_inputs[key] = spark.createDataFrame(mock_inputs[key])

        _validate_input_dataframe_schema(input_name=key, dataframe=mock_inputs[key], spark_schema=spark_schema)

    # Execute Spark pipeline to get output DataFrame.
    materialized_spark_df = pipeline_to_dataframe(
        spark,
        pipeline=fv_proto.pipeline,
        consume_streaming_data_sources=False,
        data_sources=fv_proto.enrichments.virtual_data_sources,
        transformations=fv_proto.enrichments.transformations,
        feature_time_limits=feature_time_limits_aligned,
        schedule_interval=pendulum.Duration(seconds=fv_proto.materialization_params.schedule_interval.ToSeconds()),
        mock_inputs=mock_inputs,
    )

    fd = FeatureDefinition(fv_proto)
    # If aggregate_tiles is set, aggregates the output rows into corresponding aggregate-tiles.
    # Please note that this will not perform the 2nd rollup to FeatureAggregation time windows.
    if aggregate_tiles:
        if fd.trailing_time_window_aggregation.is_continuous:
            raise errors.TectonValidationError(
                "aggregate_tiles=True is not supported for this FeatureView, as it has a slide interval set to "
                + "continuous. This means all aggregation is done online and there are no pre-aggregated tiles."
            )
        materialized_spark_df = construct_partial_time_aggregation_df(
            materialized_spark_df,
            list(fv_proto.join_keys),
            fd.trailing_time_window_aggregation,
            fv_proto.feature_store_format_version,
            window_start_column_name="tile_start_time",
            window_end_column_name="tile_end_time",
            convert_to_epoch=False,
        )
        # Intermediate-rollup output columns will be renamed to use the similar pattern as final aggregated columns.
        materialized_spark_df = _rename_intermediate_aggregate_columns(materialized_spark_df, fd)

    if not (fd.is_temporal_aggregate and aggregate_tiles):
        # Filter output rows which are not within feature time range. This won't apply if aggregate_tiles is set,
        # because aggregated output rows won't correspond to a timestamp, but instead aggregated into the time window.
        materialized_spark_df = materialized_spark_df.filter(
            materialized_spark_df[fd.timestamp_key] >= feature_start_time
        )
        materialized_spark_df = materialized_spark_df.filter(materialized_spark_df[fd.timestamp_key] < feature_end_time)

    return tecton.interactive.data_frame.DataFrame._create(materialized_spark_df)


def run_stream(fv_proto: feature_view_pb2.FeatureView, output_temp_table: str) -> None:
    plan = materialization_plan.get_stream_materialization_plan(
        TectonContext.get_instance()._spark,
        data_sources=fv_proto.enrichments.virtual_data_sources,
        transformations=fv_proto.enrichments.transformations,
        feature_definition=FeatureDefinition(fv_proto),
    )
    spark_df = plan.online_store_data_frame
    spark_df.writeStream.format("memory").queryName(output_temp_table).outputMode("append").start()


def run_ondemand(
    fv_proto: feature_view_pb2.FeatureView, fv_name: str, mock_inputs: Dict[str, Union[pandas.DataFrame, DataFrame]]
) -> "tecton.interactive.data_frame.DataFrame":  # a single row:
    for key in mock_inputs:
        if isinstance(mock_inputs[key], DataFrame):
            mock_inputs[key] = mock_inputs[key].toPandas()

    # Validate that all the mock_inputs matchs with FV inputs, and that num rows match across all mock_inputs.
    _validate_ondemand_mock_inputs_keys(mock_inputs, fv_proto)

    # Execute Pandas pipeline to get output DataFrame.
    return tecton.interactive.data_frame.DataFrame._create(
        run_mock_pandas_pipeline(
            name=fv_name,
            pipeline=fv_proto.pipeline,
            transformations=fv_proto.enrichments.transformations,
            mock_inputs=mock_inputs,
        )
    )


def _rename_intermediate_aggregate_columns(df: DataFrame, fd: FeatureDefinition) -> DataFrame:
    # Create a map from intermediate rollup column name to preferred column names.
    renaming_map = dict()
    slide_interval_string = fd.get_aggregate_slide_interval_string
    for feature in fd.trailing_time_window_aggregation.features:
        aggregation_plan = get_aggregation_plan(
            feature.function, feature.function_params, fd.trailing_time_window_aggregation.is_continuous
        )
        aggregation_function_name = get_aggregation_function_name(feature.function)
        for old_name in aggregation_plan.materialized_column_names(feature.input_feature_name):
            renaming_map[old_name] = f"{feature.input_feature_name}_{aggregation_function_name}_{slide_interval_string}"
    for (old_name, new_name) in renaming_map.items():
        df = df.withColumnRenamed(old_name, new_name)
    return df


# For single-batch-schedule-interval-per-job backfill, validate the followings.
# - Only support single-tile run.
# - Don't allow passing `feature_start_time` without feature_end_time since it may be confusing that the tile time
#   range goes into the future.
def _validate_feature_time_for_backfill_config(
    fv_proto: feature_view_pb2.FeatureView,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_end_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_time_limits_aligned: pendulum.Period,
):
    # TODO(raviphol): Use utils.is_bfc_mode_single once D9614 is landed.
    if not fv_proto.HasField("temporal"):
        return
    if not fv_proto.temporal.HasField("backfill_config"):
        return
    backfill_config_mode = fv_proto.temporal.backfill_config.mode
    if backfill_config_mode is not BackfillConfigMode.BACKFILL_CONFIG_MODE_SINGLE_BATCH_SCHEDULE_INTERVAL_PER_JOB:
        return

    if feature_start_time and not feature_end_time:
        raise errors.BFC_MODE_SINGLE_REQUIRED_FEATURE_END_TIME_WHEN_START_TIME_SET

    schedule_interval_seconds = fv_proto.materialization_params.schedule_interval.ToSeconds()
    if schedule_interval_seconds == 0:
        raise errors.INTERNAL_ERROR("Materialization schedule interval not found.")

    num_tile = feature_time_limits_aligned.in_seconds() // schedule_interval_seconds
    if num_tile > 1:
        raise errors.BFC_MODE_SINGLE_INVALID_FEATURE_TIME_RANGE


# Validate that mock_inputs keys are a subset of data sources.
def _validate_batch_mock_inputs_keys(mock_inputs, fv_proto):
    expected_input_names = get_all_input_keys(fv_proto.pipeline.root)
    mock_inputs_keys = set(mock_inputs.keys())
    if not mock_inputs_keys.issubset(expected_input_names):
        raise errors.FV_INVALID_MOCK_INPUTS(mock_inputs_keys, expected_input_names)


# Validate that mock_inputs keys are exact match with expected inputs.
def _validate_ondemand_mock_inputs_keys(mock_inputs, fv_proto):
    expected_input_names = get_all_input_keys(fv_proto.pipeline.root)
    mock_inputs_keys = set(mock_inputs.keys())
    if mock_inputs_keys != expected_input_names:
        raise errors.FV_INVALID_MOCK_INPUTS(mock_inputs_keys, expected_input_names)
    # Get num row for all FV mock_inputs, to validate that they match.
    num_rows = [len(mock_inputs[key].index) for key in mock_inputs]
    if len(set(num_rows)) > 1:
        raise errors.FV_INVALID_MOCK_INPUTS_NUM_ROWS(num_rows)


# Check that schema of each mock inputs matches with data sources.
def _validate_input_dataframe_schema(input_name, dataframe: DataFrame, spark_schema):
    columns = sorted(dataframe.columns)
    expected_column_names = sorted([field.name for field in spark_schema.fields])

    # Validate mock input's schema against expected schema.
    if not expected_column_names == columns:
        raise errors.FV_INVALID_MOCK_INPUT_SCHEMA(input_name, columns, expected_column_names)


def _get_ds_by_id(data_sources, id: str):
    for ds in data_sources:
        if IdHelper.to_string(ds.virtual_data_source_id) == id:
            return ds
    return None


# Align feature start and end times with materialization schedule interval.
def _align_times(feature_start_time, feature_end_time, fv_proto, schedule_interval):
    # Align feature_end_time upward to the nearest materialization schedule interval.
    feature_end_time = time_utils.align_time_upwards(feature_end_time, schedule_interval)

    # Align feature_start_time downward to the nearest materialization schedule interval.
    feature_start_time = time_utils.align_time_downwards(feature_start_time, schedule_interval)
    return pendulum.period(feature_start_time, feature_end_time)


def _get_spark_schema(ds):
    if ds.HasField("batch_data_source"):
        spark_schema = ds.batch_data_source.spark_schema
    elif ds.HasField("stream_data_source"):
        spark_schema = ds.stream_data_source.spark_schema
    else:
        raise errors.INTERNAL_ERROR("DataSource is missing a supporting config")
    return SparkSchemaWrapper.from_proto(spark_schema).unwrap()
