from kafka import KafkaConsumer
import json
import os

consumer = KafkaConsumer(
  "demo-events",
  bootstrap_servers=os.getenv("BOOTSTRAP", "kafka:9092"),
  value_deserializer=lambda b: json.loads(b.decode()),
  auto_offset_reset="earliest",
  group_id="demo-class"
)

for message in consumer:
  print("received", message.value)
