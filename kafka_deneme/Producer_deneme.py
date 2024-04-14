from kafka import KafkaProducer
import time

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Create a KafkaProducer instance
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Define the topic to which you want to send messages
topic = 'test-topic'

# Path to the text file
file_path = 'test.txt'

try:
    # Open the text file and read its content line by line
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Iterate over each line in the file
        for line in lines:
            # Send each line as a message to the topic
            producer.send(topic, value=bytes(line, 'utf-8'))
            print(f"Sent: {line.strip()}")
            time.sleep(5)  # Sleep for 5 seconds between sending each line

except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the Kafka producer
    producer.close()
