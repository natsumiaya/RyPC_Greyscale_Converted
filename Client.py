__author__ = 'aya'

import rpyc
import os
import time
import threading

def totheserver(name,  nname, out, conn):
    for x in range (0, nname):
        with open(name[x], 'rb') as read_file:
            contents = read_file.read()
            with conn.root.open(name[x], 'wb') as create_file:
                print "sending to server..."
                create_file.write(contents)
                create_file.close()
                print "Converting Image..."
                converted = conn.root.dothemagic(name[x])
            read_file.close()
        print "receiving form server..."
        with open(os.path.join(out,name[x]), 'wb') as greyscaled:
            greyscaled.write(converted)
            greyscaled.close()

ipaddr = []
ipport = []
connect = []

inputpath = raw_input('Please enter the input folder path: ')
outputpath = raw_input('Please enter the input folder path: ')

nworker = raw_input('How many worker do you want to use? ')
nworker = int(nworker)

for i in range(0, nworker):
    print "for worker %d" %(i+1)
    ipaddr.append(raw_input('Please enter the IP Adress : '))
    ipport.append(raw_input('Please enter the port number : '))

for j in range(0, nworker):
    connect.append(rpyc.connect(ipaddr[j], ipport[j]))

arrayfile = []
start_time_total = time.time()
for filename in os.listdir(inputpath):
    arrayfile.append(filename)
narray = len(arrayfile)

os.chdir(inputpath)
thread = []
nfile = narray / nworker

for nthread in range(0, nworker):
    if nthread == nworker-1:
        if narray % nworker != 0:
            nfile +=1
    thread.append(threading.Thread(target=totheserver, args=(arrayfile, nfile, outputpath, connect[nthread])))
    thread[nthread].start()

for fthread in range (0, nworker):
    thread[fthread].join()

print ("Done converting all in %s seconds" % (time.time() - start_time_total))







