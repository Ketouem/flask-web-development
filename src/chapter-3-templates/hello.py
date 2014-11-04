# By default Flask looks for templates in a templates subfolder located inside
# the app folder
from flask import Flask, render_template
# Wraps Twitter bootstrap to use them inside templates
from flask.ext.bootstrap import Bootstrap
# Wraps moment.js, a JS library to handle dates and times. Depends on jquery.js
# already available through bootstrap
from flask.ext.moment import Moment

from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# Custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
