import os
from adara_privacy.utils.config import (
    Config,
    CONFIG_ENVIRONMENT_VARIABLE,
)

from adara_privacy.utils.strings import (
    is_stringable,
    is_empty_string,
    identifiers_as_single_str,
)

if CONFIG_ENVIRONMENT_VARIABLE in os.environ and not is_empty_string(os.environ[CONFIG_ENVIRONMENT_VARIABLE]):
    sdk_config = Config()
else:
    sdk_config = None
