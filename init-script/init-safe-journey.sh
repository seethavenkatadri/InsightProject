# Kafka

# Refresh topics
cd $KAFKA_HOME/bin
./kafka-topics.sh --zookeeper localhost:2181 --delete --topic topic-flight
./kafka-topics.sh --zookeeper localhost:2181 --delete --topic topic-weather
./kafka-topics.sh --zookeeper localhost:2181 --delete --topic topic-flying-conditions
./kafka-topics.sh --zookeeper localhost:2181 --delete --topic topic-latest-weather
./kafka-topics.sh --zookeeper localhost:2181 --create --topic topic-flight --replication-factor 3 --partitions 16
./kafka-topics.sh --zookeeper localhost:2181 --create --topic topic-weather --replication-factor 3 --partitions 16
./kafka-topics.sh --zookeeper localhost:2181 --create --topic topic-flying-conditions --replication-factor 3 --partitions 16
./kafka-topics.sh --zookeeper localhost:2181 --create --topic topic-latest-weather --replication-factor 3 --partitions 16
./kafka-streams-application-reset.sh --application-id stream-processor
cd $HOME



#Kafka Streams
# Refresh and Execution Script

rm -rf InsightProject
git clone https://github.com/seethavenkatadri/InsightProject.git
cd InsightProject/data-processing/stream-processing
mvn compile
mvn clean package
mvn exec:java -Dexec.mainClass=StreamProcessor



# Postgres

# Refresh Script

rm -rf InsightProject
git clone https://github.com/seethavenkatadri/InsightProject.git

# Execution Script
# Run 1 - topic-flying-conditions
# Run 2 - topic-latest-weather

cd InsightProject/database-scripts
python3 kafka-postgres-connect.py $1
cd $HOME


# Flask
# Refresh and Execution Script

rm -rf InsightProject
git clone https://github.com/seethavenkatadri/InsightProject.git
cd InsightProject/app
nohup python3 app.py &
cd $HOME

# Kafka

# Start Streaming
# Run 1 - seetha-weather-data topic-weather
# Run 2 - seetha-flight-live topic-flight

cd $HOME
rm -rf InsightProject
git clone https://github.com/seethavenkatadri/InsightProject.git
cd InsightProject/ingestion
python3 streaming.py $1 $2


