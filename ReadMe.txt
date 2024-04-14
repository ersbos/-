MetroPt data üzerine model geliştirme

Kafka Çalıştırma için:
Start zookeeper:
E:/Kafka/kafka_2.12-3.6.0/bin/windows/zookeeper-server-start.bat E:/Kafka/kafka_2.12-3.6.0/config/zookeeper.properties
Start kafka-server:
E:/Kafka/kafka_2.12-3.6.0/bin/windows/kafka-server-start.bat E:/Kafka/kafka_2.12-3.6.0/config/server.properties

Create a topic:
E:/Kafka/kafka_2.12-3.6.0/bin/windows/kafka-topics.bat --create --topic test-topic --bootstrap-server localhost:9092 --replication-factor 1 partitions 1