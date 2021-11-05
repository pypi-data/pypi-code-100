def get_test_template(path):
    txt = """\
import os


def test():
    # set default path
    os.environ.setdefault('DATAPATH', os.path.join('%s', 'test', 'datapath'))
    os.environ.setdefault('STASHPATH', os.path.join('%s', 'test', 'stashpath'))
    os.environ.setdefault('SAVEDPATH', os.path.join('%s', 'test', 'savedpath'))
    
    # set default env
    json_template = {
        'env': {'None': None},
        'CPU': 1
    }
    
    for k, v in json_template.items():
        if k != 'env':
            os.environ.setdefault(k, str(v))
        else:
            for env_k, env_v in json_template['env'].items():
                os.environ.setdefault(env_k, str(env_v))
                
    # test your code here
    pass
    
    
if __name__ == '__main__':
    test()
"""
    txt = txt % (path, path, path)
    return txt
