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
"""Recs simulation story."""
from typing import Any, Callable, Collection, Mapping, Text, Tuple, Union
from recsim_ng.core import variable
from recsim_ng.entities.recommendation import recommender as recommender_lib
from recsim_ng.entities.recommendation import user as user_lib

Variable = variable.Variable
Config = Mapping[Text, Any]
Recommender = recommender_lib.BaseRecommender
User = user_lib.User


def recs_story(
    config, user_ctor,
    recommender_ctor
):
  """A simple recommendation story."""
  # Construct entities.
  user = user_ctor(config)
  recommender = recommender_ctor(config)

  # Variables.
  user_response = Variable(name='user response', spec=user.response_spec)
  user_state = Variable(name='user state', spec=user.state_spec)
  slate_docs = Variable(name='slate docs', spec=recommender.slate_docs_spec)

  # 0. Initial state.
  user_state.initial_value = variable.value(user.initial_state)
  slate_docs.initial_value = variable.value(recommender.slate_docs)
  user_response.initial_value = variable.value(user.next_response,
                                               (user_state, slate_docs))

  # 1. Update user state.
  user_state.value = variable.value(
      user.next_state,
      (user_state.previous, user_response.previous, slate_docs.previous))
  # 2. Recommender makes recommendation.
  slate_docs.value = variable.value(recommender.slate_docs)
  # 3. User responds to recommendation.
  user_response.value = variable.value(user.next_response,
                                       (user_state, slate_docs))

  return [slate_docs, user_state, user_response]
