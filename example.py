#!/usr/bin/env python

import pysctl as pc


what = "net/core/rmem_max"

orig = pc.read(what)
print "Original Value:\t", orig


try:
    pc.write(what, int(orig)/2)
except pc.WriteError as e:
    print e
    pass

print "New Value:\t", pc.read(what)


try:
    pc.write(what, orig)
except pc.WriteError as e:
    print e
    pass

print "Reset Value:\t", pc.read(what)


try:
    print pc.read("net.ipv4.tcp_fastopen_key")
except pc.ReadError as e:
    print e
    pass


