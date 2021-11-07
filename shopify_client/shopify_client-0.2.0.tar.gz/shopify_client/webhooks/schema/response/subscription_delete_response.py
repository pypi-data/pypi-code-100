import dataclasses

from .user_error import UserError


@dataclasses.dataclass
class SubscriptionDeleteResponse:
    deleted_webhook_subscription_id: str
    user_error: UserError = None
