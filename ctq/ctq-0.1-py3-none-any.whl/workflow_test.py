from . import workflow
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch


class TestMockWorkflow(TestCase):
    class MockWorkflow(workflow.Workflowable):

        workflow_transitions = {
            "publish": {"from": ["draft", "private"], "to": "public"},
            "unpublish": {"from": ["public"], "to": "private"},
        }

        workflow_state = "private"

    def setUp(self):
        self.instance = self.MockWorkflow()
        self.instance.emit = Mock()

    def test_exceptions(self):
        with self.assertRaises(workflow.WorkflowUnknownActionError):
            self.instance.workflow_action("foo")
        with self.assertRaises(workflow.WorkflowIllegalTransitionError):
            self.instance.workflow_action("unpublish")

    @patch("ctq.workflow.emit")
    def test_publish(self, mock_emit):
        self.instance.workflow_action("publish")
        self.assertEqual(self.instance.workflow_state, "public")
        expected_event_data = {
            "action": "publish",
            "from_state": "private",
            "to_state": "public",
        }
        mock_emit.assert_any_call(
            self.instance, "workflow-before-publish", expected_event_data
        )
        mock_emit.assert_any_call(
            self.instance, "workflow-after-publish", expected_event_data
        )
