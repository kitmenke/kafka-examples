from kafka import KafkaProducer
from kafka.errors import KafkaError
from faker import Faker
import json

producer = KafkaProducer(bootstrap_servers=['35.225.183.78:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    print('I am an errback', exc_info=excp)

fake = Faker()
# produce asynchronously with callbacks
producer.send('orders', {'key': 'value'}, b'foo').add_callback(on_send_success).add_errback(on_send_error)

# block until all async messages are sent
producer.flush()