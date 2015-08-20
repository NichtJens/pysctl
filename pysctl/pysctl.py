import os
import string

base = "/proc/sys"
delim = os.path.sep
delim_alt = "."
base = base.split(delim)


def remove_prefix(p, l):
    """Remove prefix p from start of line l"""
    if l.startswith(p):
        return l[len(p):]
    else:
        return l


def clean_key(k):
    """Clean the key k"""
    k = k.replace(delim_alt, delim)
    k = k.strip(string.whitespace + delim)

    for b in base[1:]:
        k = remove_prefix(b, k)
        k = k.strip(string.whitespace + delim)

    return delim.join(base + [k])


def printable_key(k):
    """Pretty printed version of the key k"""
    k = clean_key(k)
    k = k.replace(clean_key(""), "")
    k = k.replace(delim, delim_alt)
    return k


def clean_value(v):
    """Clean the value v"""
    return str(v).strip()


def read(k):
    """Read and return value for key k"""
    k = clean_key(k)

    try:
        with open(k, 'r') as f:
            v = f.readline()
    except IOError as e:
        raise ReadError(e.strerror, e.filename)

    return clean_value(v)


def write(k, v):
    """Write value v to key k"""
    k = clean_key(k)
    v = clean_value(v)

    try:
        with open(k, 'w') as f:
            f.write(v)
    except IOError as e:
        raise WriteError(e.strerror, e.filename, v)





class Error(Exception):
    pass

class ReadError(Error):
    def __init__(self, error, key):
        msg = "{} when trying to read from {}".format(error, key)
        super(ReadError, self).__init__(msg)

class WriteError(Error):
    def __init__(self, error, key, value):
        msg = "{} when trying to write {} to {}".format(error, value, key)
        super(WriteError, self).__init__(msg)



