while (true)
do
filename=states-`date '+%Y-%m-%d_%H:%M:%S'`.json
curl -s "https://opensky-network.org/api/states/all" | python -m json.tool > $filename
aws s3 cp $filename s3://seetha-flight-live
rm $filename
sleep 6
done

