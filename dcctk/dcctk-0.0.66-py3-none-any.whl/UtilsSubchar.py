from .UtilsConcord import match_mode

SUBCHAR_ATTRS = set('compo idc radical phon sys'.split())


def is_subchar(tk:dict):
    keys = tk.get('match', {}).keys()
    for k in SUBCHAR_ATTRS:
        if k in keys: return True
    return False    


def has_cql_match_type(query, type_='regex'):
    for tk in query:
        for tp in ['match', 'not_match']:
            for k, values in tk.get(tp, {}).items():
                if k != 'char': continue
                for v in values:
                    if match_mode(v)[-1] == type_:
                        return True
    return False

def has_plain_cql(query):
    for tk in query:
        for k in tk.get('match', {}):
            if k == 'char': return True
        for k in tk.get('not_match', {}):
            if k == 'char': return True
    return False


def all_plain_cql(query):
    for tk in query:
        for tp in ['match', 'not_match']:
            for k in tk.get(tp, {}):
                if k in SUBCHAR_ATTRS: return False
    return True 