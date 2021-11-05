from unittest import TestCase
from uuid import uuid4

from fastapi import Request

from edu_py_logger.utils import get_request_extra_data


class TestExtraDataFromRequest(TestCase):
    def test_extra(self):
        trace_id = uuid4()
        request = Request({"type": "http"})
        request.state.trace_id = trace_id
        expected = {"trace_id": trace_id, "correlation_id": "correlation_id"}

        result = get_request_extra_data(
            request, correlation_id="correlation_id", user={}
        )

        self.assertEqual(result, expected)
