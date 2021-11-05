from circle.resources.abstract import CreateableAPIResource, ListableAPIResource


class Subscription(CreateableAPIResource, ListableAPIResource):
    OBJECT_NAME = "notifications.subscriptions"
