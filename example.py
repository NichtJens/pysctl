#!/usr/bin/env python

from pysctl import read, write


what = "net/core/rmem_max"

orig = read(what)
print read(what)

write(what, int(orig)/2)
print read(what)

write(what, orig)
print read(what)

print read("net.ipv4.tcp_fastopen_key")

