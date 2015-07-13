import os
import string

base = "/proc/sys"
delim = os.path.sep
base = base.split(delim)


def remove_prefix(p, l):
    """Remove prefix p from start of line l"""
    if l.startswith(p):
        return l[len(p):]
    else:
        return l


def clean_key(k):
    """Clean the key k"""
    k = k.replace(".", delim)
    k = k.strip(string.whitespace + delim)

    for b in base[1:]:
        k = remove_prefix(b, k)
        k = k.strip(string.whitespace + delim)

    return delim.join(base + [k])


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
        print '{} when trying to read from {}'.format(e.strerror, e.filename)
        return None

    return clean_value(v)


def write(k, v):
    """Write value v to key k"""
    k = clean_key(k)
    v = clean_value(v)

    try:
        with open(k, 'w') as f:
            f.write(v)
    except IOError as e:
        print '{} when trying to write {} to {}'.format(e.strerror, v, e.filename)
        return False

    return True


