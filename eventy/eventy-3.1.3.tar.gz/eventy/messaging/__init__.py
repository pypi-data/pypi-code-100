# Copyright (c) Qotto, 2021

"""
Eventy messaging API

The messaging API itself is backend-agnostic, there is currently only a Kafka backend implemented.
"""
from eventy.messaging.agent import Agent, handle_event, handle_request, handle_response, Guarantee
from eventy.messaging.app import App
from eventy.messaging.errors import MessagingError
from eventy.messaging.service import Service
from eventy.messaging.store import Store, Cursor

__all__ = [
    # base
    'Service',
    # store
    'Store',
    'Cursor',
    # agent
    'Agent',
    'Guarantee',
    'handle_event',
    'handle_request',
    'handle_response',
    # app
    'App',
    # errors
    'MessagingError',
]
