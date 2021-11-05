from circle import api_requestor, util
from circle.resources.abstract.api_resource import APIResource


class UpdateableAPIResource(APIResource):
    @classmethod
    def update(cls, uid, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key)
        url = "%s/%s" % (cls.class_url(), uid)

        response, api_key = requestor.request("put", url, params)
        return util.convert_to_circle_object(
            response, api_key, klass_name=cls.OBJECT_NAME
        )
