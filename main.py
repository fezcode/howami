#!/usr/bin/env python
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from math import floor
from threading import local
import psutil
import asyncio
import websockets
import datetime
import getopt
import sys

interval = 1

async def do_stuff(websocket, path):
    while True:
        # Use a breakpoint in the code line below to debug your script.
        # gives a single float value
        cpu = psutil.cpu_percent()
        # gives an object with many fields
        # vm = psutil.virtual_memory()
        # you can convert that object to a dictionary
        dict(psutil.virtual_memory()._asdict())
        # you can have the percentage of used RAM
        vm_per = floor(psutil.virtual_memory().percent)
        # you can calculate percentage of available memory
        avm_per = floor(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
        # msg = "CPU     : {}\nVM_PER  : {}\nAVM_PER : {}\n".format(cpu, vm_per, avm_per);

        cpu_freq = psutil.cpu_freq().current
        disk_usage = psutil.disk_usage('/')
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        network = psutil.net_io_counters()
        
        msg = {
            "CPU": cpu,
            "VM": vm_per,
            "AVM_PER": avm_per,
            "CPU_FREQ": cpu_freq,
            "DISK_USAGE": disk_usage,
            "BOOT_TIME" : boot_time,
            "NETWORK": {
                "SENT_KB": floor(network.bytes_sent / 1024),
                "RECV_KB": floor(network.bytes_recv / 1024)
            }
        }
        
        await websocket.send(msg.__str__())
        print(msg)
        await asyncio.sleep(interval)




def usage():
    s = """
        howami
        ---------------------------------
        
        howami [hi:]
        
        Sends system and process information over Websocket (0.0.0.0:9090)
        """
    print(s)    



    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help", "interval="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        # usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--interval"):
            interval = int(a)
            print(interval)
        else:
            assert False, "unhandled option"
    
    
    start_server = websockets.serve(do_stuff, "0.0.0.0", 9090)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
