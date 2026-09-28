import pika
import os

RABBITMQ_HOST = "192.168.17.244"
RABBITMQ_USER = "admin"
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=5672,
        credentials=pika.PlainCredentials(
            RABBITMQ_USER,
            RABBITMQ_PASSWORD
        )
    )
)

channel = connection.channel()

exchange_name = "training.direct"
routing_key = "training"

for i in range(1, 11):
    message = f"Message {i}"

    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    print(f"Sent: {message}")
channel.basic_publish(
    exchange=exchange_name,
    routing_key=routing_key,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2
    )
)

print("Message sent:")
print(message)

connection.close()