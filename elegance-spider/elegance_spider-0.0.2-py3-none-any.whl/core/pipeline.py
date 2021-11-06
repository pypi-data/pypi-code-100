'''管道组件'''


class Pipeline(object):
    '''管道组件'''

    def process_item(self, item):
        '''处理item'''
        print("item", item)
