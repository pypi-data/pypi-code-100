# coding=utf-8

import tensorflow as tf
import numpy as np

from mammut.models.parameter_node import ParameterNode
from mammut.models.worker_node import WorkerNode
from mammut.common.util import StringEnum, RegionalSettingsType


class ExecutionMode(StringEnum):
    eager = "eager"
    graph = "graph"
    differentiable = "differentiable"


class TransitionOracleMockNode(WorkerNode):
    def __init__(self):
        # TODO:cambiar nombres de parametro que se pasan a constructor de workernode
        WorkerNode.__init__(self, "worker-mx", "model-test", "worker-mx", 0, None)
        self.counter = 0
        # se sobreescribre para cada caso en las pruebas
        # transitoins debe ser un tensor
        self.transition_list = [
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
            ],
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
            ],
        ]
        self.transitions = tf.constant(
            self.transition_list, dtype=tf.float32
        )  # shape = steps, batch, numero de transiciones posibles

    def _operation(self, *args, **kwargs):
        if len(args[0]) > 1:
            if isinstance(args[0][1], tf.Tensor):
                # print('arg0', args[0][1], isinstance(args[0][1], tf.Tensor))
                transition = self.transitions[args[0][1]]
        else:
            if self.transitions.shape[0] > self.counter:
                transition = self.transitions[self.counter]
                self.counter += 1
            else:
                transition = None  # [[0,0,0,0,0,0,0,0]]
            return transition
        return transition


class OutputOracleMockNode(WorkerNode):
    def __init__(self):
        # TODO:cambiar nombres de parametro que se pasan a constructor de workernode
        WorkerNode.__init__(self, "worker-mx", "model-test", "worker-mx", 0, None)
        self.counter = 0
        # debe ser un tensor!!???
        self.outputs = [
            [[1], [2], [3]],
            [[1], [2], [3]],
        ]  # shape = steps, batch, output_value(numero de outputs posibles si fuese onehot)

    def _operation(self, *args, **kwargs):
        print("arg0", args[0])
        print("arg1", args[0][1], isinstance(args[0][1], tf.Tensor))
        if len(args[0]) > 1:
            if isinstance(args[0][1], tf.Tensor):
                print("arg0", args[0][1], isinstance(args[0][1], tf.Tensor))
                outputs = self.outputs[args[0][1]]
                self.counter += 1
            else:
                outputs = self.outputs[args[0][1]]
                self.counter += 1
        else:
            if self.outputs.shape[0] > self.counter:
                outputs = self.outputs[self.counter]
                self.counter += 1
            else:
                outputs = None  # [[0,0,0,0,0,0,0,0]]
        return outputs


class TransitionSystemConfigurations(ParameterNode):
    def __init__(
        self,
        stack_size: int,
        transition_size: int,
        output_size: int,
        input_size: int,
        batch_size: int,
        stack_position: int,
        stack_position_elems: list,
        transition_position: int,
        output_position: list,
        input_position: int,
        execution_mode: ExecutionMode,
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
        self.stack_size = stack_size  # deberia buscarse bien cual es la longitud optima, longitud de la palabra mas largs
        self.transition_size = transition_size
        self.output_size = output_size  # ids de entities, lemmas, etc, #numero de states pasados que sirven de contexto
        self.input_size = input_size
        self.batch_size = batch_size
        self.state_size = (
            self.stack_size + self.transition_size + self.output_size + self.input_size
        )
        self.stack_position = stack_position  # 0-4
        self.stack_position_elems = stack_position_elems
        self.transition_position = transition_position
        self.output_position = output_position
        self.input_position = input_position
        self.transitions = None  # transiciones a aplicar
        self.transitions_array = None
        self.step_transition = None
        # TODO: los names deberian estr hardcode???
        # TODO: en sentido estricto add_output y add_transition no son trnasiciones, se calculan al final y se suman al state resultante
        self.transition_names = [
            "shift",
            "discard",
            "delete_stack",
            "output_shift",
            "morpheme",
        ]
        self.available_transitions_len = len(
            self.transition_names
        )  # numero de transiciones posibles
        self.available_transitions = (
            self.get_one_hot_transitions()
        )  # transiciones que s epueden ejecutar
        self.execution_mode = execution_mode

    def _operation(self, *args, **kwargs):
        return

    ######### SHIFT######

    @staticmethod
    def get_selector_shift_projection(transitions, transition_unit_vector):
        transitions_number = len(transition_unit_vector)
        selector_shift_projection = tf.constant(
            [transition_unit_vector], dtype=tf.float32, shape=[transitions_number, 1]
        )  # numero de transiciones en dimension 1
        selector_shift_projection_result = tf.matmul(
            transitions, selector_shift_projection
        )
        return selector_shift_projection_result

    def get_selector_shift_filter(self, state_size):
        tensor_ones_indexes = [k for k in range(0, state_size)]
        tensor_ones_indexes = np.roll(tensor_ones_indexes, 1)

        selector_shift_filter = np.zeros([state_size, state_size])
        for i in range(0, state_size):
            if (
                i != self.transition_position
                and i not in self.output_position
                and i != self.input_position
            ):
                selector_shift_filter[i, tensor_ones_indexes[i]] = 1
            if (
                i in self.output_position
            ):  # or i == transition_position: #mantener el transtion??o conviene eliminarla de una vez
                selector_shift_filter[i, i] = 1
            if i == self.transition_position:
                selector_shift_filter[i, i] = 0
        return selector_shift_filter

    def get_selector_shift_result(
        self, transitions, transition_unit_vector, state_size
    ):
        selector_shift_projection_result = self.get_selector_shift_projection(
            transitions, transition_unit_vector
        )  # segundo es lo puedo pasar como transtions[index]
        selector_shift_filter = self.get_selector_shift_filter(state_size)

        selector_shift_filter = tf.reshape(
            tf.constant(selector_shift_filter, dtype=tf.float32),
            shape=[1, state_size, state_size],
        )
        selector_shift_projection_result_reshape = tf.reshape(
            selector_shift_projection_result,
            shape=[selector_shift_projection_result.shape[0], 1, 1],
        )
        selector_shift_result = (
            selector_shift_projection_result_reshape * selector_shift_filter
        )
        return selector_shift_result

    ##########DISCARD################

    def get_selector_clean_input_projection(self, transitions, transition_unit_vector):
        selector_clean_input_projection = tf.constant(
            [transition_unit_vector],
            dtype=tf.float32,
            shape=[self.available_transitions_len, 1],
        )
        selector_clean_input_projection_result = tf.matmul(
            transitions, selector_clean_input_projection
        )
        return selector_clean_input_projection_result

    def get_selector_clean_input_filter(self, state_size, input_position):
        selector_clean_input_filter = np.zeros([state_size, state_size])
        for i in range(0, state_size):
            if i != input_position:
                selector_clean_input_filter[i, i] = 1
            else:
                selector_clean_input_filter[i, i] = 0
            if i == self.transition_position:
                selector_clean_input_filter[i, i] = 0
        return selector_clean_input_filter

    def get_selector_clean_input_result(
        self, transitions, transition_unit_vector, state_size
    ):

        selector_clean_input_filter = self.get_selector_clean_input_filter(
            state_size, self.input_position
        )
        selector_clean_input_filter = tf.reshape(
            tf.constant(selector_clean_input_filter, dtype=tf.float32),
            shape=[1, state_size, state_size],
        )
        # print("clean_input Filter: \n %s" % (selector_clean_input_filter.eval()))
        selector_clean_input_projection_result = self.get_selector_clean_input_projection(
            transitions, transition_unit_vector
        )

        selector_clean_input_projection_result_reshape = tf.reshape(
            selector_clean_input_projection_result,
            shape=[selector_clean_input_projection_result.shape[0], 1, 1],
        )
        # print("clean_input transitions reshaped: \n %s" % (selector_clean_input_projection_result_reshape.eval()))

        selector_clean_input_projection_result = (
            selector_clean_input_projection_result_reshape * selector_clean_input_filter
        )
        # print("clean input transitions: \n %s" % selector_clean_input_projection_result.eval())
        return selector_clean_input_projection_result

    ################DELETE STACK##################

    def get_selector_delete_stack_projection(self, transitions, transition_unit_vector):
        selector_delete_stack_projection = tf.constant(
            [transition_unit_vector],
            dtype=tf.float32,
            shape=[self.available_transitions_len, 1],
        )
        selector_delete_stack_projection_result = tf.matmul(
            transitions, selector_delete_stack_projection
        )
        return selector_delete_stack_projection_result

    def get_selector_delete_stack_filter(self, state_size, stack_postion_elems):
        selector_delete_stack_filter = np.zeros([state_size, state_size])
        for i in range(0, state_size):
            if i in stack_postion_elems:
                selector_delete_stack_filter[i, i] = 0
            else:
                selector_delete_stack_filter[i, i] = 1
            if i == self.transition_position:
                selector_delete_stack_filter[i, i] = 0
        return selector_delete_stack_filter

    def get_selector_delete_stack_result(
        self, transitions, transition_unit_vector, state_size
    ):

        selector_delete_stack_filter = self.get_selector_delete_stack_filter(
            state_size, self.stack_position_elems
        )
        selector_delete_stack_filter = tf.reshape(
            tf.constant(selector_delete_stack_filter, dtype=tf.float32),
            shape=[1, state_size, state_size],
        )
        # print("delete_stack Filter: \n %s" % (selector_delete_stack_filter.eval()))

        selector_delete_stack_projection_result = self.get_selector_delete_stack_projection(
            transitions, transition_unit_vector
        )
        selector_delete_stack_projection_result_reshape = tf.reshape(
            selector_delete_stack_projection_result,
            shape=[selector_delete_stack_projection_result.shape[0], 1, 1],
        )
        # print("delete_stack transitions reshaped: \n %s" % (selector_delete_stack_projection_result_reshape.eval()))

        selector_delete_stack_projection_result = (
            selector_delete_stack_projection_result_reshape
            * selector_delete_stack_filter
        )
        # print("delete stack transitions: \n %s" % selector_delete_stack_projection_result.eval())
        return selector_delete_stack_projection_result

    ################## OUTPUT SHIFT ###################

    def get_selector_shift_output_projection(self, transitions, transition_unit_vector):
        selector_shift_output_projection = tf.constant(
            [transition_unit_vector],
            dtype=tf.float32,
            shape=[self.available_transitions_len, 1],
        )
        selector_shift_output_projection_result = tf.matmul(
            transitions, selector_shift_output_projection
        )
        return selector_shift_output_projection_result

    def get_selector_shift_output_filter(self, state_size, morpheme_position):
        tensor_ones_indexes = [k for k in range(0, state_size)]
        tensor_ones_indexes = np.roll(tensor_ones_indexes, 1)

        selector_shift_output_filter = np.zeros([state_size, state_size])
        for i in range(0, state_size):
            if i in morpheme_position[1:]:
                selector_shift_output_filter[i, tensor_ones_indexes[i]] = 1
            else:
                selector_shift_output_filter[i, i] = 0
            if i == self.transition_position:
                selector_shift_output_filter[i, i] = 0
        return selector_shift_output_filter

    def get_selector_shift_output_result(
        self, transitions, transition_unit_vector, state_size
    ):
        selector_shift_output_filter = self.get_selector_shift_output_filter(
            state_size, self.output_position
        )
        selector_shift_output_filter = tf.reshape(
            tf.constant(selector_shift_output_filter, dtype=tf.float32),
            shape=[1, state_size, state_size],
        )
        # print("shift_output Filter: \n %s" % (selector_shift_output_filter.eval()))

        selector_shift_output_projection_result = self.get_selector_shift_output_projection(
            transitions, transition_unit_vector
        )
        selector_shift_output_projection_result_reshape = tf.reshape(
            selector_shift_output_projection_result,
            shape=[selector_shift_output_projection_result.shape[0], 1, 1],
        )
        # print("shift_output transitions reshaped: \n %s" % (selector_shift_output_projection_result_reshape.eval()))

        selector_shift_output_projection_result = (
            selector_shift_output_projection_result_reshape
            * selector_shift_output_filter
        )
        # print("shift_output transitions: \n %s" % selector_shift_output_projection_result.eval())
        return selector_shift_output_projection_result

    #############  ADD OUTPUT#######################

    def get_output_matrix(self, output_values):
        output_column = tf.reshape(
            tf.cast(output_values, dtype=tf.float32), shape=[self.batch_size, 1]
        )
        output_row = tf.constant(
            [
                [
                    0 if i != self.output_position[0] else 1
                    for i in range(0, self.state_size)
                ]
            ],
            dtype=tf.float32,
            shape=[1, self.state_size],
        )
        output_matrix = tf.matmul(
            output_column, output_row, a_is_sparse=True, b_is_sparse=True
        )
        output_matrix = tf.reshape(
            output_matrix, shape=[self.batch_size, self.state_size, 1]
        )
        return output_matrix

    ####################  ADD TRANSITION #######

    def get_transition_matrix(self, transitions_array):
        transition_column = tf.reshape(
            tf.cast(transitions_array, dtype=tf.float32), shape=[self.batch_size, 1]
        )
        transition_row = tf.constant(
            [
                [
                    0 if i != self.transition_position else 1
                    for i in range(0, self.state_size)
                ]
            ],
            dtype=tf.float32,
            shape=[1, self.state_size],
        )
        transition_matrix = tf.matmul(
            transition_column, transition_row, a_is_sparse=True, b_is_sparse=True
        )
        transition_matrix = tf.reshape(
            transition_matrix, shape=[self.batch_size, self.state_size, 1]
        )
        return transition_matrix

    ###################### MORPHEME ######################
    # TODO:esto parece ser solo la transicion shif_output!!

    def get_selector_morpheme_projection_result(
        self, transitions, transition_unit_vector
    ):
        selector_morpheme_projection = tf.constant(
            [transition_unit_vector],
            dtype=tf.float32,
            shape=[self.available_transitions_len, 1],
        )
        selector_morpheme_projection_result = tf.matmul(
            transitions, selector_morpheme_projection
        )
        return selector_morpheme_projection_result

    def get_selector_morpheme_filter(self, state_size):
        # 4
        selector_shift_output_filter = self.get_selector_shift_output_filter(
            state_size, self.output_position
        )
        selector_morpheme_filter = selector_shift_output_filter

        return selector_morpheme_filter

    def get_selector_morpheme_result(self, transitions, transition_unit_vector):

        selector_morpheme_filter = self.get_selector_morpheme_filter(self.state_size)
        selector_morpheme_filter = tf.reshape(
            tf.constant(selector_morpheme_filter, dtype=tf.float32),
            shape=[1, self.state_size, self.state_size],
        )
        # print("morpheme Filter: \n %s" % (selector_morpheme_filter.eval()))
        selector_morpheme_projection_result = self.get_selector_morpheme_projection_result(
            transitions, transition_unit_vector
        )
        selector_morpheme_projection_result_reshape = tf.reshape(
            selector_morpheme_projection_result,
            shape=[selector_morpheme_projection_result.shape[0], 1, 1],
        )
        # print("morpheme transitions reshaped: \n %s" % (selector_morpheme_projection_result_reshape.eval()))

        selector_morpheme_projection_result = (
            selector_morpheme_projection_result_reshape * selector_morpheme_filter
        )
        # print("morpheme transitions: \n %s" % selector_morpheme_projection_result.eval())
        return selector_morpheme_projection_result

    ###################### TRANSICIONES DISPONIBLES##################

    def get_one_hot_transitions(self):
        transitions_names_len = len(self.transition_names)
        available_transitions = np.zeros([transitions_names_len, transitions_names_len])
        for index, i in enumerate(available_transitions):
            available_transitions[index, index] = 1
        return available_transitions

    @staticmethod
    def get_transitions_array(next_transition):
        transitions_array = tf.argmax(next_transition, axis=1)
        return transitions_array

    @staticmethod
    def get_one_hot_index(one_hot):
        for index, i in enumerate(one_hot):
            if i == 1:
                return index


class TransitionSystemWorkerNode(WorkerNode):
    def __init__(
        self,
        stack_size: int,
        transition_size: int,
        output_size: int,
        input_size: int,
        batch_size: int,
        stack_position: int,
        stack_position_elems: list,
        transition_position: int,
        morpheme_position: list,
        input_position: int,
        execution_mode: ExecutionMode,
        transition_oracle: WorkerNode,
        output_oracle: WorkerNode,
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
        self.transition_system_configurations = TransitionSystemConfigurations(
            stack_size,
            transition_size,
            output_size,
            input_size,
            batch_size,
            stack_position,
            stack_position_elems,
            transition_position,
            morpheme_position,
            input_position,
            execution_mode,
            scope_name,
            configuration_path,
            configuration_name,
            task_index,
            redis_connection_pool,
        )
        self.batch_size = batch_size
        self.transition_oracle = transition_oracle
        self.output_oracle = output_oracle
        # TODO:ajustar para que el parameternode me devuelva las cosas que necesito, asi el codgo es mas legible
        # self.filters, self.linear_regressor, self.options, self.temperature = self.transition_system_configurations()

    def _operation(
        self, *args
    ):  # recibe outputs array y state, creo que estos deberian ser parte de la clase, incluirlos como atributos
        if self.transition_system_configurations.execution_mode == ExecutionMode.eager:
            state_result = self.apply_eager_step(args[0][0])
        elif (
            self.transition_system_configurations.execution_mode == ExecutionMode.graph
        ):
            state_result = self.apply_graph_step(args[0][0])
            state_result = tf.expand_dims(state_result, axis=2)
        return state_result

    # aqui aplicamos solo la transicion del vector unitario que se recibe, por eso hay que iterar sobre las transiciones disponibles, esto no tiene mucho sentido ahora
    # quien llama a esta funcion debe ir acumulando el resultado
    def apply_transition(
        self,
        transitions,
        transition_unit_vector,
        state_size,
        original_state,
        current_state=None,
    ):
        transition_index = self.transition_system_configurations.get_one_hot_index(
            transition_unit_vector
        )
        original_state = tf.reshape(
            tf.cast(original_state, dtype=tf.float32),
            shape=[self.batch_size, state_size],
        )
        expanded_state = tf.expand_dims(original_state, axis=2)
        if transition_index == 0:  # shift
            # obtenemos el selctor con las matrices que se aplicaran
            selector_shift_result = self.transition_system_configurations.get_selector_shift_result(
                transitions, transition_unit_vector, state_size
            )
            new_state = tf.matmul(selector_shift_result, expanded_state)
        elif transition_index == 1:  # discar/clean_input
            selector_clean_input_projection_result = self.transition_system_configurations.get_selector_clean_input_result(
                transitions, transition_unit_vector, state_size
            )
            new_state = tf.matmul(
                selector_clean_input_projection_result, expanded_state
            )
        elif transition_index == 2:  # delete_stack
            selector_delete_stack_result = self.transition_system_configurations.get_selector_delete_stack_result(
                transitions, transition_unit_vector, state_size
            )
            new_state = tf.matmul(selector_delete_stack_result, expanded_state)
        elif transition_index == 3:  # shift_output
            selector_shift_output_result = self.transition_system_configurations.get_selector_shift_output_result(
                transitions, transition_unit_vector, state_size
            )
            new_state = tf.matmul(selector_shift_output_result, expanded_state)
        elif transition_index == 4:  # morpheme
            selector_morpheme_projection_result = self.transition_system_configurations.get_selector_morpheme_result(
                transitions, transition_unit_vector
            )
            new_state = tf.matmul(selector_morpheme_projection_result, expanded_state)
        else:  # esto es un hack para probar, falta inlcuir las otras transiciones en el if
            original_state_zeros = tf.constant(
                np.zeros(original_state.shape),
                dtype=tf.float32,
                shape=[self.batch_size, state_size],
            )
            new_state = tf.expand_dims(original_state_zeros, axis=2)

        if current_state is None:
            return new_state
        else:
            new_state = current_state + new_state
            return new_state

    # TODO: esta bien que esten hardcodes los unitarios en onehot correspondientes a cada transicion??
    # se calculan las transciones de un step a un batch, a diferencia de apply_transition no itera sino que recibe todos los vectores unitarios de transiciones disponibles
    def apply_batch_transition(
        self,
        transitions,
        transition_unit_vectors,
        state_size,
        original_state,
        current_state=None,
    ):
        original_state = (
            original_state  # priemra dimension es el numeor de rows en matriz de state
        )
        expanded_state = tf.expand_dims(original_state, axis=2)

        #######

        selector_shift_result = self.transition_system_configurations.get_selector_shift_result(
            transitions, list(transition_unit_vectors[0]), state_size
        )
        selector_clean_input_projection_result = self.transition_system_configurations.get_selector_clean_input_result(
            transitions, list(transition_unit_vectors[1]), state_size
        )
        selector_delete_stack_result = self.transition_system_configurations.get_selector_delete_stack_result(
            transitions, list(transition_unit_vectors[2]), state_size
        )
        selector_shift_output_result = self.transition_system_configurations.get_selector_shift_output_result(
            transitions, list(transition_unit_vectors[3]), state_size
        )
        selector_morpheme_projection_result = self.transition_system_configurations.get_selector_morpheme_result(
            transitions, list(transition_unit_vectors[4])
        )

        #######
        new_state = tf.matmul(selector_shift_result, expanded_state)
        new_state = new_state + tf.matmul(
            selector_clean_input_projection_result, expanded_state
        )
        new_state = new_state + tf.matmul(selector_delete_stack_result, expanded_state)
        new_state = new_state + tf.matmul(selector_shift_output_result, expanded_state)
        new_state = new_state + tf.matmul(
            selector_morpheme_projection_result, expanded_state
        )

        return new_state

    # next_transition: batch de transiciones
    def apply_eager_transitions(self, next_transition, original_state):
        state_size = self.transition_system_configurations.state_size
        state_result = None
        for transition in self.transition_system_configurations.available_transitions:
            self.transition_system_configurations.step_transition = next_transition
            if state_result is None:
                state_result = self.apply_transition(
                    next_transition, list(transition), state_size, original_state
                )
            else:
                transition_result = self.apply_transition(
                    next_transition,
                    list(transition),
                    state_size,
                    original_state,
                    current_state,
                )
                state_result = transition_result

            current_state = state_result
        self.transition_system_configurations.transitions_array = self.transition_system_configurations.get_transitions_array(
            next_transition
        )
        transition_matrix = self.transition_system_configurations.get_transition_matrix(
            self.transition_system_configurations.transitions_array
        )
        outputs_array = self.output_oracle(state_result, self.output_oracle.counter)
        output_matrix = self.transition_system_configurations.get_output_matrix(
            outputs_array
        )
        state_result = state_result + transition_matrix + output_matrix
        return state_result

    def apply_graph_transitions(self, next_transition, original_state, counter):
        state_size = self.transition_system_configurations.state_size
        state_result = None
        self.transition_system_configurations.step_transition = next_transition
        transition_unit_vectors = (
            self.transition_system_configurations.available_transitions
        )

        state_result = self.apply_batch_transition(
            next_transition, transition_unit_vectors, state_size, original_state
        )
        self.transition_system_configurations.transitions_array = self.transition_system_configurations.get_transitions_array(
            next_transition
        )
        transition_matrix = self.transition_system_configurations.get_transition_matrix(
            self.transition_system_configurations.transitions_array
        )
        outputs_array = self.output_oracle(state_result, counter)
        output_matrix = self.transition_system_configurations.get_output_matrix(
            outputs_array
        )
        state_result = state_result + transition_matrix + output_matrix
        return state_result

    def apply_eager_step(self, original_state):
        state = original_state
        condition = (
            self.transition_oracle.transitions.shape[0] > self.transition_oracle.counter
        )
        while condition:
            transitions = self.transition_oracle(state)  # transition o transitionsss??
            # transitions = tf.constant(transitions, dtype=tf.float32)
            self.transition_system_configurations.transitions = (
                transitions  # es un STEP, BATCH DE N ELEMENTOS
            )
            # output_array = self.output_oracle(state??)
            state = self.apply_eager_transitions(transitions, state)
            condition = (
                self.transition_oracle.transitions.shape[0]
                > self.transition_oracle.counter
            )
        return state

    # el counter es del oracle y lo comparo contra las transiciones, deberia ser otra la condicion??
    def transition_condition(self, counter, transitions_len, state):
        return tf.less(counter, transitions_len)

    def transition_body(self, counter, transitions_len, state):
        transitions = self.transition_oracle(
            state, counter
        )  # transition o transitionsss??
        self.transition_system_configurations.transitions = (
            transitions  # es un STEP, BATCH DE N ELEMENTOS
        )
        state = self.apply_graph_transitions(transitions, state, counter)
        state = tf.reshape(
            state,
            shape=[self.batch_size, self.transition_system_configurations.state_size],
        )
        counter = tf.add(counter, 1, name="current-counter")
        return [counter, transitions_len, state]

    def apply_graph_step(self, original_state):
        counter = tf.constant(
            self.transition_oracle.counter,
            dtype=tf.int32,
            shape=[],
            name="current-counter-init",
        )
        transitions_len = tf.constant(
            self.transition_oracle.transitions.shape[0],
            dtype=tf.int32,
            shape=[],
            name="transtions_len",
        )
        state = np.array(original_state, np.float32)
        counter, _, state = tf.while_loop(
            self.transition_condition,
            self.transition_body,
            [counter, transitions_len, state],
            parallel_iterations=1,
        )
        return state
