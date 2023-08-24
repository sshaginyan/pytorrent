import hashlib
import urllib.parse
from bencoding import encode, decode

sha1 = hashlib.sha1()

with open('Artificial_Intelligence.torrent', 'rb') as fd:
    a = fd.read()
    a = decode(a)
    a = a[b'info']
    a = encode(a)
    a = urllib.parse.quote(a)
    sha1.update(a.encode())
    print(sha1.hexdigest())