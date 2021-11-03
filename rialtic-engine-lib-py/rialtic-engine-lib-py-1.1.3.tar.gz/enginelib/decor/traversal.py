import os
from typing import cast, Callable, Tuple, Optional

from enginelib.decor.predicate import Predicate
from enginelib.decor.errors import InvalidParameterError
from enginelib.decor.node import DecisionNode, LeafNode
from enginelib.decor.registry import Registry
from enginelib.decor.tree import Tree


class TreeTraversal:
    """Responsible for walking down a decision tree, from its root
    while making the registry update itself (the set of qualifying
    claims and claim lines, and the custom parameters) according to
    the predicate functions in each node of the decision tree."""
    def __init__(self, decision_tree: Tree, registry: Registry):
        #: the decision tree that must be traversed.
        self.decision_tree = decision_tree

        #: the registry in its initial state.
        self.registry = registry

    @staticmethod
    def _log(msg_line: str):
        print(msg_line)

    def execute(self) -> str:
        """Perform the traversal, starting from the root of the tree.
        For debugging, please set DECOR_DEBUG environment variable to a non-empty value.

        Returns:
            a SimpleInsight according to the end branch that was reached.
        """
        debug = os.environ.get('DECOR_DEBUG', '')
        node = self.decision_tree.root
        yes_no = '   '
        if debug:
            msg = f'Traversal of tree for claim {self.registry.cue.claim_num}' + \
                  f' line {self.registry.clue.sequence}:'
            self._log('-' * len(msg))
            self._log(msg)
        while isinstance(node, DecisionNode):
            func, param_name = self._wrapped_predicate_func(node.predicate)
            if debug:
                self._log(f'  {yes_no} --> #{node.label}: "{node.predicate.description}"' +
                          (f' (filtering {param_name.upper()})' if param_name else ''))
            if param_name is None:
                value = func()
            elif param_name == 'oc':
                value = self.registry.is_there_oc_such_that(func)
            elif param_name == 'ocl':
                value = self.registry.is_there_ocl_such_that(func)
            elif param_name == 'ocl_s':
                value = self.registry.is_there_ocl_s_such_that(func)
            elif param_name == 'ocl_d':
                value = self.registry.is_there_ocl_d_such_that(func)
            elif param_name == 'acl':
                value = self.registry.is_there_acl_such_that(func)
            else:
                raise InvalidParameterError(f'(TreeTraversal) Invalid parameter {param_name} encountered.')

            node = node.yes_node if value else node.no_node
            if debug:
                yes_no = 'YES' if value else ' NO'

        node = cast(LeafNode, node)
        return node.label

    def _wrapped_predicate_func(self, predicate: Predicate) -> Tuple[Callable[..., bool], Optional[str]]:
        outer_kwargs = dict()
        if 'cue' in predicate.standard_params:
            outer_kwargs['cue'] = self.registry.cue
        if 'clue' in predicate.standard_params:
            outer_kwargs['clue'] = self.registry.clue
        if 'data' in predicate.standard_params:
            outer_kwargs['data'] = self.registry.data
        if 'registry' in predicate.standard_params:
            outer_kwargs['registry'] = self.registry
        for param_name in predicate.custom_params:
            outer_kwargs[param_name] = self.registry[param_name]

        filtering_param = set(predicate.standard_params).difference(
            {'cue', 'clue', 'data', 'registry'}
        )
        if filtering_param == set():
            if predicate.func(**outer_kwargs):
                return (lambda: True), None
            else:
                return (lambda: False), None

        def inner(**inner_kwargs) -> bool:
            inner_kwargs.update(outer_kwargs)
            return predicate.func(**inner_kwargs)

        return inner, next(iter(filtering_param))
