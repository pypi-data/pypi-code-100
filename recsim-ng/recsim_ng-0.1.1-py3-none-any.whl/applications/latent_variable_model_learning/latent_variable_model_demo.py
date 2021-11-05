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
from absl import app
import numpy as np

from recsim_ng.applications.latent_variable_model_learning import simulation_config
from recsim_ng.core import network as network_lib
from recsim_ng.lib.tensorflow import entity
from recsim_ng.lib.tensorflow import log_probability
from recsim_ng.lib.tensorflow import runtime
import tensorflow as tf


def main(argv):
  del argv
  variables = simulation_config.create_latent_variable_model_network(
      num_users=5, num_topics=3, slate_size=4)
  data_generation_network = network_lib.Network(variables=variables)

  initial_sensitivity = tf.Variable(
      np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
      dtype=tf.float32,
      constraint=lambda x: tf.clip_by_value(x, 0.0, 1.0))
  story = lambda: simulation_config.create_latent_variable_model_network(
      num_users=5,
      num_topics=3,
      slate_size=4,
      satisfaction_sensitivity=initial_sensitivity)
  trainable_vars = entity.trainable_variables(story)['ModelLearningDemoUser']

  horizon = 6
  optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)
  t_vars = story()
  for _ in range(100):
    tf_runtime = runtime.TFRuntime(network=data_generation_network)
    traj = tf_runtime.trajectory(length=horizon)
    with tf.GradientTape() as tape:
      obs = log_probability.observation_variables(t_vars, traj)
      replay = log_probability.replay_variables(t_vars, obs)
      lpvars = log_probability.log_prob_variables(replay)
      disagg_runtime = runtime.TFRuntime(
          network=network_lib.Network(replay + obs + lpvars))
      distraj = disagg_runtime.trajectory(length=horizon)
      print(distraj)
      print(distraj['user response_log_prob'])
      objective = -tf.reduce_sum(
          distraj['user response_log_prob'].get('choice'))
      # objective = -log_probability.log_probability_from_value_trajectory(
      #     variables=story(), value_trajectory=traj, num_steps=horizon - 1)
      # tf.print(objective)
    print(trainable_vars)
    print(initial_sensitivity)
    grads = tape.gradient(objective, trainable_vars)
    print(grads)
    optimizer.apply_gradients(zip(grads, trainable_vars))


if __name__ == '__main__':
  app.run(main)
