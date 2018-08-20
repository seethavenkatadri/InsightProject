import confluent_kafka
import boto3
import csv
import codecs
import json
import sys
from datetime import datetime

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

def assign_defaults(dict):
    "Function to set default inputs for latitude and longitude"
    if dict["latitude"] == "":
        dict["latitude"] = '0.0'
    if dict["longitude"] == "":
        dict["longitude"] = '0.0'
    return dict


def publish_message(producerInstance, topic_name, key, value):
    "Function to send messages to the specific topic"
    try:
        producerInstance.produce(topic_name,key=key,value=value)
        producerInstance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    "Function to create a producer handle"
    _producer = None
    conf = {'bootstrap.servers': 'ec2-35-160-138-85.us-west-2.compute.amazonaws.com:9092,ec2-34-218-19-12.us-west-2.compute.amazonaws.com:9092,ec2-54-148-69-162.us-west-2.compute.amazonaws.com:9092,ec2-54-149-61-226.us-west-2.compute.amazonaws.com:9092'}
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
     "position_source","inputTime"]
    weather_record=["ID","USAF","WBAN","Elevation","Country_Code","Latitude","Longitude","Date","Year","Month","Day","Mean_Temp","Mean_Temp_Count","Mean_Dewpoint",
                    "Mean_Dewpoint_Count","Mean_Sea_Level_Pressure","Mean_Sea_Level_Pressure_Count","Mean_Station_Pressure","Mean_Station_Pressure_Count",
                    "Mean_Visibility","Mean_Visibility_Count","Mean_Windspeed","Mean_Windspeed_Count","Max_Windspeed","Max_Gust","Max_Temp","Max_Temp_Quality_Flag",
                    "Min_Temp","Min_Temp_Quality_Flag","Precipitation","Precip_Flag","Snow_Depth","Fog","Rain_or_Drizzle","Snow_or_Ice","Hail","Thunder","Tornado",
                    "inputTime"]

    ############   Main Function   ###############
    bucketName = sys.argv[1]
    topicName = sys.argv[2]
    myBucket=get_bucket_details(bucketName)

   # reading one file as of now
    fileHandleList=get_all_bucket_files(myBucket)
    kafkaProducer=connect_kafka_producer()

    #for file in fileHandleList:
    for file in fileHandleList:
        skip_header=0
        for record in codecs.getreader('utf-8')(file.get()[u'Body']):
            if skip_header == 0 and topicName == 'topic-weather':
                skip_header += 1
                continue
            arr=record.strip().split(',')
            if topicName == 'topic-flight':
                tempDict = dict({flight_record[i]:arr[i] for i in range(len(arr) - 1)})
                resultDict = assign_defaults(tempDict)
            else:
                resultDict = dict({weather_record[i]: arr[i] for i in range(len(arr) - 1)})
            resultDict["inputTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


            print(resultDict)
            #### because both the arrays have their first element as keys icao24 and ID
            publish_message(kafkaProducer, topicName,arr[0], json.dumps(resultDict))


            num_records+=1
            if num_records == 10:
                break
        num_files+=1
        if num_files == 5:
            break


