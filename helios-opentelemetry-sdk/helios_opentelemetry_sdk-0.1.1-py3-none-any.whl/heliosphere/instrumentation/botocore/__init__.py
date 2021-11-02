from heliosphere.instrumentation.base import HeliosphereBaseInstrumentor
from heliosphere.instrumentation.botocore.consts import AwsAttribute
from heliosphere.instrumentation.botocore.dynamodb import DynamoDBInstrumentor
from heliosphere.instrumentation.botocore.s3 import S3Instrumentor
from heliosphere.instrumentation.botocore.ses import SESInstrumentor
from heliosphere.instrumentation.botocore.sns import SNSInstrumentor
from heliosphere.instrumentation.botocore.sqs import SQSInstrumentor


class HeliosphereBotocoreInstrumentor(HeliosphereBaseInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.botocore'
    INSTRUMENTOR_NAME = 'BotocoreInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)
        self.services = dict()

    def instrument(self, tracer_provider=None):
        if self.get_instrumentor() is None:
            return

        self.services.update({
            'dynamodb': DynamoDBInstrumentor(),
            's3': S3Instrumentor(),
            'ses': SESInstrumentor(),
            'sns': SNSInstrumentor(),
            'sqs': SQSInstrumentor(tracer_provider=tracer_provider),
        })

        self.get_instrumentor().instrument(tracer_provider=tracer_provider,
                                           response_hook=self.response_hook,
                                           request_hook=self.request_hook)

    def request_hook(self, span, service_name, operation_name, api_params):
        if not span or not span.is_recording():
            return

        span.set_attribute(AwsAttribute.AWS_SERVICE, service_name)
        service_instrumentor = self.services.get(service_name)
        if service_instrumentor is not None:
            if callable(service_instrumentor.request_hook):
                return service_instrumentor.request_hook(span, operation_name, api_params)

    def response_hook(self, span, service_name, operation_name, result):
        if not span or not span.is_recording():
            return

        span.set_attribute(AwsAttribute.AWS_SERVICE, service_name)
        service_instrumentor = self.services.get(service_name)
        if service_instrumentor is not None:
            if callable(service_instrumentor.response_hook):
                return service_instrumentor.response_hook(span, operation_name, result)
