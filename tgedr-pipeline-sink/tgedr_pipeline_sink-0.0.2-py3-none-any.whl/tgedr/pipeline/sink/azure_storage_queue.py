from typing import Any, Dict

from azure.storage.queue import BinaryBase64DecodePolicy, BinaryBase64EncodePolicy, QueueClient
from tgedr.pipeline.common.common import PipelineConfigException
from tgedr.pipeline.common.sink import PipelineSink


class AzureStorageQueue(PipelineSink):
    def __init__(self, config: Dict[str, Any]) -> None:
        super(AzureStorageQueue, self).__init__(config=config)
        self.__client = None
        self.__queue_name = self._get_config("queue")
        self.__connect_string = self._get_config("connection_string")
        self.__queue_properties = None

    def _validate_config(self, config: Dict[str, Any]):
        self.log.info(f"[_validate_config|in]{config}")
        config_keys = ["queue", "connection_string"]
        if not all(x in config.keys() for x in config_keys):
            raise PipelineConfigException(f"expected keys: {config_keys} | actual keys: {config.keys()}")
        self.log.info("[_validate_config|out]")

    def _get_client(self):
        self.log.info("[AzureStorageQueue._get_client|in]")
        if not self.__client:
            self.__client = QueueClient.from_connection_string(
                conn_str=self.__connect_string,
                queue_name=self.__queue_name,
                message_encode_policy=BinaryBase64EncodePolicy(),
                message_decode_policy=BinaryBase64DecodePolicy(),
            )
        self.log.info(f"[AzureStorageQueue._get_client|out] => {self.__client}")
        return self.__client

    def _assert_queue(self) -> bool:
        self.log.info("[AzureStorageQueue._assert_queue|in]")
        if not self.__queue_properties:
            result = False
            try:
                self.__queue_properties = self._get_client().get_queue_properties()
                result = True
            except Exception as ex:
                self.log.info(f"[AzureStorageQueue._assert_queue] queue not found: {ex}")
        else:
            result = True
        self.log.info(f"[AzureStorageQueue._assert_queue|out] => {result}")
        return result

    def _create_queue(self):
        self.log.info("[AzureStorageQueue._create_queue|in]")
        self._get_client().create_queue()
        self.log.info("[AzureStorageQueue._create_queue|out]")

    def put(self, msg: str):
        self.log.info(f"[AzureStorageQueue.put|in] ({self.text_fragment(msg) if msg else None})")
        if not self._assert_queue():
            self._create_queue()
        self._get_client().send_message(msg.encode(encoding="UTF-8", errors="replace"))
        self.log.info("[AzureStorageQueue.put|out]")
