# This file is part of ts_IntegrationTests.
#
# Developed for the Rubin Observatory Telescope and Site System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import yaml
from .config_registry import registry


# Add the script configurations to the configuration registry.

registry["auxtel_visit_config1"] = yaml.safe_dump(
    {
        "nimages": 1,
        "exp_times": 5.0,
        "image_type": "OBJECT",
        "filter": "FELH0600",
        "grating": "ronchi90lpmm",
        "linear_stage": None,
    },
    explicit_start=True,
    canonical=True,
)

registry["auxtel_visit_config2"] = yaml.safe_dump(
    {
        "nimages": 1,
        "image_type": "OBJECT",
        "exp_times": 5.0,
        "filter": "BG40",
        "grating": "ronchi90lpmm",
    },
    explicit_start=True,
    canonical=True,
)

registry["auxtel_visit_config3"] = yaml.safe_dump(
    {
        "nimages": 1,
        "image_type": "OBJECT",
        "exp_times": 5.0,
        "filter": "BG40",
        "grating": "holo4_003",
    },
    explicit_start=True,
    canonical=True,
)

registry["auxtel_visit_config4"] = yaml.safe_dump(
    {
        "nimages": 1,
        "image_type": "OBJECT",
        "exp_times": 5.0,
        "filter": "FELH0600",
        "grating": "holo4_003",
    },
    explicit_start=True,
    canonical=True,
)

registry["auxtel_visit_config5"] = yaml.safe_dump(
    {
        "nimages": 1,
        "image_type": "OBJECT",
        "exp_times": 5.0,
        "filter": "FELH0600",
        "grating": "empty_1",
    },
    explicit_start=True,
    canonical=True,
)

registry["auxtel_visit_config6"] = yaml.safe_dump(
    {
        "nimages": 1,
        "image_type": "OBJECT",
        "exp_times": 5.0,
        "filter": "BG40",
        "grating": "empty_1",
    },
    explicit_start=True,
    canonical=True,
)
