import psycopg2
from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
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

def insert_status(sql):
    """ insert a new record into the flying conditions table """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # get the generated id back
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


all_stations=open('/Users/seethadixit/Documents/Insight/Project/random/weather-stations-data.csv','r')
skip_header=0
for record in all_stations:
    if skip_header == 0 :
        skip_header += 1
        continue
    parsed=record.strip().split(',')
    sql = """INSERT INTO WEATHER_STATION(STATIONID,USAF,WBAN,NAME,COUNTRY,STATE,CALL,LOCATION,ELEVATION,BEGINDATE,ENDDATE)
                 VALUES('""" + parsed[0] + parsed[1] + """','""" + parsed[0] + """','""" + parsed[1] + """','""" + \
          parsed[2] + """','""" + parsed[3] + """','""" + parsed[4] + """','""" + parsed[5]  + """',POINT(""" + parsed[6] + """,""" + parsed[7] + """),'""" + parsed[8] + """','""" + parsed[9] + """','""" + parsed[10] + """');"""
    insert_status(sql)
    print()