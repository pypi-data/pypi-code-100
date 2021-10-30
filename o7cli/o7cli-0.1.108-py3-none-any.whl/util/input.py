#!/usr/bin/python3
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



#*************************************************
#
#*************************************************
def GetInput(str): return input(str)


#*************************************************
#
#*************************************************
def IsItOk(question='Is it OK'):
    str = f'{question} (y/n):'
    while True:
        key = GetInput(str)
        if key.lower()  == 'y': return True
        if key.lower()  == 'n': return False


#*************************************************
#
#*************************************************
def WaitInput(question='Press to continue'):
    return GetInput(question)

#*************************************************
#
#*************************************************
def InputInt(question='How much ?(int)'):

    try:
        ret=int(GetInput(question))
    except ValueError:
        print("Not an integer")
        return None

    return ret

#*************************************************
#
#*************************************************
def InputString(question='Enter Text'):

    try:
        ret=str(GetInput(question))
    except ValueError:
        print("Not a Sting")
        return None

    return ret

#*************************************************
#
#*************************************************
def InputMulti(question='Enter Text or Int'):

    val = None
    t = None
    rxInput = GetInput(question)

    try:
        t='int'
        val=int(rxInput)
    except ValueError:
        t=None
        val=None

    if t is None :
        try:
            t='str'
            val=str(rxInput)
        except ValueError:
            t=None
            val=None

    return (t, val)


#*************************************************
# To Pacakage
#*************************************************
if __name__ == "__main__":

    val = InputMulti()
    print(val)

 
   