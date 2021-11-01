def ListConversionDictionary(keys, values, Conversion=False):
    dictionary = {}
    ListSetDictionary = []
    if Conversion:
        for key, value in zip(keys, values):
            KeyValue = dictionary.fromkeys([key], value)
            ListSetDictionary.append(KeyValue)
        return ListSetDictionary
    else:
        for key, value in zip(keys, values):
            KeyValue = dictionary.fromkeys([key], value)
            dictionary.update(KeyValue)
        return dictionary

