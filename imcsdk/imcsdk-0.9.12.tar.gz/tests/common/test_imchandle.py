# Copyright 2015 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nose.tools import assert_equal
from imcsdk.imchandle import ImcHandle


def test_001_create_handle():
    handle = ImcHandle("192.168.1.1", "admin", "my_extra_secure_password")
    assert_equal(handle.username, "admin")
    assert_equal(handle.ip, "192.168.1.1")

