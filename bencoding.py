import re

def _parse_integer(file_bytes):
    search = re.search(b'(?<=i)-?\d+(?=e)', file_bytes)
    integer = int(search.group())
    offset = search.span()[1] + 1
    return (integer, file_bytes[offset:])

def _parse_string(file_bytes):
    match = re.search(b'^\d+(?=:)', file_bytes)
    length = int(match.group())
    colon_offset = match.span()[1] + 1
    string = file_bytes[colon_offset:colon_offset + length]
    offset = colon_offset + length
    return (string, file_bytes[offset:])

def encode(obj):
    '''
        Description of encode function
    '''

    if(type(obj) == int):
        return b'i' + str(obj).encode() + b'e'
    elif(type(obj) == bytes):
        return str(len(obj)).encode() + b':' + obj
    elif(type(obj) == list):
        items = [encode(e) for e in obj]
        return b'l' + b''.join(items) + b'e'
    elif(type(obj) == dict):
        items = [encode(key)+encode(value) for key, value in obj.items()]
        return b'd' + b''.join(items) + b'e'
    
    # TODO: There must be an else here to handle a condition

def decode(file_bytes):

    # TODO: Add docstring
    '''
        Description of decode function
    '''

    # TODO: Do I need to have to conditions for b'l' and b'd'?

    if file_bytes[:1] == b'l':
        l = []
        file_bytes = file_bytes[1:]
        while file_bytes[:1] != b'e':
            value, file_bytes = decode(file_bytes)
            l.append(value)
        file_bytes = file_bytes[1:]
        if not file_bytes: return l
        return l, file_bytes
    elif file_bytes[:1] == b'd':
        # TODO: All keys must be byte strings and must appear in
        # lexicographical order
        d = {}
        file_bytes = file_bytes[1:]
        while file_bytes[:1] != b'e':
            key, file_bytes = decode(file_bytes)
            value, file_bytes = decode(file_bytes)
            d[key] = value
        file_bytes = file_bytes[1:]
        if not file_bytes: return d
        return d, file_bytes
    elif file_bytes[:1] == b'i':
        return _parse_integer(file_bytes)
    elif 48 <= file_bytes[0] <= 57:
        return _parse_string(file_bytes)
    # TODO: There must be an else here to handle a condition