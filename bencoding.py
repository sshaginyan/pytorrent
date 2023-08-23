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
    # TODO: make this work with weird character § or 0xa7
    # string = string.decode('ascii')
    offset = colon_offset + length
    return (string, file_bytes[offset:])


# TODO: Complete encode function
def encode(struct):
    '''
        Description of encode function
    '''
    pass

# TODO: The return of this function is a tupal (structure, b'')
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
        return l, file_bytes
    elif file_bytes[:1] == b'd':
        d = {}
        file_bytes = file_bytes[1:]
        while file_bytes[:1] != b'e':
            key, file_bytes = decode(file_bytes)
            # TODO: Understand why I need this with my example,
            # but not when using a torrent file
            #file_bytes = file_bytes[1:]
            value, file_bytes = decode(file_bytes)
            d[key] = value
        file_bytes = file_bytes[1:]
        return d, file_bytes
    elif file_bytes[:1] == b'i':
        return _parse_integer(file_bytes)
    elif 48 <= file_bytes[0] <= 57:
        return _parse_string(file_bytes)

with open('big-buck-bunny.torrent', 'rb') as fd:
    b = fd.read()
    decode(b)
# print(decode(b'li3eli45ell4:spani1ei2eeeli24eeei7ed3:now:d2:hi:3:byeeee'))