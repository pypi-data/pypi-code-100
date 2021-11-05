from circle.resources.abstract import CreateableAPIResource, UpdateableAPIResource


class Card(CreateableAPIResource, UpdateableAPIResource):
    OBJECT_NAME = "cards"
