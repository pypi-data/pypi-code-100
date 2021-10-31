# coding=utf-8

import tensorflow as tf

from mammut.models.parameter_node import ParameterNode
from mammut.models.worker_node import WorkerNode
from mammut.models.reparameterization import gumbel


class ObservedUtilityEstimatorNode(ParameterNode):
    def __init__(
        self,
        padding,
        state_free_dimension_choices,
        state_size,
        scope_name,
        configuration_path,
        configuration_name,
        task_index,
        redis_connection_pool,
    ):
        ParameterNode.__init__(
            self,
            scope_name,
            configuration_path,
            configuration_name,
            task_index,
            redis_connection_pool,
        )
        self.size = state_size - self.state_size_reduction
        self.free_dimension_choices = state_free_dimension_choices
        # The size of the linear regressor must be the same as the output of the convolution operation
        if padding == "VALID":
            self.linear_regressor_size = state_size - self.size + 1
        else:
            self.linear_regressor_size = state_size

    state_size_reduction = ParameterNode._add_configuration_property(
        "ObservedUtilityEstimatorNode",
        "state_size_reduction",
        1,
        int,
        "The size of the filter is the state_size - state_size_reduction.",
    )

    def _operation(self, *args, **kwargs):
        filters = []
        options_list = []
        for i in range(0, self.free_dimension_choices):
            # This is a filter to use with conv1d that expects a filter / kernel tensor of shape
            # [filter_width, in_channels, out_channels]
            filters.append(
                tf.Variable(
                    tf.truncated_normal(
                        [self.size, 1, 1],
                        mean=0.0,
                        stddev=0.1,
                        dtype=tf.float32,
                        seed=21,
                        name="init-filter",
                    ),
                    name="utility-paramters-convolution-filter-{}".format(i),
                )
            )
            options_list.append(float(i))
        linear_regressor = tf.Variable(
            tf.truncated_normal(
                [self.linear_regressor_size],
                mean=0.0,
                stddev=0.1,
                dtype=tf.float32,
                seed=21,
                name="init-linear-regressor",
            ),
            name="linear-utility-m",
        )
        options = tf.constant(options_list, dtype=tf.float32, name="options")
        temperature = tf.Variable(0.1, name="temperature", trainable=False)
        return [filters, linear_regressor, options, temperature]


class LexicalDiscreteChoiceNode(WorkerNode):
    def __init__(
        self,
        one_hot_output,
        intermediate_node,
        state_free_dimension,
        state_free_dimension_choices,
        state_size,
        scope_name,
        configuration_path,
        configuration_name,
        task_index,
        redis_connection_pool=None,
    ):
        WorkerNode.__init__(
            self,
            scope_name,
            configuration_path,
            configuration_name,
            task_index,
            redis_connection_pool,
        )
        self.use_one_hot_output = one_hot_output
        self.is_intermediate_node = intermediate_node
        self.free_dimension = state_free_dimension
        self.free_dimension_choices = state_free_dimension_choices
        self.state_size = state_size
        self.observed_utility_estimator = ObservedUtilityEstimatorNode(
            self.padding,
            self.free_dimension_choices,
            self.state_size,
            scope_name,
            configuration_path,
            configuration_name,
            task_index,
            redis_connection_pool,
        )
        (
            self.filters,
            self.linear_regressor,
            self.options,
            self.temperature,
        ) = self.observed_utility_estimator()

    padding = ParameterNode._add_configuration_property(
        "LexicalDiscretChoiceNode",
        "padding",
        "SAME",
        None,
        "The padding parameter of the tf.nn.conv2d method.",
    )
    output_size = ParameterNode._add_configuration_property(
        "LexicalDiscretChoiceNode",
        "output_size",
        1,
        int,
        "The amount of options in the output. The options is a ordered vector",
    )

    def _operation(self, *args, **kwargs):
        # Extract the input state and reshaped as one vector
        x = args[0]
        # This is the input tensor of shape [batch, in_width, in_channels] expected for conv1d
        x = tf.to_float(tf.reshape(x, [-1, self.state_size, 1]))

        # Compute the utility of each option
        utility_options = []
        for i in range(0, self.free_dimension_choices):
            # Applies the filter to the input state in order to obtain the utility parameters of the state for the option i
            utility_parameters = tf.nn.conv1d(
                x,
                self.filters[i],
                stride=1,
                padding=self.padding,
                data_format="NWC",
                name="convolution",
            )
            utility_parameters = tf.reshape(
                utility_parameters, [-1, tf.shape(self.linear_regressor)[0]]
            )
            # Compute the observed utility. Its a vector of [batch_size]
            observed_utility = tf.reduce_sum(
                self.linear_regressor * utility_parameters, axis=1
            )
            utility_options.append(observed_utility)
        utility_options_tensor = tf.stack(
            utility_options, axis=1, name="utility_options"
        )

        # Compute the probability of each option
        options_probabilities = tf.nn.softmax(utility_options_tensor, name="logit")

        # Compute the selected option using Gumbel-Max Trick if you are using the output as input of another node
        if self.is_intermediate_node:
            if self.use_one_hot_output:
                output = gumbel.gumbel_softmax(
                    utility_options_tensor, self.temperature, hard=True
                )
            else:
                output = gumbel.gumbel_softmax_option(
                    utility_options_tensor, self.temperature, self.options
                )
        else:
            output = tf.argmax(options_probabilities, 1)
            if self.use_one_hot_output:
                output = tf.one_hot(output, self.free_dimension_choices)
        return [output, options_probabilities, utility_options_tensor]
