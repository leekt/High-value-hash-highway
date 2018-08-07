import numpy as np
from bitarray import bitarray
from binascii import hexlify
from matplotlib import pylab
import csv
import math

def hash_value(h):
    return 256 - np.log2(float(h))
    
#    value = 0
#    for i in range(0,32):
#        if h[i] == 0:
#            value = value + 8
#            continue
#        else:
#            value = value + 8 - np.log2(h[i::])
#            return value
#    return value

def nbits_to_target(bits):
    coeff = bits & 0x00ffffff
    expon = ((bits & 0xff000000) >> 24) - 3
    target = coeff * 2 ** (8*expon)
    # print("TARGET : "+ str(target))
    return target

def target_to_work(target):
    return (2**256) / float(target)

def scan():
    f = open('./csv/hash_bits.csv','r')
    f_csv = csv.reader(f)

    data = list(f_csv)
    data = data[1::]

    result = []
    for row in data:
        height = row[0]
        work = target_to_work(nbits_to_target(int(row[2])))
        value = hash_value(int(hexlify(bytes.fromhex(row[1])),16))
        result.append((height, work, value))
    
    return np.array(result,dtype='f8')

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

floor_diff = np.floor( dv[:,2] - np.log2(dv[:,1]) )
pylab.figure(3)
pylab.clf()
pylab.scatter(dv[:,0], floor_diff, s=0.1, label='Hash Values (bits)')
pylab.title('Hash Value - Difficulty')
pylab.ylabel('Hash Value (zero bits) (log2(hash))')
pylab.xlabel('Time (blocks)')
pylab.legend(loc=4)

pylab.figure(4)
pylab.clf()
pylab.hist(floor_diff,color="green",alpha=0.8, histtype='bar', ec='black', bins=range(0,int(floor_diff.max())))
pylab.title('Hash Value - Difficulty Histogram')
pylab.yscale('log',basey=2)
pylab.xlabel('Hash Value - Difficulty')
pylab.ylabel('Counts')

pylab.show()
