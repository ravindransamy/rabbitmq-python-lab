\# RabbitMQ Python Lab



A hands-on RabbitMQ learning project using Python, Pika, Docker Compose, and RabbitMQ Management UI.



This project demonstrates how a Python producer sends messages to RabbitMQ and how one or more Python consumers receive and process those messages.



\## Architecture



```text

&#x20;                ┌──────────────────────┐

&#x20;                │    Python Producer    │

&#x20;                │     producer.py      │

&#x20;                └──────────┬───────────┘

&#x20;                           │

&#x20;                           │ Publish

&#x20;                           ▼

&#x20;                ┌──────────────────────┐

&#x20;                │   RabbitMQ Exchange  │

&#x20;                │   training.direct    │

&#x20;                │       (direct)       │

&#x20;                └──────────┬───────────┘

&#x20;                           │

&#x20;                    Routing Key:

&#x20;                    training

&#x20;                           │

&#x20;                           ▼

&#x20;                ┌──────────────────────┐

&#x20;                │    training.queue    │

&#x20;                │    RabbitMQ Queue    │

&#x20;                └──────────┬───────────┘

&#x20;                           │

&#x20;                           │ Consume

&#x20;                           ▼

&#x20;                ┌──────────────────────┐

&#x20;                │    Python Consumer   │

&#x20;                │     consumer.py      │

&#x20;                └──────────────────────┘

```



\## Technologies



\* RabbitMQ 4.x

\* Python 3

\* Pika

\* Docker

\* Docker Compose

\* RabbitMQ Management UI

\* Git / GitHub



\## Project Structure



```text

rabbitmq-python-lab/

│

├── producer.py

├── consumer.py

├── docker-compose.yml

├── requirements.txt

├── .gitignore

├── .env                 # Local only - not committed

└── README.md

```



\## RabbitMQ Configuration



The lab uses:



| Component     | Value           |

| ------------- | --------------- |

| RabbitMQ Host | 192.168.17.248  |

| AMQP Port     | 5672            |

| Management UI | 15672           |

| Virtual Host  | /               |

| Exchange      | training.direct |

| Exchange Type | direct          |

| Queue         | training.queue  |

| Routing Key   | training        |



\## Environment Variables



RabbitMQ credentials are not stored directly in the Python source code or Docker Compose configuration.



Create a local `.env` file:



```env

RABBITMQ\_PASSWORD=your-password

```



The `.env` file is excluded from Git using `.gitignore`.



Never commit real passwords, API keys, tokens, or other secrets to GitHub.



\## Install Python Dependency



Install the required Python package:



```cmd

pip install -r requirements.txt

```



Or:



```cmd

pip install pika

```



\## Start RabbitMQ with Docker Compose



Start the RabbitMQ container:



```cmd

docker compose up -d

```



Check the container:



```cmd

docker ps

```



View logs:



```cmd

docker compose logs -f

```



\## RabbitMQ Management UI



Open:



```text

http://localhost:15672

```



or use the IP address of the RabbitMQ server:



```text

http://192.168.17.248:15672

```



The Management UI can be used to monitor:



\* Connections

\* Channels

\* Exchanges

\* Queues

\* Message rates

\* Ready messages

\* Unacknowledged messages



\## Run the Producer



Open Command Prompt:



```cmd

cd /d G:\\rabbitMQ

python producer.py

```



The producer sends messages to RabbitMQ:



```text

Message 1

Message 2

Message 3

...

Message 10

```



Example:



```text

Sent: Message 1

Sent: Message 2

Sent: Message 3

...

Sent: Message 10

```



\## Run the Consumer



Open another Command Prompt:



```cmd

cd /d G:\\rabbitMQ

python consumer.py

```



The consumer receives and processes messages.



Example:



```text

Received: Message 1

Processing...

Finished processing



Received: Message 2

Processing...

Finished processing

```



\## Message Acknowledgement



The consumer uses manual acknowledgement.



After successful processing:



```python

ch.basic\_ack(

&#x20;   delivery\_tag=method.delivery\_tag

)

```



This tells RabbitMQ:



> The message was successfully processed. Remove it from the queue.



If the consumer fails before acknowledging the message, RabbitMQ can redeliver the message depending on the configuration.



\## Negative Acknowledgement and Requeue



The lab also demonstrates message failure using `basic\_nack()`.



Example:



```python

ch.basic\_nack(

&#x20;   delivery\_tag=method.delivery\_tag,

&#x20;   requeue=True

)

```



When `requeue=True` is used, RabbitMQ puts the message back into the queue.



For example, if `Message 5` fails:



```text

Received: Message 5

ERROR: Message processing failed!



Received: Message 5

ERROR: Message processing failed!



Received: Message 5

ERROR: Message processing failed!

```



This demonstrates an important RabbitMQ concept:



> A message that continuously fails and is requeued can create a retry loop.



\## Prefetch



The consumer uses:



```python

channel.basic\_qos(prefetch\_count=1)

```



This limits the consumer to one unacknowledged message at a time.



Conceptually:



```text

RabbitMQ Queue

&#x20;     │

&#x20;     ▼

Message 1 ──► Consumer

&#x20;              │

&#x20;              │ Processing

&#x20;              ▼

&#x20;            ACK

&#x20;              │

&#x20;              ▼

Message 2 ──► Consumer

```



This is useful when processing tasks that should not be delivered to the consumer faster than it can handle them.



\## Important RabbitMQ Concepts Learned



\### Producer



Creates and publishes messages.



```text

Producer → Exchange

```



\### Exchange



Receives messages from producers and routes them to queues.



```text

Exchange → Queue

```



\### Queue



Stores messages until a consumer processes them.



```text

Queue → Consumer

```



\### Consumer



Receives and processes messages.



```text

Consumer → ACK

```



\### Routing Key



Used by an exchange to determine where a message should be routed.



\### ACK



Confirms successful message processing.



\### NACK



Indicates that message processing failed.



\### Requeue



Places a failed message back into the queue.



\### Prefetch



Controls how many unacknowledged messages can be delivered to a consumer.



\## Troubleshooting



\### Authentication Error



If you receive:



```text

ACCESS\_REFUSED - Login was refused using authentication mechanism PLAIN

```



check:



\* RabbitMQ username

\* RabbitMQ password

\* RabbitMQ host

\* RabbitMQ port

\* Virtual host permissions



\### Connection Error



If you receive:



```text

pika.exceptions.AMQPConnectionError

```



check connectivity:



```cmd

ping 192.168.17.248

```



Check RabbitMQ AMQP port:



```powershell

Test-NetConnection 192.168.17.248 -Port 5672

```



\### Message Repeating Continuously



If a message repeatedly appears:



```text

Received: Message 5

ERROR: Message processing failed!

```



check whether the consumer is using:



```python

basic\_nack(..., requeue=True)

```



The message will continue to be redelivered until it is successfully acknowledged, rejected without requeue, or otherwise handled.



\## Security



Do not commit sensitive information to GitHub.



The following files should never contain real production credentials:



\* `producer.py`

\* `consumer.py`

\* `docker-compose.yml`

\* `README.md`



Use environment variables for credentials.



The `.env` file is intentionally excluded using `.gitignore`.



\## Future Improvements



Planned RabbitMQ learning topics:



\* Dead Letter Exchange (DLX)

\* Dead Letter Queue (DLQ)

\* Retry mechanisms

\* Message TTL

\* Multiple consumers

\* Load balancing between consumers

\* Durable queues and persistent messages

\* Publisher confirms

\* Exchange types



&#x20; \* Direct

&#x20; \* Fanout

&#x20; \* Topic

&#x20; \* Headers

\* RabbitMQ monitoring

\* RabbitMQ authentication and permissions

\* Dockerized Python producer and consumer

\* RabbitMQ clustering

\* High Availability

\* Prometheus and Grafana monitoring



\## Learning Objective



This project is part of a hands-on DevOps learning journey focused on understanding message brokers and asynchronous application architecture using RabbitMQ and Python.



\---



\## Author



Ravindran Karypusamy



GitHub:



https://github.com/ravindransamy



