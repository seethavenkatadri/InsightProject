import confluent_kafka
import boto3
import csv
import codecs
import json
import sys

def get_file_handle(my_bucket, filename):
    # getting each file handle
    fileHandle = my_bucket.Object(key=filename)
    return fileHandle

def get_bucket_details(bucketName):
    ## getting bucket details
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucketName)
    return my_bucket

def get_all_bucket_files(my_bucket):

    fileHandleList=[]
    ## getting all files in csv folder
    for object in my_bucket.objects.filter(Prefix='sample_data/'):
        fileHandleList.append(get_file_handle(my_bucket, object.key))
    return fileHandleList

def publish_message(producerInstance, topic_name, value):
    "Function to send messages to the specific topic"
    try:
        producerInstance.produce(topic_name,value)
        producerInstance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    "Function to create a producer handle"
    _producer = None
    conf = {'bootstrap.servers': 'ec2-54-203-179-203.us-west-2.compute.amazonaws.com:9092'}
    try:
        _producer = confluent_kafka.Producer(conf)
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

if __name__ == '__main__':

    ##Limited number of records as of now
    num_records=0
    num_files=0
    flight_record=["icao24", "callsign", "origin_country", "time_position", "last_contact", "longitude", "latitude", "geo_altitude",
     "on_ground", "velocity", "true_track", "vertical_rate", "sensors", "baro_altitude", "squawk", "spi",
     "position_source"]
    weather_record=["ID","USAF","WBAN","Elevation","Country_Code","Latitude","Longitude","Date","Year","Month","Day","Mean_Temp","Mean_Temp_Count","Mean_Dewpoint",
                    "Mean_Dewpoint_Count","Mean_Sea_Level_Pressure","Mean_Sea_Level_Pressure_Count","Mean_Station_Pressure","Mean_Station_Pressure_Count",
                    "Mean_Visibility","Mean_Visibility_Count","Mean_Windspeed","Mean_Windspeed_Count","Max_Windspeed","Max_Gust","Max_Temp","Max_Temp_Quality_Flag",
                    "Min_Temp","Min_Temp_Quality_Flag","Precipitation","Precip_Flag	Snow_Depth","Fog","Rain_or_Drizzle","Snow_or_Ice","Hail","Thunder","Tornado"]

    ############   Main Function   ###############
    bucketName = sys.arg[1]
    topicName = sys.argv[2]
    myBucket=get_bucket_details(bucketName)

   # reading one file as of now
    fileHandleList=get_all_bucket_files(myBucket)
    kafkaProducer=connect_kafka_producer()

    #for file in fileHandleList:
    for file in fileHandleList:
        for record in codecs.getreader('utf-8')(file.get()[u'Body']):
            arr=record.strip().split(',')
            if topicName == 'topic-flight':
                resultDict = dict({flight_record[i]:arr[i] for i in range(len(arr))})
            else:
                resultDict = dict({weather_record[i]: arr[i] for i in range(len(arr))})
            print(resultDict)

            publish_message(kafkaProducer, topicName, json.dumps(resultDict))
            num_records+=1
            if num_records == 10:
                break
        num_files+=1
        if num_files == 5:
            break


