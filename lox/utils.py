import typing 

def nth_line_of_string(string: str, line_number: int) -> str:
    return "" 

def loxify(f):

    if f is True:
        return "true"
    elif f is False: 
        return "false" 
    elif f == None:
        return "nil"
    else:
        return f 

def supports_in_operator(obj):
    return hasattr(obj, "__contains__")