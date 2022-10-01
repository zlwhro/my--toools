
import asyncio
import argparse


def Packet_Generator(address, path,mode):

    fuz = b""
    while(1):
        fuz += b"a"*100
        yield fuz
        ##yield header + content


async def main():
    n = 1
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip_address','-ip', type=str, help='target\'s address')
    parser.add_argument('--port', '-p', type=int)

    args = parser.parse_args()

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
