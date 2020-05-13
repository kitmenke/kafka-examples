from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import signal
import sys
import time
from pathlib import Path
import json
import os.path

p = Path('/home/kit/polynote/products.json/')
servers = ['35.208.65.122:9092', '34.68.16.1:9092', '35.225.151.65:9092']
#servers = ['localhost:9092']
producer = KafkaProducer(bootstrap_servers=servers)

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    print('I am an errback', exc_info=excp)

def signal_handler(sig, frame):
    print('Shutting down, please wait...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Sending data')

for filename in list(p.glob('*.json')):
    if os.path.isfile("processed_files.txt"):
        with open("processed_files.txt", "r") as fin:
            if filename in fin:
                continue

    print("Working on %s" % (filename))
    with open(filename, 'r') as fin:
        for line in fin:
            data = line.encode('utf-8')
            producer.send('reviews', key=None, value=data).add_callback(on_send_success).add_errback(on_send_error)
            time.sleep(1)

    with open("processed_files.txt", "a") as fin:
        fin.write(filename + "\n")

# block until all async messages are sent
producer.flush()