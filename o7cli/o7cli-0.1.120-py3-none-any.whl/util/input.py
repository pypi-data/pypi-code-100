#!/usr/bin/env python
#************************************************************************
# Copyright 2021 O7 Conseils inc (Philippe Gosselin)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#************************************************************************
""" Package with function to request input from user"""
import inspect

import o7lib.util.displays as o7d


#*************************************************
# https://www.geeksforgeeks.org/class-as-decorator-in-python/
#*************************************************
class InputDecorator:
    """Decorator Class to add format to Input functions"""

    def __init__(self, function):
        self.function = function
        self.defaultQuestion = None

        signature = inspect.signature(function)
        for param in signature.parameters.values():
            #print(f'{param.name} -> default: {param.default}')
            if param.name == 'question':
                self.defaultQuestion = param.default

    def __call__(self, question = None, color = o7d.Colors.ACTION, **kwargs):

        if question is None:
            question = self.defaultQuestion

        if color is not None:
            question = f'{color}{question}{o7d.Colors.ENDC}'

        result = self.function(question, **kwargs)

        return result



#*************************************************
#
#*************************************************
def GetInput(question):
    """Stub in front of inputs"""
    return input(question)


#*************************************************
#
#*************************************************
@InputDecorator
def IsItOk(question='Is it OK'):
    """Ask a question and wait for a boolean answer"""
    newQuestion = f'{question} (y/n):'
    while True:
        key = GetInput(newQuestion)
        if key.lower()  == 'y':
            return True
        if key.lower()  == 'n':
            return False


#*************************************************
#
#*************************************************
@InputDecorator
def WaitInput(question='Press to continue'):
    """Wait for any input to continue"""
    return GetInput(question)

#*************************************************
#
#*************************************************
@InputDecorator
def InputInt(question='How much ?(int)'):
    """Ask and expects an integer"""

    try:
        ret=int(GetInput(question))
    except ValueError:
        print("Not an integer")
        return None

    return ret

#*************************************************
#
#*************************************************
@InputDecorator
def InputString(question='Enter Text'):
    """Request a Text String"""

    try:
        ret=str(GetInput(question))
    except ValueError:
        print("Not a Sting")
        return None

    return ret

#*************************************************
#
#*************************************************
@InputDecorator
def InputMulti(question='Enter Text or Int :', **kwargs):
    """Request a Text String or an Integer"""

    val = None
    inputType = None
    rxInput = GetInput(question)

    try:
        inputType='int'
        val=int(rxInput)
    except ValueError:
        inputType=None
        val=None

    if inputType is None :
        try:
            inputType='str'
            val=str(rxInput)
        except ValueError:
            inputType=None
            val=None

    return (inputType, val)


#*************************************************
# To Pacakage
#*************************************************
if __name__ == "__main__":

    theVal = InputMulti()
    print(theVal)
