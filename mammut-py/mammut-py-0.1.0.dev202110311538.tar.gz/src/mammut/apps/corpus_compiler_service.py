# coding=utf-8
from kafka import KafkaConsumer, KafkaProducer
import logging
from mammut.apps import InterpreterMain_pb2

from mammut.apps import (
    KAFKA_BROKER_STR,
    COMPILER_SERVICE_INPUT_TOPIC,
    COMPILER_SERVICE_OUTPUT_TOPIC,
    COMPILER_OUTPUT_RETRIES,
    COMPILER_OUTPUT_TIMEOUT,
    COMPILER_OUTPUT_MAX_RECORDS,
)
from mammut.common.util import StringEnum

log = logging.getLogger(__name__)

FINAL_OUTPUT_MESSAGE_PREFIX = "Finished compilation for Compilation Task: {}"


class CorpusCompilerServiceCallResult(StringEnum):
    NoneCall = "NoneCall"
    Unknown = "Unknown"
    FailedCall = "FailedCall"
    SuccessCall = "SuccessCall"


def is_error_message(imo: InterpreterMain_pb2.InterpreterMainOutput):

    imo_type = imo.type
    switcher = {
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "SuccessOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "FailureOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "UnsupportedFeatureOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "PropertyValueNotFoundOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "UnknownPropertyOrEdgeOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "OntologyTypeNotFoundOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "VertexUndefinedOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "VariableUndefinedOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "FieldUndefinedOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "EdgeValueNotFoundOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "ReservedKeywordFoundOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "PropertyDescriptorNotFoundOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "GettingCorpusMapOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "GettingOntologyOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "ExpandingOntologyOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "ComputingEntryPointOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "GettingOntologyInstancesOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "LoadingInstancesToWorkingMemoryOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "GeneratingOntologyClassesOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "GettingVariablesOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "GettingSceneriesOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "GettingExtensionsOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "CompilingVariablesOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "CompilingSceneriesOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "CompilingExtensionsOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "GroupingCompiledExtensionsOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "GroupingCompiledSceneriesOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "CompilingInformationTuplesOutput"
        ].number: True,
        InterpreterMain_pb2.InterpreterMainOutput.Types.DESCRIPTOR.values_by_name[
            "UnexpectedCompilerError"
        ].number: True,
    }
    if switcher.__contains__(imo_type):
        return switcher[imo_type]
    else:
        return False


class CorpusCompilerService:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER_STR], retries=5)
        self.consumer = KafkaConsumer(
            COMPILER_SERVICE_OUTPUT_TOPIC,
            enable_auto_commit=True,
            group_id="framework",
            bootstrap_servers=[KAFKA_BROKER_STR],
            api_version=(0, 10),
        )

    def compile(
        self,
        mammut_id: int,
        slide_id: str,
        execute_sampling_corpus: bool,
        regional_settings: str,
        metadata_token_separator: str,
        corpus_ids: [],
        compilation_message_callback,
    ):
        raw_messages = self.consumer.poll(
            timeout_ms=COMPILER_OUTPUT_TIMEOUT, max_records=COMPILER_OUTPUT_MAX_RECORDS
        )
        for topic_partition, messages in raw_messages.items():
            for message in messages:
                output = InterpreterMain_pb2.InterpreterMainOutput()
                output.ParseFromString(message.value)
                mess = "Previous unread message found: {}".format(output.message)
                log.info(mess)
                if compilation_message_callback:
                    compilation_message_callback(mess, None)

        def on_send_success(record_metadata):
            mess = "Message delivered to {} [{} - {}]".format(
                record_metadata.topic, record_metadata.partition, record_metadata.offset
            )
            log.info(mess)
            if compilation_message_callback:
                compilation_message_callback(mess, None)

        def on_send_error(excp):
            mess = "Compilation Error: Message delivery failed: {}".format(excp)
            if compilation_message_callback:
                compilation_message_callback(mess, None)
            log.error(mess, exc_info=excp)

        input = InterpreterMain_pb2.InterpreterMainInput()
        input.regionalSettings = regional_settings
        input.mammutId = mammut_id
        input.slideId = slide_id
        input.executeSamplingCorpus = execute_sampling_corpus
        input.corpusIds.extend(corpus_ids)
        input.metadataTokenSeparator = metadata_token_separator
        self.producer.send(
            COMPILER_SERVICE_INPUT_TOPIC,
            key=str(mammut_id).encode(),
            value=input.SerializeToString(),
        ).add_callback(on_send_success).add_errback(on_send_error)
        # block until all async messages are sent
        self.producer.flush()
        outputs = []
        retries = COMPILER_OUTPUT_RETRIES
        while retries > 0:
            retries -= 1
            raw_messages = self.consumer.poll(
                timeout_ms=COMPILER_OUTPUT_TIMEOUT,
                max_records=COMPILER_OUTPUT_MAX_RECORDS,
            )
            for topic_partition, messages in raw_messages.items():
                for message in messages:
                    output = InterpreterMain_pb2.InterpreterMainOutput()
                    output.ParseFromString(message.value)
                    outputStr = "Additional info: Phase->" + str(output.phase)
                    if output.mammutId == mammut_id:
                        retries = COMPILER_OUTPUT_RETRIES
                        outputs.append(output)
                        if compilation_message_callback and is_error_message(output):
                            compilation_message_callback(output.message, outputStr)

                        log.info(output.message)
                        if output.message.startswith(
                            FINAL_OUTPUT_MESSAGE_PREFIX.format(mammut_id)
                        ):
                            retries = 0
                    else:
                        if compilation_message_callback and is_error_message(output):
                            compilation_message_callback(output.message, outputStr)

                        log.info(output.message)
        return outputs
