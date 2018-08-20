from flask import Flask
from flask import render_template
import psycopg2
from configparser import ConfigParser
import geojson


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

def fetch(limit):
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

def get_results(limit):
    results = fetch(limit)
    featureList=[]
    for record in results:
        flightId=record['flight']
        myPoint=geojson.Point((float(record['latitude']),float(record['longitude'])))
        featureList.append(geojson.Feature(geometry=myPoint,id=flightId))
    return featureList

app = Flask(__name__,static_url_path='/static')
app.config['DEBUG'] = True
results=get_results(30)

@app.route('/')
def main():
    return render_template('airtravel.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',name=results)