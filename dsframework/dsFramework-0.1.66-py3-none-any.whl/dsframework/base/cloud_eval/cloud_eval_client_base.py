class CloudEvalClientBase:
    UNIMPLEMENTED_ERROR_MESSAGE = "Please override the parent base class methods for using cloud eval"

    def get_request_headers(self, row: dict):
        """
        construct the model service request headers.
        dataset csv record is provided in case it is needed.
        Ex:
        ```
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "x-token": "fake-super-secret-token"
        }
        ```
        """
        raise NotImplementedError(CloudEvalClientBase.UNIMPLEMENTED_ERROR_MESSAGE)

    def get_request_payload(self, row: dict):
        """
        construct a model service payload from a dataset csv record
        Ex:
        ```
        if 'uid' not in record:
            record['uid'] = str(uuid.uuid4())
        input = PyScoopsClassificationInputs(html_content=record['text'],
                                             source=record['source'],
                                             queue_name=record['queue_name'],
                                             title=record['title']
                                             )
        model_request = input  # [input]
        payload = model_request.dict()
        return payload
        ```
        """
        raise NotImplementedError(CloudEvalClientBase.UNIMPLEMENTED_ERROR_MESSAGE)

    def extract_model_predictions_from_response(self, predictions):
        """
        Extract the predictions from the service response.
        ```
        if type(predictions) == list:
            if len(predictions) > 1:
                raise Exception("We do not currently support mini batches")
            prediction = predictions[0]
            try:
                prediction_obj = PyScoopsClassificationOutputs(**prediction)
                return prediction_obj.dict()
            except:
                # default answer
                return {}
        ```
        """
        raise NotImplementedError(CloudEvalClientBase.UNIMPLEMENTED_ERROR_MESSAGE)

    def get_endpoint_name(self):
        """
        Return the model's endpoint name.
        For example, if you invoke the model with `/predict` then you can do:
        ```
        return "predict"
        ```
        """
        raise NotImplementedError(CloudEvalClientBase.UNIMPLEMENTED_ERROR_MESSAGE)
