from . import call_character
from test_first import test_first_exception
import test_first.expectations.call
from test_first import expectations
import test_first.call_modifiers.synchronous
import test_first.call_modifiers.asynchronous
import test_first.call_modifiers.awaitable
import test_first.call_modifiers.trivial

class ExpectationMaker:
    def __init__(self, scenario, scenarioMocks, path, character: call_character.CallCharacter):
        self.__scenario = scenario
        self.__scenarioMocks = scenarioMocks
        self.__path = path
        self.__character = character

    def __getattr__( self, name ):
        childPath = f'{self.__path}.{name}'
        return ExpectationMaker(self.__scenario, self.__scenarioMocks, childPath, self.__character)

    def __call__(self, *args, **kwargs):
        call = self.__generate_expectation(*args, **kwargs)
        self.__scenario.addEvent(call)
        if call.extra_path is not None:
            extra = expectations.call.Call(call.extra_path, test_first.call_modifiers.trivial.Trivial)
            self.__scenario.addEvent(extra)
        return call

    def __generate_expectation(self, *args, **kwargs):
        if self.__character.normal:
            modifier = test_first.call_modifiers.trivial.Trivial
        if self.__character.awaitable:
            modifier = test_first.call_modifiers.awaitable.Awaitable
        if self.__character.is_sync_context:
            modifier = test_first.call_modifiers.synchronous.Synchronous
        if self.__character.is_async_context:
            modifier = test_first.call_modifiers.asynchronous.Asynchronous

        return expectations.call.Call(self.__path, modifier, *args, **kwargs)
