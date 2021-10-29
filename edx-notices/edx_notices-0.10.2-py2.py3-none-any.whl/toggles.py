"""This file houses all the toggles, namely waffle switches and flags."""
from edx_toggles.toggles import WaffleFlag


# .. toggle_name: notices.enable_notices
# .. toggle_implementation: WaffleFlag
# .. toggle_default: False
# .. toggle_description: If enabled, the unacknowledged notices API will return notices the user hasn't acknowledged
# .. toggle_use_cases: opt_in
# .. toggle_creation_date: 2021-10-07
ENABLE_NOTICES = WaffleFlag("notices.enable_notices", module_name=__name__, log_prefix="notices")
