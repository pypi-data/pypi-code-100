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
"""User entity for the simulation of learning latent variable models."""
import edward2 as ed  # type: ignore
import gin
from gym import spaces
import numpy as np
from recsim_ng.core import value
from recsim_ng.entities.choice_models import affinities
from recsim_ng.entities.choice_models import selectors
from recsim_ng.entities.recommendation import user
from recsim_ng.entities.state_models import static
from recsim_ng.lib.tensorflow import entity
import tensorflow as tf

Value = value.Value
ValueSpec = value.ValueSpec
Space = value.Space


@gin.configurable
class ModelLearningDemoUser(entity.Entity, user.User):
  """User model with embedding target intent, satisfaction, and curiosity.

  This entity models a user which interacts with a recommender system by
  repeatedly selecting items among slates of items. The user's action
  space consists of:
    * selecting one of k presented items for consumption
    * selecting one of k presented items for exploration
    * terminating the session.
  The user's state consists of:
    * a curiosity parameter c
    * an intent realized by a target item
    * a dynamic satisfaction s, which reflects the user's impression of whether
      the recommender makes progress towards the target
    * an acceptance threshold t.
  The user's choice process proceeds as follows:
    1. the user tries to select a document for consumption, using the item
       utilities as logits. The possibility of not consuming is also added with
       logit equal to t. If a document is selected for consumption, the session
       ends.
    2. Users who do not pick an item for consumption decide whether to explore
       further. The exploration decision is made with probability sigmoid(c * s)
       that is, more satisfied users are likely to explore further.
    3. If the user decides to explore, a document from the slate is selected for
       exploration, this time without the no-choice option. Otherwise the
       session terminates.
  The user state updates as follows:
    * if the decision to end the session has been made during the choice
      process, all state variables are redrawn from their initial distributions.
    * The target, threshold, and curiosity remain fixed over time.
    * The satisfaction s evolves as:
          s_t = satisfaction_sensitivity * s_{t-1} + delta_t + eps,
      where delta_t is difference between the maximum utility of the items from
      the t-slate and that of the (t-1)-slate, and eps is zero-mean Gaussian
      noise with std=0.3.
  """

  def __init__(self,
               config,
               affinity_model_ctor=affinities.TargetPointSimilarity,
               choice_model_ctor=selectors.MultinormialLogitChoiceModel,
               user_intent_variance=0.1,
               satisfaction_sensitivity=None,
               initial_satisfication=5.0,
               name='ModelLearningDemoUser'):
    user.User.__init__(self, config)
    entity.Entity.__init__(self, name=name)
    self._slate_size = config['slate_size']
    self._user_intent_variance = user_intent_variance
    if satisfaction_sensitivity is None:
      self._sat_sensitivity = 0.8 * tf.ones(self._num_users)
    else:
      self._sat_sensitivity = satisfaction_sensitivity
    self._initial_satisfication = initial_satisfication
    # Sample from a number of user intents.
    self._num_intents = config['num_topics']
    batch_intent_means = tf.eye(
        self._num_intents,
        num_columns=self._num_topics,
        batch_shape=(self._num_users,))
    lop_ctor = lambda params: tf.linalg.LinearOperatorScaledIdentity(  # pylint: disable=g-long-lambda
        num_rows=self._num_topics,
        multiplier=params)
    self._intent_model = static.GMMVector(
        batch_ndims=1,
        mixture_logits=tf.zeros((self._num_users, self._num_intents)),
        component_means=batch_intent_means,
        component_scales=tf.sqrt(self._user_intent_variance),
        linear_operator_ctor=lop_ctor)
    self._choice_model = choice_model_ctor(
        batch_shape=(self._num_users,),
        nochoice_logits=tf.zeros(self._num_users))
    self._affinity_model = affinity_model_ctor((self._num_users,),
                                               self._num_topics)
    self._response_spec = self._choice_model.specs()
    self._state_spec = ValueSpec(
        intent=self._intent_model.specs().get('state'),
        satisfaction=Space(
            spaces.Box(low=-np.Inf, high=np.Inf, shape=(self._num_users,))),
        max_slate_utility=Space(
            spaces.Box(low=-np.Inf, high=np.Inf, shape=(self._num_users,))))

  def initial_state(self):
    """The state value after the initial value."""
    return Value(
        satisfaction=self._initial_satisfication * tf.ones(self._num_users),
        intent=self._intent_model.initial_state().get('state'),
        max_slate_utility=ed.Deterministic(loc=tf.zeros(self._num_users)))

  def next_state(self, previous_state, _, slate_docs):
    """The state value after the initial value."""
    # Compute the improvement of slate scores.
    slate_doc_features = slate_docs.get('features')
    slate_doc_affinities = self._affinity_model.affinities(
        previous_state.get('intent'), slate_doc_features).get('affinities')
    max_slate_utility = tf.reduce_max(slate_doc_affinities, axis=-1)
    improvement = max_slate_utility - previous_state.get('max_slate_utility')
    next_satisfaction = self._sat_sensitivity * previous_state.get(
        'satisfaction') + improvement
    return Value(
        satisfaction=next_satisfaction,
        intent=self._intent_model.next_state(
            Value(state=previous_state.get('intent'))).get('state'),
        max_slate_utility=ed.Deterministic(max_slate_utility))

  def next_response(self, previous_state, slate_docs):
    """The response value after the initial value."""
    slate_doc_features = slate_docs.get('features')
    slate_doc_scores = self._affinity_model.affinities(
        previous_state.get('intent'), slate_doc_features).get('affinities')
    adjusted_scores = (
        slate_doc_scores +
        tf.expand_dims(previous_state.get('satisfaction'), axis=-1))
    return self._choice_model.choice(adjusted_scores)

  def observation(self):
    pass
