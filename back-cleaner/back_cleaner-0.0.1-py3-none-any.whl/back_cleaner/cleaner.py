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

def strip_non_alpha(string):
    abc_set = set (["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "\\"])
    i = 0
	
    while i < len(string):
            if string[i] in abc_set:
                break
                    
            else:
                i+=1
    return string[i:]
	

def escape_script_tags(input_str):
    if type(input_str) != str:
        return input_str

    result = ""
    last_open = None
    last_replacement = None
    has_open = False
    input_length = len(input_str)
    
    for i in range(input_length):
            current_char = input_str[i];
            if current_char == "<" and has_open == False:
                if last_replacement == None or (last_replacement != None and i - last_replacement > 1):
                    result += input_str[0 if last_replacement == None else last_replacement + 1 : i]
                last_open = i
                has_open = True
                
            
            elif (current_char == "<" and has_open == True):
                    result+=input_str[last_open: i]
                    last_open = i

            
            elif (current_char == ">" and has_open == True):
                    search_string = input_str[last_open+1: i].lower()
                    if (not strip_non_alpha(search_string).startswith("script")):
                            result += input_str[last_open : i+1]
                    
                    else:
                        result += ("<\\" + input_str[last_open + 1: i+1])
                
                    has_open = False
                    last_replacement = i;
    
            
            else:
                continue		

            
    if last_open == None:
        return input_str
    
            
    if has_open == True:
        return result + input_str[last_open:]
    
    return result if input_length - 1 == last_replacement else (result+input_str[last_replacement+1:])


def replace_with_ents(input_str):
    if type(input_str) != str:
        return input_str

    reserved_chars = {"&" : "&amp;", "<" : "&lt;", ">" : "&gt;", "\"" : "&quot;", "\'" : "&#39;"}
    result = ""
    last_replacement = 0;
    string_len = len(input_str)

    for i in range (string_len):
        char = input_str[i]
        if char in reserved_chars:
            replacement = reserved_chars[char]
            result+= ((input_str[last_replacement : i ] + replacement) if  i > last_replacement else replacement)
            last_replacement = i + 1

    if last_replacement == 0:
        return input_str

    return result if last_replacement == string_len else result + input_str[last_replacement]

