# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""A django application for serving up data about recently observed LSST/ZTF
alerts published in a collection of configured PubSub topics.
"""

# Todo alerts:
# - Add / use PubSub configuration to / from global settings
# - Populate the AlertsJsonView view using PubSub messages
# - Use arguments from the filter results from to filter values in AlertsJsonView
# - Move ``forms.topics`` into global settings
