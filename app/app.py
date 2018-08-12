from flask import Flask
from flask import render_template

app = Flask(__name__,static_url_path='/static')
app.config['DEBUG'] = True


@app.route('/')
def main():
    return render_template('airtravel.html')

if __name__ == '__main__':
    app.run()