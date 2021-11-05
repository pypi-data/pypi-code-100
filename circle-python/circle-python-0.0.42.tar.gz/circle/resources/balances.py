from circle import util
from circle.api_requestor import APIRequestor
from circle.resources.abstract.api_resource import APIResource


class Balances(APIResource):
    """
    The balances are obtained with the .retrieve() method which is supported in the base APIResource class.
    https://developers.circle.com/reference/encryption
    """

    OBJECT_NAME = "balances"  # The object name as it maps to the API resource.

    @classmethod
    def retrieve(cls, api_key=None, **kwargs):
        """
        The balances retrieve method looks like the list method as there is no ID to query by.

        However, this returns a {} not a [], thus, for consistency we want devs to call the retrieve method.
        """
        requestor = APIRequestor(api_key)
        url = cls.class_url()
        response, api_key = requestor.request("get", url, kwargs)
        circle_object = util.convert_to_circle_object(response, api_key)
        return circle_object
