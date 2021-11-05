# Copyright 2021 The Kubeflow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Launcher module for dataflow componeonts."""

from google_cloud_pipeline_components.container.experimental.dataflow import dataflow_launcher
import json

argv = [
              "--project",
              "tfe-ecosystem-dev",
              "--location",
              "us-central1",
              "--python_module_path",
              "gs://ml-pipeline-playground/samples/dataflow/wc/wc.py",
              "--temp_location",
              "gs://sina-dev",
              "--requirements_file_path",
              "gs://ml-pipeline-playground/samples/dataflow/wc/requirements.txt",
              "--args",
              json.dumps(["--output", "gs://sina-dev/wc/wordcount.out"]),
              "--gcp_resources",
              "/tmp/test_dataflow"
            ]

dataflow_launcher.main(argv)