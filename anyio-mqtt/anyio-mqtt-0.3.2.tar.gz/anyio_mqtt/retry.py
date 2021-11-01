# from typing import Tuple, Type, Union

# from tenacity.retry import retry_if_exception


# class retry_if_not_exception_type(retry_if_exception):
#     """Retries except an exception has been raised of one or more types."""

#     def __init__(
#         self,
#         exception_types: Union[
#             Type[BaseException],
#             Tuple[Type[BaseException], ...],
#         ] = Exception,
#     ) -> None:
#         self.exception_types = exception_types
#         super().__init__(lambda e: not isinstance(e, exception_types))
