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

def is_punct(char):
    if type(char) != str:
        return False
    
    if len(char) > 1 or len(char) == 0:
        return False

    return ((char.isalpha() or char.isnumeric()) or char.isspace()) == False

def strip_outer_punct(word):
    if type(word) != str:
        return word

    i = 0

    while i < len(word):
        if is_punct(word[i]):
            i+=1
        else:
            break

    if i > 0:
        word = word[i:]

    last_char_index = len(word) -1
    j = last_char_index

    while j >=0:
        if is_punct(word[j]):
            j-=1
        else:
            break

    if j < last_char_index:
        return word[:j+1]

    return word


def get_category(char):
    if char.isspace():
        return "SPACE"

    return "PUNCT" if is_punct(char) else "NOTPUNCT"

def normalize_punct(input_str, mode, input_skips = "", replacement = " "):
    result = []
    skips = [] if type(input_skips) != str else set([char for char in input_skips])
    replacement = replacement if type(replacement) == str else " "
    last_replacement = None
    last_char = ""
    last_category = ""
    string_len = len(input_str)

    for i in range(string_len):
        current_char = input_str[i]
        current_category = get_category(current_char)

        if current_category == "PUNCT" and current_char not in skips:
            if mode == "REPLACE":
                if (last_char != replacement and last_category != "SPACE") or last_replacement == None:
                    result.append((input_str[0 if last_replacement == None else last_replacement + 1: i] + replacement))
                    
                else:
                    result.append(input_str[0 if last_replacement == None else last_replacement + 1: i])

                last_replacement = i
                last_char = replacement
                last_category = "REPLACEMENT"
                continue
                                    
            else:
                if last_replacement == None or (last_replacement != None and i - last_replacement > 1):
                    result.append(input_str[0 if last_replacement == None else last_replacement+1:i])
                    last_replacement = i

        if current_category == "SPACE" and mode == "REPLACE":
            if last_category == "REPLACEMENT":
                last_replacement = i

        last_char = current_char
        last_category = current_category
               
    if last_replacement == None:
        return input_str

    if last_replacement < string_len - 1:
        result.append(input_str[last_replacement+1:])
    
    return "".join(result)

def strip_punct(input_str, input_skips = ""):
    if type(input_str) != str:
        return input_str
    
    return normalize_punct(input_str, "STRIP", input_skips)

def replace_punct(input_str, input_skips = "", replacement= " "):
    if type(input_str) != str:
        return input_str
    
    return normalize_punct(input_str, "REPLACE", input_skips, replacement)
