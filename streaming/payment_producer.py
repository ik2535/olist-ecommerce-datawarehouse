from kafka import KafkaProducer
import json
import time
import pandas as pd

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

df = pd.read_csv('/app/streaming/order_payments_stream.csv')  # Mount this path in Docker

for _, row in df.iterrows():
    producer.send('order_payments', row.to_dict())
    print(f"✅ Sent: {row.to_dict()}")
    time.sleep(1)  # Simulate streaming delay
