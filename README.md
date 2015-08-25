# pysctl
A Python interface for sysctl via procfs for Linux

The two functions `pysctl.read(key)` and `pysctl.write(key, value)` provide a simple interface to the settings stored in `/proc/sys`. The keys can be given in different forms as it is passed into a harmonizing function (`pysctl.clean_key(key)`). Thus, all of the following forms will be understood as the same key:

- /proc/sys/net/ipv4/tcp_rmem
- net/ipv4/tcp_rmem
- proc.sys.net.ipv4.tcp_rmem
- net.ipv4.tcp_rmem

A pretty printer (`pysctl.printable_key(key)`) is also available using the last form in the above list.

The return value of the read() function will always be a (stripped) string. Conversions, e.g., if it was a numerical value, should be done after reading values.

In case of an error, reading and writing will raise the exceptions `pysctl.ReadError` and `pysctl.WriteError`, respectively. Both share the base class `pysctl.Error`.

Also see the enclosed [example](example.py) for how to use the module.