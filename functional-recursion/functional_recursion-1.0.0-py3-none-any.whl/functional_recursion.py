_RECURSE_ID = "__recurse__"
_YIELD_ID = "__recurse_yield__"


def recur(*args, **kwargs):
    """Wrapper for avoiding overflowing the stack
    
    Using a tuple is significantly faster 
    than instantiating a class or raising error.
    """
    return (_RECURSE_ID, args, kwargs)


def tail_recursive(f):
    """Perform tail recursion and return the final result
    
    This assumes that the final result is not a three element tuple
    that is equal to the ID constant
    """
    def decorated(*args, **kwargs):
        # avoid using the stack too much by matching and looping 
        while True:
            result = f(*args, **kwargs)
            # see if the result matches, otherwise return
            try:
                type, args, kwargs = result
                if type != _RECURSE_ID:
                    return result
            except:
                return result
    return decorated


def recur_yield(*args, yield_val=None, **kwargs):
    """Wrapper for avoiding overflowing the stack
    
    Note: Be sure to assign yield_val to something or
    the generator will contain only None(s)
    
    Using a tuple is significantly faster 
    than instantiating a class or raising error.
    """
    return (_YIELD_ID, yield_val, args, kwargs)


def tail_recursive_yield(f):
    """Perform tail recursion and yield the results along the way
    
    This assumes that the final result is not a four element tuple
    that is equal to the ID constant
    """
    def decorated(*args, **kwargs):
        # avoid using the stack too much by matching and looping 
        while True:
            result = f(*args, **kwargs)
            # see if the result matches, otherwise return
            try:
                type, yield_val, args, kwargs = result
                # yield to the generator
                yield yield_val
                if type != _YIELD_ID:
                    return result
            except:
                return result
    return decorated
