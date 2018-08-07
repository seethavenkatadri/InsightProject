from kafka import KafkaProducer


def publish_message(producer_instance, topic_name, key, value):
    "Function to send messages to the specific topic"
    try:
        producer_instance.send(topic_name, key=key, value=value)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    "Function to create a producer handle"
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['ec2-34-210-24-198.us-west-2.compute.amazonaws.com:9092'])
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

if __name__ == '__main__':

    ############   Main Function   ###############

    input_message_list = ['Hi','more','messages','arriving']
    if len(input_message_list) > 0:
        kafka_producer = connect_kafka_producer()
        for message in input_message_list:
            publish_message(kafka_producer, 'topic-flight', 'raw', message.strip())
        if kafka_producer is not None:
            kafka_producer.close()