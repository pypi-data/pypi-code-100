# coding=utf-8
# Copyright 2021 The RecSim Authors.
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

# python3
"""Tests for recsim_ng.applications.latent_variable_model_learning."""
from recsim_ng.applications.latent_variable_model_learning import simulation_config
from recsim_ng.core import network as network_lib
from recsim_ng.lib.tensorflow import log_probability
from recsim_ng.lib.tensorflow import runtime
import tensorflow as tf


class LatentVariableModelTest(tf.test.TestCase):

  def setUp(self):
    super(LatentVariableModelTest, self).setUp()
    tf.random.set_seed(0)

  def test_log_probability(self):
    horizon = 6
    variables = simulation_config.create_latent_variable_model_network(
        num_users=5, num_topics=3, slate_size=4)
    network = network_lib.Network(variables=variables)
    tf_runtime = runtime.TFRuntime(network)
    traj = tf_runtime.trajectory(horizon)
    log_prob = log_probability.log_probability_from_value_trajectory(
        variables=variables, value_trajectory=traj, num_steps=horizon - 1)
    self.assertLess(log_prob, 0.0)

  def test_log_probability2(self):
    horizon = 6
    variables = simulation_config.create_latent_variable_model_network(
        num_users=5, num_topics=3, slate_size=4)
    data_generation_network = network_lib.Network(variables=variables)
    tf_runtime = runtime.TFRuntime(data_generation_network)
    traj = tf_runtime.trajectory(horizon)

    initial_sensitivity = tf.Variable(
        [0.1, 0.2, 0.3, 0.4, 0.5],
        dtype=tf.float32,
        constraint=lambda x: tf.clip_by_value(x, 0.0, 1.0))
    variables = simulation_config.create_latent_variable_model_network(
        num_users=5,
        num_topics=3,
        slate_size=4,
        satisfaction_sensitivity=initial_sensitivity)
    log_prob = log_probability.log_probability_from_value_trajectory(
        variables=variables, value_trajectory=traj, num_steps=horizon - 1)
    self.assertLess(log_prob, 0.0)


if __name__ == '__main__':
  tf.test.main()
