# high value hash highway visualization

**virtualenv (OPTIONAL)**
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
```
sudo apt-get install python-tk
```
**create empty csv**
```
touch csv/hash_bits.csv
```
**crawl data**
```
python3 src/bitcoinhash.py
```

**visualize**
```
python3 src/visualize.py
```

**Reference**
- [high value hash highway](https://bitcointalk.org/index.php?topic=98986.0)
- [21e800](https://medium.com/coinmonks/00000000000000000021e800c1e8df51b22c1588e5a624bea17e9faa34b2dc4a-cd4b67d446be)
