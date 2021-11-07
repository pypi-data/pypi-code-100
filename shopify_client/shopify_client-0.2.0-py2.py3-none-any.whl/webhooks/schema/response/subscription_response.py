import dataclasses

from .user_error import UserError
from .webhook_subscription import WebhookSubscription


@dataclasses.dataclass
class SubscriptionResponse:
    subscription: WebhookSubscription
    user_errors: [UserError] = None
