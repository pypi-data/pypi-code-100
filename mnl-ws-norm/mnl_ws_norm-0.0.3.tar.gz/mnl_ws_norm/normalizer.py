'''
Copyright 2021 Rairye
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''

def trim_result(result):
    beginning_spaces = 0

    for i in range(len(result)):
        if result[i].isspace():
            beginning_spaces+=1
            
        else:
            break

    if beginning_spaces > 1:
        result = result[i:]

    ending_spaces = 0
    j = len(result)-1

    while j >= 0:
        current_char = result[j]
        if current_char.isspace():
            ending_spaces+=1
            j-=1
            
        else:
            break
        
    if ending_spaces > 1:
        result = result[:j+1]

    return result

def get_category(char):
    if char.isspace():
        return "SPACE"

    return "NOTSPACE"

def norm_spaces(input_str, space_type, remove_extra_spaces = False):
    if type(input_str) != str or type(space_type) != str:
        return input_str

    if len(input_str) == 0:
        return input_str
    
    result = ""
    last_category = ""
    last_replacement = None
    string_len = len(input_str)

    for i in range (string_len):
        current_char = input_str[i]
        current_category = get_category(current_char)

        if current_category == "SPACE":
            if (last_category == "SPACE" and remove_extra_spaces == False) or last_category != "SPACE":
                result+= (input_str[0 if last_replacement == None else last_replacement + 1: i] + space_type)

            last_replacement = i
            
            last_category = current_category
            continue
            
        last_category = current_category

    if last_replacement == None:
        return input_str

    if last_replacement < string_len - 1:
        result+=input_str[last_replacement+1:]
    
    return result if remove_extra_spaces == False else trim_result(result)

def split_by_spaces(input_str):
    if type(input_str) != str:
        return input_str

    words = []
    last_category = ""
    i = 0
    j = 0

    while j < len(input_str):
        current_char = input_str[j]
        current_category = get_category(current_char)

        if current_category == "SPACE" and last_category == "NOTSPACE":
            words.append(input_str[i:j])
            j+=1
            i=j

        elif current_category == "SPACE" and last_category == "SPACE":
            j+=1
            i=j

        elif current_category == "NOTSPACE" and last_category == "SPACE" :
            i=j
            j+=1
            
        else:
            j+=1

        last_category = current_category    

    if j-i > 0:
        words.append(input_str[i:])

    return words
