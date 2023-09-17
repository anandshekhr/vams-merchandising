from hashids import Hashids
from django.conf import settings

hashids = Hashids(settings.HASHIDS_SALT, min_length=8)


def h_encode(id):
    
    return hashids.encode(id)


def h_decode(h):
    z = hashids.decode(h)
    if z:
        return z[0]


class HashIdConverter:
    regex = '[a-zA-Z0-9]{8,}'

    def to_python(self, value):
        print(type(value))
        return h_decode(value)

    def to_url(self, value):
        return h_encode(value)
    
class FloatConverter:
    # regex = '[\d\.\d]+'
    regex = '[0-9]+\.?[0-9]+'

    def to_python(self, value):
        
        return float(value)

    def to_url(self, value):
        return '{}'.format(value)  

class RomanNumeralConverter:
    regex = '[MDCLXVImdclxvi]+'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return '{}'.format(value)

