from kafka import KafkaProducer
from kafka.errors import KafkaError
from faker import Faker
import json
import signal
import sys
import time

producer = KafkaProducer(bootstrap_servers=['35.208.65.122:9092', '34.68.16.1:9092', '35.225.151.65:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))

def on_send_success(record_metadata):

    print("Sending key=%s, data=%s" % (customer_id, data))
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    print('I am an errback', exc_info=excp)


fake = Faker()

def signal_handler(sig, frame):
    print('Shutting down, please wait...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Sending data')

while True:
    random_int = fake.random_int(0, 100)
    random_name = fake.name()
    customer_id = str(fake.random_int(0, 10))
    # produce asynchronously with callbacks
    data = {'random-name': random_name, 'random-int': random_int}
    print("Sending key=%s, data=%s" % (customer_id, data))
    producer.send('test', data, str.encode(customer_id)).add_callback(on_send_success).add_errback(on_send_error)
    time.sleep(.25)

# block until all async messages are sent
producer.flush()