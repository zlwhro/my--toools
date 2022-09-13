#! /bin/python

import asyncio
import re
import sys
import copy

async def smtp_read(fd, reader, n, q: asyncio.Queue) -> None:
    count = 0
    lock = asyncio.Lock()
    while(count < n):
        reply = await reader.readline()
        result = reply.decode()
        state = result[:3]
        
        if(state=='252'):
            try:
                name = result.split()[2]
                print('found existing name {}'.format(name))
                print(result)
                async with lock:
                    fd.write(name+'\n')
            except RuntimeError:
                print('runt time error')
                print(result)
                
            count +=1
        elif(state=='550'):
            count += 1
        else:
            if(state != '220'):
                count += 1
            print(result)
        
        await q.put(count+10)
        

async def smtp_write(namelist,writer, q: asyncio.Queue) -> None:
    for name in namelist:
        k = await q.get()    
        message = 'VRFY '+  name + '\r\n'
        writer.write(message.encode())



async def smtp_enum(fd, qq, name):
    try:
        reader, writer = await asyncio.open_connection(
                host='10.11.1.217', port=25)
    except OSError:
        print('connection fail')
    
    print('connection sucess')
    q = asyncio.Queue()
    for i in range(10):
        await q.put(i)

    n = len(name)

    producer = asyncio.create_task(smtp_read(fd, reader, n, q))
    consumer = asyncio.create_task(smtp_write(name,writer,q))
    await consumer
    await producer
    
    print('enumeration complete')
    writer.write('QUIT'.encode())
    print('send:QUIT')
    writer.close()
    await writer.wait_closed()
    print('connetion was closed')
    await qq.put(0)

async def aaaa(readfile, writefile):
    namelist = []
    enumer = []
    f = open(readfile, "r")
    f2 = open(writefile, "a")

    c = 0
    q = asyncio.Queue()
    for i in range(10):
        await q.put(0)
    
    while(True):
        line = f.readline()
        if(len(line) > 0):
            namelist.append(copy.deepcopy(line[:-1]))
            if(len(namelist)==20): 
                await q.get()
                enumer.append(asyncio.create_task(smtp_enum(f2, q,copy.deepcopy(namelist) )))
                namelist=[]
                print("connection",c)
                c += 1
        else:
            if(len(namelist)):
                await q.get()
                enumer.append(asyncio.create_task(smtp_enum(f2, q, copy.deepcopy(namelist)))) 
                print("last connection")
                print(namelist)
                break


    await asyncio.gather(*enumer)
    print("end eunmeration")
    f.close()

if __name__=="__main__":

    if(len(sys.argv)<3):
        print("usage: ")
    else:
        asyncio.run(aaaa(sys.argv[1],sys.argv[2]))

