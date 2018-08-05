import numpy as np
from bitarray import bitarray
from binascii import hexlify
import pylab
import csv
import math

def hash_value(h):
    value = 0
    for i in range(0,32):
        if h[i] == 0:
            value = value + 8
            continue
        else:
            value = value + 8 - np.log2(h[i])
            return value
    return value
def hash_value2(h):
    if h==0: return 256
    if h > (1<<256)-1: return 0
    c = 0

    while not (h & (1<<255)):
        h <<= 1
        c += 1

    return c

def nbits_to_target(bits):
    coeff = bits & 0x00ffffff
    expon = ((bits & 0xff000000) >> 24) - 3
    target = coeff * 2 ** (8*expon)
    # print("TARGET : "+ str(target))
    return target

def target_to_work(target):
    return (2**256) / float(target)

def scan():
    # data = np.genfromtxt('./csv/hash_bits.csv', dtype=(int,object,int), delimiter=',', names=True)[::-1]
    f = open('./csv/hash_bits.csv','r')
    f_csv = csv.reader(f)

    data = list(f_csv)
    data = data[1::]

    result = []
    for row in data:
        height = row[0]
        work = target_to_work(nbits_to_target(int(row[2])))
        value = hash_value(bytearray.fromhex(row[1]))
        # print("WORK: "+str(work) + "\tVALUE : "+str(value))
        result.append((height, work, value))
    return np.array(result,dtype='f8')[::-1]

dv = scan()
print(dv)

pylab.figure(1)
pylab.clf()
pylab.scatter(dv[:,0], dv[:,2], s=0.1, label='Hash Values (bits)')
pylab.plot(dv[:,0],np.log2(dv[:,1]), 'r', linewidth=2, label='Difficulty (minimum value)')
pylab.title('Hash Value vs Time')
pylab.ylabel('Hash Value (zero bits) (log2(hash))')
pylab.xlabel('Time (blocks)')
pylab.legend(loc=4)

work = np.cumsum(dv[:,1])
pylab.figure(2)
pylab.clf()
pylab.scatter(work, dv[:,2], s=0.1, label='Hash Values (bits)')
pylab.plot(work, np.log2(dv[:,1]),'r',linewidth=2, label='Difficulty (minimum value)')
pylab.title('Hash Value vs Work')
pylab.ylabel('Hash Value (zero bits) (log2(hash))')
pylab.xlabel('Cumulative Work (est. hashes computed)')
pylab.legend(loc=4)

pylab.show()
