import pika
import time
import os

RABBITMQ_HOST = "192.168.17.244"
RABBITMQ_USER = "admin"
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=5672,
        virtual_host="/",
        credentials=pika.PlainCredentials(
            RABBITMQ_USER,
            RABBITMQ_PASSWORD
        )
    )
)

channel = connection.channel()

queue_name = "training.queue"

channel.queue_declare(
    queue=queue_name,
    durable=True
)

# Only allow 1 unacknowledged message
channel.basic_qos(prefetch_count=1)


def callback(ch, method, properties, body):

    message = body.decode()

    print(f"\nReceived: {message}")

    # Intentionally fail Message 5
    #if message == "Message 5":

    #    print("ERROR: Message processing failed!")

     #   ch.basic_nack(
     #       delivery_tag=method.delivery_tag,
      #      requeue=False
       # )

        #return

    print("Processing...")

    time.sleep(2)

    print("Finished processing")

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


# Register the consumer
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False
)

print("Connected to RabbitMQ")
print("Prefetch = 1")
print("Waiting for messages...")

# Start waiting for messages
channel.start_consuming()