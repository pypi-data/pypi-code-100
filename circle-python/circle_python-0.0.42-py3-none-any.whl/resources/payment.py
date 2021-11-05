from circle.resources.abstract import CreateableAPIResource, ListableAPIResource


class Payment(CreateableAPIResource, ListableAPIResource):
    OBJECT_NAME = "payments"
