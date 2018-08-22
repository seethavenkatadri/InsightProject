from flask import Flask
from flask import render_template
import psycopg2
from configparser import ConfigParser
import geojson
from collections import OrderedDict
from threading import Timer, Thread
from time import sleep

class Scheduler(object):
    def __init__(self, sleep_time, function):
        self.sleep_time = sleep_time
        self.function = function
        self._t = None

    def start(self):
        if self._t is None:
            self._t = Timer(self.sleep_time, self._run)
            self._t.start()
        else:
            raise Exception("this timer is already running")

    def _run(self):
        self.function()
        self._t = Timer(self.sleep_time, self._run)
        self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None

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

def fetch_flights():
    """ select flight records for display """
    sql = "select flight_id AS flight,info ->> 'latitude' as latitude, info ->> 'longitude' as longitude, info ->> 'track' as angle  from  flight f where date_trunc('day',f.create_date) = date_trunc('day',current_timestamp) and create_date = (select max(create_date) from flight fi where fi.flight_id = f.flight_id);"
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
        cur.execute(sql)
        r = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return r
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def fetch_weather():
    """ select flight records for display """
    sql = "select station_id AS station, info ->> 'Latitude' as latitude, info ->> 'Longitude' as longitude, info ->> 'Mean_Visibility' as visibility, info ->> 'Mean_Windspeed' as windspeed, info ->> 'Precipitation' as precipitation  from weather w where date_trunc('day',w.create_date) = date_trunc('day',current_timestamp) and create_date = (select max(create_date) from weather wi where wi.station_id = w.station_id);"
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
        cur.execute(sql)
        r = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return r
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_flight_results():
    results = fetch_flights()
    flightFeatureList=[]
    angleList=[]
    for record in results:
        print("flights:",record['latitude'],record['longitude'])
        myPoint=geojson.Point((float(record['latitude']),float(record['longitude'])))
        flightFeatureList.append(geojson.Feature(geometry=myPoint, properties={"id" : record['flight']}))
        angleList.append(record['angle'])
    return flightFeatureList,angleList

def get_weather_results():
    results = fetch_weather()
    tmpDict={}
    weatherFeatureList = []
    weatherDataList = []
    for record in results:
        print("weather:", record['latitude'], record['longitude'])
        myPoint = geojson.Point((float(record['latitude']), float(record['longitude'])))
        weatherFeatureList.append(geojson.Feature(geometry=myPoint))
        tmpDict['station'] = record['station']
        tmpDict['visibility'] = record['visibility']
        tmpDict['windspeed'] = record['windspeed']
        tmpDict['precipitation'] = record['precipitation']
        tmpDict=OrderedDict()

        weatherDataList.append(tmpDict)
    return weatherFeatureList, weatherDataList

def query_db():
    flight_results,angleList = get_flight_results()
    weather_points, weather_results = get_weather_results()
    return flight_results,weather_points,weather_results,angleList

app = Flask(__name__,static_url_path='/static')
app.config['DEBUG'] = True

@app.route('/')
def main():
    flight_results, weather_points, weather_results,angleList = query_db()
    return render_template('airtravel.html', flights=flight_results, angles=angleList,weatherpoints=weather_points,
                    weatherdata=weather_results)


if __name__ == '__main__':
    scheduler = Scheduler(5, query_db)
    scheduler.start()
    app.run(host='0.0.0.0',use_reloader=False)
    scheduler.stop()
