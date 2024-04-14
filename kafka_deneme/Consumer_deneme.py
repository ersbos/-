from kafka import KafkaConsumer

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Define the topic from which you want to consume messages
topic = 'test-topic'

# Create a KafkaConsumer instance
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)

try:
    # Start consuming messages
    for message in consumer:
        print(f"Received: {message.value.decode('utf-8')}")
except KeyboardInterrupt:
    # Handle keyboard interrupt
    consumer.close()
