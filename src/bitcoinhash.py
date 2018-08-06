import json
import requests
import csv

def getBlockchainHeight():
    url = 'https://blockchain.info/latestblock'
    response = requests.get(url)

    json_data = json.loads(response.text)
    return int(json_data['height']);

def getHash(num):
    # set url for json response
    url = 'https://blockchain.info/block-height/%d?format=json' % num
    response = requests.get(url)
    if response.ok :
        # get json data
        json_data = json.loads(response.text)
        return json_data['blocks'][0]['hash'], json_data['blocks'][0]['bits']
    else :
        raise ValueError('response not ok.')

f_ = open('./csv/hash_bits.csv','r')
csv_ = csv.reader(f_)
row_count = sum(1 for row in csv_)
f_.close()

f = csv.writer(open('./csv/hash_bits.csv', 'a'))

if row_count == 0 :
    print("EMPTY CSV")
    f.writerow(['height','hash','bits'])
else :
    print("LAST BLOCK HEIGHT STORED = %d" % (int(row_count)-2))

if row_count <= 0:
    row_count = 1

max_height = int(getBlockchainHeight())

for i in range(int(row_count)-1,max_height):
    try:
        h,b = getHash(i)
        print("#"+str(i)+"\t\t"+str(h)+"\t"+str(b))
        f.writerow([i,h,b])
    except ValueError as error:
        print('Caught this error: ' + repr(error))
        i = i-1

