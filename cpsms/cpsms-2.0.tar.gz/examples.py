"""
Copyright 2010-2021 Mikkel Munch Mortensen <3xm@detfalskested.dk>.

This file is part of SMS Gateway.

SMS Gateway is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SMS Gateway is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SMS Gateway.  If not, see <http://www.gnu.org/licenses/>.
"""

import cpsms


# This will send text messages to Bob and Carol respectively. On their
# devices, the sender will shown as "Alice".

gateway = cpsms.Gateway("username", "password", "Alice")
gateway.send("4512345678", "Hello Bob")
gateway.send("4587654321", "Hello Carol")

# The `.send()` method will return the response from the SMS gateway. Have a
# look at the CPSMS documentation to see what responses look like:
# <https://api.cpsms.dk/documentation/index.html#send>
