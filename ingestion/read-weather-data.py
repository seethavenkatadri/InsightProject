import boto3
import csv
import codecs

## getting bucket details
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('seetha-weather-data')

## getting all files in csv folder
for object in my_bucket.objects.filter(Prefix='csv/'):

        # getting each file handle
        fileHandle = my_bucket.Object(key=object.key)
        fileContent = fileHandle.get()

        # iterating over the lines
        for row in csv.DictReader(codecs.getreader('utf-8')(fileContent[u'Body'])):
            print(row)



