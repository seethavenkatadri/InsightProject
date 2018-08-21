from flask import Flask
from flask import render_template
import psycopg2
from configparser import ConfigParser
import geojson
from collections import OrderedDict


def config(filename='database-fe.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def fetch_flights(limit):
    """ select flight records for display """
    sql = "select flight_id AS flight,info ->> 'latitude' as latitude, info ->> 'longitude' as longitude  from flight order by create_date desc limit %s;"
    conn = None
    state_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (limit,))
        r = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return r
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def fetch_weather(limit):
    """ select flight records for display """
    sql = "select station_id AS station, info ->> 'Latitude' as latitude, info ->> 'Longitude' as longitude, info ->> 'Mean_Visibility' as visibility, info ->> 'Mean_Windspeed' as windspeed, info ->> 'Precipitation' as precipitation  from weather order by create_date desc limit %s;"
    conn = None
    state_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (limit,))
        r = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return r
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_flight_results(limit):
    results = fetch_flights(limit)
    flightFeatureList=[]
    for record in results:
        myPoint=geojson.Point((float(record['latitude']),float(record['longitude'])))
        flightFeatureList.append(geojson.Feature(geometry=myPoint, properties={"id" : record['flight']}))
    return flightFeatureList

def get_weather_results(limit):
    results = fetch_weather(limit)
    weatherFeatureList = []
    weatherDataList = []
    for record in results:
        myPoint = geojson.Point((float(record['latitude']), float(record['longitude'])))
        weatherFeatureList.append(geojson.Feature(geometry=myPoint))
        weatherDataList.append(OrderedDict(record['station'],record['visibility'],record['windspeed'],record['precipitation']))
    return weatherFeatureList, weatherDataList

app = Flask(__name__,static_url_path='/static')
app.config['DEBUG'] = True
#flight_results=get_flight_results(30)
weather_points, weather_results=get_weather_results(30)
#weather_points=[{"geometry": {"coordinates": [37.452961, -122.181725], "type": "Point"}, "properties": {"vis": "2.2", "ws": "15.5"}, "type": "Feature"},{"geometry": {"coordinates": [53.617, 0.15], "type": "Point"}, "properties": {"vis": "2.2", "ws": "15.5"}, "type": "Feature"}, {"geometry": {"coordinates": [53.03, -0.483], "type": "Point"}, "properties": {"vis": "2.2", "ws": "14.3"}, "type": "Feature"}, {"geometry": {"coordinates": [53.317, -4.617], "type": "Point"}, "properties": {"vis": "12.4", "ws": "23.9"}, "type": "Feature"}, {"geometry": {"coordinates": [55.017, -1.417], "type": "Point"}, "properties": {"vis": "5.2", "ws": "8.2"}, "type": "Feature"}, {"geometry": {"coordinates": [56.033, -3.133], "type": "Point"}, "properties": {"vis": "9.3", "ws": "12.0"}, "type": "Feature"}, {"geometry": {"coordinates": [57.202, -2.198], "type": "Point"}, "properties": {"vis": "10.9", "ws": "11.0"}, "type": "Feature"}, {"geometry": {"coordinates": [60.133, -1.183], "type": "Point"}, "properties": {"vis": "12.4", "ws": "4.8"}, "type": "Feature"}, {"geometry": {"coordinates": [53.617, 0.15], "type": "Point"}, "properties": {"vis": "2.2", "ws": "15.5"}, "type": "Feature"}, {"geometry": {"coordinates": [53.03, -0.483], "type": "Point"}, "properties": {"vis": "2.2", "ws": "14.3"}, "type": "Feature"}, {"geometry": {"coordinates": [53.317, -4.617], "type": "Point"}, "properties": {"vis": "12.4", "ws": "23.9"}, "type": "Feature"}, {"geometry": {"coordinates": [55.017, -1.417], "type": "Point"}, "properties": {"vis": "5.2", "ws": "8.2"}, "type": "Feature"}, {"geometry": {"coordinates": [56.033, -3.133], "type": "Point"}, "properties": {"vis": "9.3", "ws": "12.0"}, "type": "Feature"}, {"geometry": {"coordinates": [57.202, -2.198], "type": "Point"}, "properties": {"vis": "10.9", "ws": "11.0"}, "type": "Feature"}, {"geometry": {"coordinates": [60.133, -1.183], "type": "Point"}, "properties": {"vis": "12.4", "ws": "4.8"}, "type": "Feature"}]
flight_results=[{"geometry": {"coordinates": [41.3404, -92.6115], "type": "Point"}, "properties": {"id": "ac70da"}, "type": "Feature"}, {"geometry": {"coordinates": [-23.4769, -46.6516], "type": "Point"}, "properties": {"id": "e4924a"}, "type": "Feature"}, {"geometry": {"coordinates": [21.7857, -157.6903], "type": "Point"}, "properties": {"id": "a19a21"}, "type": "Feature"}, {"geometry": {"coordinates": [0.0, 0.0], "type": "Point"}, "properties": {"id": "a94bff"}, "type": "Feature"}, {"geometry": {"coordinates": [38.9465, -77.449], "type": "Point"}, "properties": {"id": "a94bfc"}, "type": "Feature"}, {"geometry": {"coordinates": [39.8963, -83.1046], "type": "Point"}, "properties": {"id": "a7c584"}, "type": "Feature"}, {"geometry": {"coordinates": [43.8781, -87.8252], "type": "Point"}, "properties": {"id": "a0dd1e"}, "type": "Feature"}, {"geometry": {"coordinates": [38.2597, -119.4497], "type": "Point"}, "properties": {"id": "a1adab"}, "type": "Feature"}, {"geometry": {"coordinates": [37.0687, -89.5422], "type": "Point"}, "properties": {"id": "a0f73c"}, "type": "Feature"}, {"geometry": {"coordinates": [-23.5728, -46.6939], "type": "Point"}, "properties": {"id": "e48b64"}, "type": "Feature"}, {"geometry": {"coordinates": [36.0912, -115.1641], "type": "Point"}, "properties": {"id": "a22419"}, "type": "Feature"}, {"geometry": {"coordinates": [33.4187, -80.3274], "type": "Point"}, "properties": {"id": "ad3c6b"}, "type": "Feature"}, {"geometry": {"coordinates": [15.2737, 121.0229], "type": "Point"}, "properties": {"id": "75841b"}, "type": "Feature"}, {"geometry": {"coordinates": [-2.562, 104.5212], "type": "Point"}, "properties": {"id": "8a0311"}, "type": "Feature"}, {"geometry": {"coordinates": [49.0452, -123.039], "type": "Point"}, "properties": {"id": "3c4ad3"}, "type": "Feature"}, {"geometry": {"coordinates": [49.0269, -63.0586], "type": "Point"}, "properties": {"id": "3c4ad4"}, "type": "Feature"}, {"geometry": {"coordinates": [-38.1281, 176.3041], "type": "Point"}, "properties": {"id": "c8237a"}, "type": "Feature"}, {"geometry": {"coordinates": [0.0, 0.0], "type": "Point"}, "properties": {"id": "31828e"}, "type": "Feature"}, {"geometry": {"coordinates": [32.6417, -85.7009], "type": "Point"}, "properties": {"id": "a52e54"}, "type": "Feature"}, {"geometry": {"coordinates": [31.2301, -95.9917], "type": "Point"}, "properties": {"id": "abb579"}, "type": "Feature"}, {"geometry": {"coordinates": [40.686, -74.1812], "type": "Point"}, "properties": {"id": "a41596"}, "type": "Feature"}, {"geometry": {"coordinates": [38.7921, -80.3643], "type": "Point"}, "properties": {"id": "a65527"}, "type": "Feature"}, {"geometry": {"coordinates": [48.185, -58.6535], "type": "Point"}, "properties": {"id": "3c64f6"}, "type": "Feature"}, {"geometry": {"coordinates": [60.3009, 33.0352], "type": "Point"}, "properties": {"id": "3c4ad8"}, "type": "Feature"}, {"geometry": {"coordinates": [14.5797, 121.5244], "type": "Point"}, "properties": {"id": "758426"}, "type": "Feature"}, {"geometry": {"coordinates": [40.4735, -104.3367], "type": "Point"}, "properties": {"id": "3c4ad9"}, "type": "Feature"}, {"geometry": {"coordinates": [38.7107, -90.2912], "type": "Point"}, "properties": {"id": "abb54f"}, "type": "Feature"}, {"geometry": {"coordinates": [59.6518, 29.1423], "type": "Point"}, "properties": {"id": "4249cc"}, "type": "Feature"}, {"geometry": {"coordinates": [-26.2554, 152.2972], "type": "Point"}, "properties": {"id": "7c6aea"}, "type": "Feature"}, {"geometry": {"coordinates": [35.91, 139.887], "type": "Point"}, "properties": {"id": "86d6c8"}, "type": "Feature"}]
#weather_results=[{'windspeed': '15.5', 'visibility': '2.2', 'latitude': '53.617', 'precipitation': '0.00', 'station': '03396099999', 'longitude': '0.15'}, {'windspeed': '14.3', 'visibility': '2.2', 'latitude': '53.03', 'precipitation': '0.00', 'station': '03379099999', 'longitude': '-0.483'}, {'windspeed': '23.9', 'visibility': '12.4', 'latitude': '53.317', 'precipitation': '0.00', 'station': '03311099999', 'longitude': '-4.617'}, {'windspeed': '8.2', 'visibility': '5.2', 'latitude': '55.017', 'precipitation': '0.00', 'station': '03262099999', 'longitude': '-1.417'}, {'windspeed': '12.0', 'visibility': '9.3', 'latitude': '56.033', 'precipitation': '0.00', 'station': '03159099999', 'longitude': '-3.133'}, {'windspeed': '11.0', 'visibility': '10.9', 'latitude': '57.202', 'precipitation': '0.00', 'station': '03091099999', 'longitude': '-2.198'}, {'windspeed': '4.8', 'visibility': '12.4', 'latitude': '60.133', 'precipitation': '0.00', 'station': '03005099999', 'longitude': '-1.183'}, {'windspeed': '15.5', 'visibility': '2.2', 'latitude': '53.617', 'precipitation': '0.00', 'station': '03396099999', 'longitude': '0.15'}, {'windspeed': '14.3', 'visibility': '2.2', 'latitude': '53.03', 'precipitation': '0.00', 'station': '03379099999', 'longitude': '-0.483'}, {'windspeed': '23.9', 'visibility': '12.4', 'latitude': '53.317', 'precipitation': '0.00', 'station': '03311099999', 'longitude': '-4.617'}, {'windspeed': '8.2', 'visibility': '5.2', 'latitude': '55.017', 'precipitation': '0.00', 'station': '03262099999', 'longitude': '-1.417'}, {'windspeed': '12.0', 'visibility': '9.3', 'latitude': '56.033', 'precipitation': '0.00', 'station': '03159099999', 'longitude': '-3.133'}, {'windspeed': '11.0', 'visibility': '10.9', 'latitude': '57.202', 'precipitation': '0.00', 'station': '03091099999', 'longitude': '-2.198'}, {'windspeed': '4.8', 'visibility': '12.4', 'latitude': '60.133', 'precipitation': '0.00', 'station': '03005099999', 'longitude': '-1.183'}]
@app.route('/')
def main():
    print(flight_results)
    print(weather_points)
    print(weather_results)
    return render_template('airtravel.html',flights=flight_results, weatherpoints=weather_points, weatherdata=weather_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')