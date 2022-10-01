
import asyncio
import argparse
import sys


def Packet_Generator(address, port):

    fuz = b""
    while(1):
        fuz += b"a"*100
        yield fuz+B"\x0A"
        ##yield header + content


async def main():
    n = 1
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip_address','-ip', type=str, help='target\'s address')
    parser.add_argument('--port', '-p', type=int)

    args = parser.parse_args()

    packet = Packet_Generator(args.ip_address,args.port)

    count = 0
    try:
        """reader, writer = await asyncio.open_connection(
                host=ip, port=port)"""
        while(1):
            reader, writer = await asyncio.open_connection(
                host=args.ip_address, port=args.port)
            d = next(packet)

            writer.write(d)
            reply = await reader.read()
            reply = reply.decode()
            if("without error" in reply):
                print(reply)
                print(count)
                count += 1
            else:
                print("coumt {}".format(count))
                break


        
    except OSError:
        print('connection fail')
        sys.exit(1)

asyncio.run(main())
