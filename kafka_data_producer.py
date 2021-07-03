import json
import time
from faker import Faker
from bson import json_util
from kafka import KafkaProducer
from datetime import datetime

BOOTSTRAP_SERVER = "localhost:29092"
TOPIC_NAME = "data_pengguna"
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
fake = Faker('id_ID')

while True:
    my_dict = {"nama": fake.name(), "tanggal_lahir": fake.date("%Y-%m-%d"), "alamat": fake.address()}
    producer.send(TOPIC_NAME, json.dumps(my_dict, default=json_util.default).encode("utf-8"))
    print(my_dict)
    time.sleep(5)