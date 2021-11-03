from .events import emit


class WorkflowActionError(Exception):
    """Raised when an in performing a workflow action"""


class WorkflowUnknownActionError(WorkflowActionError):
    """Raised when an unknown action is atempted"""


class WorkflowIllegalTransitionError(WorkflowActionError):
    """Raised when a transition exists but it it not allowed for the current
    object's workflow state
    """


class Workflowable(object):
    """An object that defins a workflow state and possible transitions
    to other state.

    Attributes:

        workflow_transitions (dict): A diction object of valid transitions.
        Each transition is a key in the dictionary the value is another dictionary
        with the keys ``from`` (a list of valid transiation to come from) and
        ``to`` the target workflow state.

    """

    # Workflow
    workflow_transitions = {}

    @property
    def workflow_state(self) -> str:
        """Returns: str: the current workflow state. This property rases a
        NotImplementedError and must be overried by an inheriting class
        """
        raise NotImplementedError("Method workflow_state not implemented")

    def workflow_set_state(self, state: str):
        """Set the current workflow state. The default impleentation simply
        attribute sets ``self.workflow_state``
        """
        self.workflow_state = state

    @property
    def workflow_valid_actions(self):
        """Returns: list of string indicating the valid actions
        that can be taken.
        """
        result = []
        state = self.workflow_state
        for (name, props) in self.workflow_transitions.items():
            if state in props["from"]:
                result.append(name)
        return result

    def workflow_action(self, action: str):
        """Find an execute a workflow transition for a given action. The
        transition is sourced from ``self.workflow_transitions``.

        During the execution of the transition:

        1. A check is made that the workflow action is valid.

        2. ``workflow-before-ACTION`` event is emitted where ``ACTION`` is the
           ``action`` arg.

        3. ``self.workflow_set_state(to_state)`` is called

        4. ``workflow-after-ACTION`` event is emitted.

        Args:

            action: The action to look up in the ``self.workflow_transitions``
                attribute
        """
        from_state = self.workflow_state
        transition = self.workflow_transitions.get(action, None)

        # Check that the transition is valid
        if transition is None:
            raise WorkflowUnknownActionError(
                f"Unknown workflow action {action} on an instance of {self.__class__.__name__}."
            )
        if from_state not in transition["from"]:
            raise WorkflowIllegalTransitionError(
                f"Can not {action} on an instance of {self.__class__.__name__} in the state {from_state}"
            )
        to_state = transition["to"]

        # Perform transition
        event_data = {"action": action, "from_state": from_state, "to_state": to_state}
        emit(self, f"workflow-before-{action}", event_data)
        self.workflow_set_state(to_state)
        emit(self, f"workflow-after-{action}", event_data)
