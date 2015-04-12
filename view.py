# third party modules
from flask import (Flask, render_template, request)

# project modules
import config
from logic import Database

# instanciate application and database object
app = Flask(__name__)
db = Database(config)

# configure the web abb according to the config object
app.host = config.APP_HOST
app.port = config.APP_PORT
app.debug = config.APP_DEBUG


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
