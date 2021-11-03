from dsframework.base.cloud_eval.cloud_eval_client_base import CloudEvalClientBase


UNIMPLEMENTED_ERROR_MESSAGE = "Please override the parent base class methods for using cloud eval"


class CloudEvalClient(CloudEvalClientBase):
    """
    Override the parent base class methods for using cloud eval
    """
    def get_request_headers(row: dict):
        raise NotImplementedError(UNIMPLEMENTED_ERROR_MESSAGE)

    def get_request_payload(row: dict):
        raise NotImplementedError(UNIMPLEMENTED_ERROR_MESSAGE)

    def extract_model_predictions_from_response(self, predictions):
        raise NotImplementedError(UNIMPLEMENTED_ERROR_MESSAGE)

    def get_endpoint_name(self):
        raise NotImplementedError(UNIMPLEMENTED_ERROR_MESSAGE)

