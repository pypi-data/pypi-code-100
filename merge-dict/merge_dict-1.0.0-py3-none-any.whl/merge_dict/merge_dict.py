def merge_obj(obj1, obj2):
    """
    递归合并两个字典所有数据,有相同的就更新，不相同的就添加
    :param dic1: 基本数据
    :param dic2: 以dic2数据为准，dic1和dic2都有的数据，合并后以dic2为准
    :return: 合并后的字典
    """

    # 类型不同就直接赋值,返回第2个参数数据，是因为我们以第2个数据为准，来更新第1个数据的。
    if type(obj1) != type(obj2):
        return obj2

    # 都是字典时处理
    if isinstance(obj2, dict):
        for k, v in obj2.items():

            obj1_value = obj1.get(k)
            if obj1_value is None:
                obj1[k] = v
            else:
                obj1[k] = merge_obj(obj1[k], obj2[k])


    elif isinstance(obj2, list):
        for i in range(len(obj2)):
            try:
                obj1[i] = merge_obj(obj1[i], obj2[i])
            except IndexError:
                obj1.append(obj2[i])

    elif isinstance(obj2, tuple):
        for i in range(len(obj2)):
            try:
                # 元组不能修改，先转list再修改后再转回元组
                obj1 = list(obj1)
                obj1[i] = merge_obj(obj1[i], obj2[i])
                obj1 = tuple(obj1)

            except IndexError:
                obj1 += (obj2[i],)


    else:
        # 以第2个参数数据为准，返回obj2
        return obj2

    return obj1


if __name__ == '__main__':
    d1 = {
        'name': 'xs',
        'age': 18,
        'data': [{'api3': 'api3'}, {'api4': 'api4'}],
        'testlist': {'method': 'post',
                     'testlist': [{'list3': 'li3', 'list9': 'list9'}, {'list4': 'list4'}, {'list11': 'list11'},
                                  {'list22': 'list22'}]},
        'testlist2': {'method': 'post', 'testlist': {'list5': 'li5'}},
        'testlist3': {'tup': ({'name': 'aa'}, 123), 'testlist': [{'list5': 'li5'}, 123, {'list6': 'list6'}]},
        'testlist4': {'tup': ({'name': 'aa'}, [{'age': '123'}, (123, 145, {'test': '099'}), 'abcd'])}

    }

    d2 = {
        'age': 19,
        'path': 'xxx/path',
        'method': {'method': 'get'},
        'testlist': {'method': 'get', 'testlist': [{'list3': 'li1'}, {'list7': 'list7'}, {'list8': 'list8'}]},
        'testlist2': {'method': 'get', 'testlist': [{'list6': 'li6'}]},
        'data': [{'api': 'api1'}, {'api4': 'api2'}, {'api5': 'api5'}],
        'testlist3': {'tup': ({'name': 'bb'}, 333), 'testlist': [234, {'list7': 'list7'}, {'list6': 'list7'}]},
        'testlist4': {'tup': ({'name': 'bb'}, [{'age': '456', 'name': 'xx'}, (456, 721, {'test': '888'}), 'dddd'])}
    }

    print(merge_obj(d1, d2))
