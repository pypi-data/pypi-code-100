from unittest import TestCase, mock

from edu_py_logger.logger import LoggerService


class TestLogger(TestCase):
    @mock.patch("edu_py_logger.logger.socket")
    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_init(self, logging_module_mock, socket_module_mock):
        socket_module_mock.gethostbyname.return_value = "127.0.0.1"

        LoggerService("name", "local")

        logging_module_mock.getLogger.assert_called_once_with("name")
        logging_module_mock.LoggerAdapter.assert_called_once_with(
            logging_module_mock.getLogger.return_value,
            {
                "env": "local",
                "service_name": "name",
                "ipv4": "127.0.0.1",
                "trace_id": "",
                "correlation_id": "",
                "user_id": "",
            },
        )

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_info(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.info("message")

        logger_mock.info.assert_called_once_with("message")
        assert logger_mock.extra == {}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_info_with_extra(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.info("message", extra={"trace_id": "trace_id"})

        logger_mock.info.assert_called_once_with("message")
        assert logger_mock.extra == {"trace_id": "trace_id"}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_debug(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.debug("message")

        logger_mock.debug.assert_called_once_with("message")
        assert logger_mock.extra == {}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_debug_with_extra(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.debug("message", extra={"trace_id": "trace_id"})

        logger_mock.debug.assert_called_once_with("message")
        assert logger_mock.extra == {"trace_id": "trace_id"}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_warning(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.warning("message")

        logger_mock.warning.assert_called_once_with("message")
        assert logger_mock.extra == {}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_warning_with_extra(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.warning("message", extra={"trace_id": "trace_id"})

        logger_mock.warning.assert_called_once_with("message")
        assert logger_mock.extra == {"trace_id": "trace_id"}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_error(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.error("message")

        logger_mock.error.assert_called_once_with("message")
        assert logger_mock.extra == {}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_error_with_extra(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.error("message", extra={"trace_id": "trace_id"})

        logger_mock.error.assert_called_once_with("message")
        assert logger_mock.extra == {"trace_id": "trace_id"}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_exception(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.exception("message")

        logger_mock.exception.assert_called_once_with("message", exc_info=True)
        assert logger_mock.extra == {}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_exception_with_extra(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.exception("message", extra={"trace_id": "trace_id"})

        logger_mock.exception.assert_called_once_with("message", exc_info=True)
        assert logger_mock.extra == {"trace_id": "trace_id"}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_critical(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.critical("message")

        logger_mock.critical.assert_called_once_with("message")
        assert logger_mock.extra == {}

    @mock.patch("edu_py_logger.logger.logging")
    def test_logger_critical_with_extra(self, logging_module_mock):
        logger_mock = mock.MagicMock()
        logging_module_mock.LoggerAdapter.return_value = logger_mock

        service = LoggerService("name", "local")
        service.critical("message", extra={"trace_id": "trace_id"})

        logger_mock.critical.assert_called_once_with("message")
        assert logger_mock.extra == {"trace_id": "trace_id"}
