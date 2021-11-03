"""Integration tests for functionality related to model conversion."""
from typing import Generator
from test.common.common_models import setup_keras_model_functional
from test.common.common_test_setup import TempDirTestSetup

import pytest

from czmodel.model_metadata import ModelMetadata, ModelSpec, ModelType
from czmodel.legacy_model_metadata import (
    ModelMetadata as LegacyModelMetadata,
    ModelSpec as LegacyModelSpec,
)
from czmodel.convert import DefaultConverter, LegacyConverter

# pylint: disable=import-outside-toplevel


@pytest.fixture(name="setup_env")
def fixture_setup_env() -> Generator[TempDirTestSetup, None, None]:
    """Setup fixture to initialize the test environment."""
    with TempDirTestSetup() as ts:
        yield ts


def test_czann_workflow(setup_env: TempDirTestSetup) -> None:
    """Tests if the entire czann export workflow generates a .czann file.

    Arguments:
        setup_env: The test environment.
    """
    import os

    # ARRANGE
    license_path = os.path.join(setup_env.test_dir, "license.txt")
    output_path = os.path.join(setup_env.test_dir, "exported_model")
    output_name = "exported_model.czann"
    with open(license_path, "w", encoding="utf-8") as f:
        f.write("This file contains some license.")
    model_spatial_dims = 128, 128
    model = setup_keras_model_functional(spatial_dims=model_spatial_dims)
    model_metadata = ModelMetadata(
        input_shape=list(model_spatial_dims) + [3],
        output_shape=list(model_spatial_dims) + [3],
        model_type=ModelType.SINGLE_CLASS_SEMANTIC_SEGMENTATION,
        classes=["class1", "class2", "class3"],
        model_name="ModelName",
        min_overlap=[90, 90],
    )
    model_spec = ModelSpec(model=model, model_metadata=model_metadata, license_file=license_path)

    # ACT
    DefaultConverter().convert_from_model_spec(model_spec=model_spec, output_path=output_path, output_name=output_name)

    # ASSERT
    os.path.isfile(os.path.join(output_path, output_name))


def test_czmodel_workflow(setup_env: TempDirTestSetup) -> None:
    """Tests if the entire czmodel export workflow generates a .czseg file.

    Arguments:
        setup_env: The test environment.
    """
    import os

    # ARRANGE
    license_path = os.path.join(setup_env.test_dir, "license.txt")
    with open(license_path, "w", encoding="utf-8") as f:
        f.write("This file contains some license.")
    output_path = os.path.join(setup_env.test_dir, "exported_model")
    output_name = "exported_model.czseg"
    model_spatial_dims = 128, 128
    model = setup_keras_model_functional(spatial_dims=model_spatial_dims)
    model_metadata = LegacyModelMetadata(
        name="DNNModel",
        color_handling="ConvertToMonochrome",
        pixel_types=["Gray16"],
        classes=["Background", "Interesting Object", "Foreground"],
        border_size=90,
    )
    model_spec = LegacyModelSpec(model=model, model_metadata=model_metadata, license_file=license_path)

    # ACT
    LegacyConverter().convert_from_model_spec(model_spec=model_spec, output_path=output_path, output_name=output_name)

    # ASSERT
    os.path.isfile(os.path.join(output_path, output_name))
