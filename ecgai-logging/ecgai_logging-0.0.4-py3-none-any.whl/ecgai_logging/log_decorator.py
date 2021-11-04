import functools
import inspect
import logging
from datetime import datetime
from pathlib import Path


def log(func):
    # Declared for use by the whole function but reset by wrapper function due to an issue with freeze_time in
    # testing classes
    start_time = datetime.utcnow()

    def pre_function_log(function, args, kwargs, is_async):
        logger = get_logger(function)
        if logger.isEnabledFor(logging.DEBUG) or logger.isEnabledFor(logging.INFO):
            logger.info(f"----------pre function call log----------")
            logger.info(module_name(function=function))
            logger.info(method_name(function=function))
            logger.debug(method_type(is_async=is_async))
            logger.debug(working_directory())
            logger.debug(start_time_string())
            logger.info(variables(function, args, kwargs))

    def post_function_log(function, result):
        logger = get_logger(function)
        if logger.isEnabledFor(logging.DEBUG) or logger.isEnabledFor(logging.INFO):
            logger.info(f"----------post function call log----------")
            logger.info(module_name(function=function))
            logger.info(method_name(function=function))

            finish_time = datetime.utcnow()
            logger.debug(f"End time:              {finish_time}")
            difference = finish_time - start_time
            elapsed_time = difference.total_seconds()
            logger.info(f"Elapsed time:           {elapsed_time} seconds")
            logger.info(returns(result=result))

            logger.info(
                f"_______________________________________________________________________________________"
            )

    def pre_function_variable_signature(function, args, kwargs):
        bound_args = inspect.signature(function).bind(*args, **kwargs)
        bound_args.apply_defaults()
        loop_count = 0
        args_display = []
        for a in bound_args.arguments.items():
            if a[0] != "self":
                arg_display = ''
                if a[0] == 'kwargs':
                    if len(kwargs) > 0:
                        arg_display = ', '.join([f"{k}={v!r}" for k, v in kwargs.items()])

                elif a[0] == 'args':
                    if len(args) > 0:
                        arg_display = str(args)

                else:
                    arg_display = f"{a[0]}: {type(a[1]).__name__} = {a[1]}"

                if len(arg_display) > 0:
                    args_display.append(arg_display)
            loop_count += 1

        signature = ", ".join(args_display)
        return signature

    def post_function_return_signature(result):
        if type(result) is tuple:
            signature = post_function_tuple_signature(result)

        else:
            signature = f"{type(result).__name__} = {result}"

        return signature

    def post_function_tuple_signature(result):
        signature = f"tuple["
        count = 0
        for r in result:
            if count > 0:
                signature += f", "
            signature += f"{type(r).__name__} = {r}"
            count += 1
        signature += f"]"
        return signature

    def function_error_log(function, exception, is_async, args, kwargs):
        logger = get_logger(function=function)
        logger.error(f"-----------------error log-----------------")
        logger.error(module_name(function=function))
        logger.error(method_name(function=function))
        logger.error(method_type(is_async=is_async))
        logger.error(working_directory())
        logger.error(start_time_string())
        logger.error(variables(function, args, kwargs))
        logger.exception(exception)
        result = None
        return result

    def get_logger(function):
        logger_name = function.__module__
        logger = logging.getLogger(logger_name)
        return logger

    def module_name(function):
        return f"Module name:            {function.__module__}"

    def method_name(function):
        return f"Method name:            {function.__qualname__}"

    def method_type(is_async):
        if is_async:
            return f"Method type:            asynchronous"
        else:
            return f"Method type:           synchronous"

    def working_directory():
        return f"Working directory:      {Path.cwd()}"

    def start_time_string():
        return f"Start time:             {start_time}"

    def variables(function, args, kwargs):
        return f"Variables:              {pre_function_variable_signature(function=function, args=args, kwargs=kwargs)}"

    def returns(result):
        return f"Returns:                {post_function_return_signature(result=result)}"

    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal start_time
            start_time = datetime.utcnow()
            async_result = None
            try:
                pre_function_log(func, args, kwargs, True)
                async_result = await func(*args, **kwargs)
            except Exception as e:  # only called if exception not caught is code or re-raised by function
                function_error_log(func, e, True, args, kwargs)
                raise
            finally:
                post_function_log(func, async_result)
            return async_result

        return wrapper
    else:

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal start_time
            start_time = datetime.utcnow()
            result = None
            try:
                pre_function_log(func, args, kwargs, False)
                result = func(*args, **kwargs)

            except Exception as e:  # only called if exception not caught is code or re-raised by function
                function_error_log(func, e, False, args, kwargs)
                raise
            finally:
                post_function_log(func, result)
            return result

        return wrapper
