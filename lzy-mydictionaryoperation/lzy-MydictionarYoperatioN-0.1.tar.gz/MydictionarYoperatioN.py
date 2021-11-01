def MydictionarYoperatioN(dictionary,operation,**kwargs):
    if operation == 'min':
        return min(dictionary.items(), key=lambda k: k[0])
    elif operation == 'max':
        return max(dictionary.items(), key=lambda k: k[0])
    elif operation == 'filter':
        return list(filter(lambda k: eval(kwargs.get('relation')),dictionary.items()))
    elif operation == 'sorted':
        return sorted(dictionary.items(), key=lambda kv: kv[0],reverse=kwargs.get('reverse'))
