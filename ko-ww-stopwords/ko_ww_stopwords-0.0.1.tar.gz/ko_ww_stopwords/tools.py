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

from ko_ww_stopwords.stop_words import ko_ww_stop_words

def is_stop_word(word):
    return word in ko_ww_stop_words

def is_punct(char):
    if type(char) != str:
        return char
    if len(char) > 1 or len(char) == 0:
        return char

    return (char.isalpha() or (char.isnumeric() or char.isspace())) == False

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
