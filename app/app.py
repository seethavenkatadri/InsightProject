from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['DEBUG'] = True
POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'DB_MAIN_SCHEMA',
    'host': 'ec2-54-203-148-178.us-west-2.compute.amazonaws.com',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES



@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()