from typing import Dict

from fastapi import Body, Request


def get_request_extra_data(
    request: Request, correlation_id: str = Body(None), user: Dict = Body(None)
):
    return {
        "trace_id": request.state.trace_id,
        **({"correlation_id": correlation_id} if correlation_id else {}),
        **({"user_id": user.get("user_id")} if user else {}),
    }
