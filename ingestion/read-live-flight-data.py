import requests
import json
import csv
import datetime
import time as t
import boto3
import os


s3 = boto3.resource('s3')
myBucket = "seetha-flight-live"

while(True):
    r = requests.get('https://seetha:seetha1987@opensky-network.org/api/states/all', auth=('seetha', 'seetha1987'))
    print(r.content)
    json_str = r.content
    json_data = json.loads(json_str)
    time = json_data['time']
    states_list = json_data['states']
    now = (datetime.datetime.now()).strftime("%Y-%m-%d_%H:%M")
    filename='states_'+now+'.csv'
    # open a file for writing
    state_data = open('/Users/seethadixit/'+filename, 'w')

    # create the csv writer object

    csvwriter = csv.writer(state_data)

    count = 0

    for state in states_list:
          if count == 0:
                header = state
                csvwriter.writerow(header)
                count += 1
          csvwriter.writerow(state)
    state_data.close()
    s3.Bucket(myBucket).upload_file('/Users/seethadixit/'+filename, "latest_data/"+filename)
    os.remove('/Users/seethadixit/'+filename)
    t.sleep(5)