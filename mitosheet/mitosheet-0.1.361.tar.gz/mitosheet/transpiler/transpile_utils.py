

def column_header_to_transpiled_code(column_header):
    """
    Makes sure the column header is correctly transpiled to 
    code in a way that makes sure it's referenced properly
    """
    if isinstance(column_header, int) or isinstance(column_header, float) or isinstance(column_header, bool):
        return str(column_header)
    return f'\'{column_header}\''