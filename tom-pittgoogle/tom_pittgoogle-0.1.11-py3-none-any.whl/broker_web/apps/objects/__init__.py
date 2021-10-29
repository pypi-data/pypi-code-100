# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""A django application for serving data concerning recently observed
astronomical objects. The focus of this app is on the object itself, and not
the corresponding alerts.
"""

# Todo-objects:
# - Add / use PubSub configuration to / from global settings
# - Populate the ObjectsJsonView view using PubSub messages
# - Use arguments from the filter results from to filter values in ObjectsJsonView
# - Move ``forms.topics`` into global settings
