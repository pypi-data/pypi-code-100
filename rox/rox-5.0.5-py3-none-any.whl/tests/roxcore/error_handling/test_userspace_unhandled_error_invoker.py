import unittest

from rox.core.error_handling.userspace_unhandled_error_invoker import UserspaceUnhandledErrorInvoker
from rox.core.error_handling.exception_trigger import ExceptionTrigger
from rox.core.logging.logging import Logging

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

class UserspaceUnhandledErrorInvokerTests(unittest.TestCase):
    def test_will_write_error_when_invoke_user_userhandled_error_invoked_handler_wasnt_set(self):
        user_unhandled_error_invoker = UserspaceUnhandledErrorInvoker()
        obj = '123'

        log = Mock()
        Logging.set_logger(log)

        user_unhandled_error_invoker.invoke(obj, ExceptionTrigger.CONFIGURATION_FETCHED_HANDLER, Exception('some exception'))
        
        self.assertEqual(1, len(log.error.call_args_list))
        args, _ = log.error.call_args_list[0]
        self.assertTrue('User Unhandled Error Occurred' in args[0])

    def test_will_write_error_when_involer_user_unhandled_error_invoker_threw_exception(self):
        user_unhandled_error_invoker = UserspaceUnhandledErrorInvoker()
        obj = '123'

        log = Mock()
        Logging.set_logger(log)

        def raise_(ex):
            raise ex
        handler = lambda userspace_unhandled_error_args: raise_(Exception('userUnhandlerError exception'))
        user_unhandled_error_invoker.set_handler(handler)
        user_unhandled_error_invoker.invoke(obj, ExceptionTrigger.CONFIGURATION_FETCHED_HANDLER, Exception('some exception'))

        self.assertEqual(1, len(log.error.call_args_list))
        args, _ = log.error.call_args_list[0]
        self.assertTrue('User Unhandled Error Handler itself' in args[0])
