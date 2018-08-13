import boto3
import csv
import codecs

## getting bucket details
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('seetha-flight-live')

with open('/Users/seethadixit/' + 'states_2018-08-12_18:27.csv', 'w') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow()

## getting all files in csv folder
    for object in my_bucket.objects.filter(Prefix='latest_data/'):
        print(object.key)
        fileHandle = my_bucket.Object(key=object.key)
        fileContent = fileHandle.get()

            # iterating over the lines
        with fileContent[u'Body'] as incsv:
            reader = csv.reader(incsv)
            writer.writerow(row for row in reader)




