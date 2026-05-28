from kafka import KafkaProducer
import json, time
import os

producer = KafkaProducer(
  bootstrap_servers=os.getenv("BOOTSTRAP", "kafka:9092"),
  value_serializer=lambda v: json.dumps(v).encode()
)

i = 0

while True:
  producer.send("demo-events", {"counter": i})
  producer.flush()
  print(f"sent {i}")
  i += 1
  time.sleep(2)
