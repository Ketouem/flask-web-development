from flask import Flask
# One of Flask context global
from flask import request
# currrent_app, g -> application context
# request, session -> request context
from flask import make_response
from flask import redirect
from flask import abort

# Flask extension that handles CLI
from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)


@app.route('/')  # Routes stored in app.url_map
def index():
    browser = request.headers.get('User-Agent')
    return '<h1>Hello World! You browser is {}</h1>'.format(browser)


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}</h1>'.format(name), 200  # By default sends back 200


@app.route('/response_inside_cookie')
def response_inside_cookie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


# 302 response, with a Location header
@app.route('/redirect')
def redirect_me():
    return redirect('http://www.google.com')


@app.route('/abort/<int:code>')
def abort_by_code(code):
    # Abort does not return control back to the function that calls it but
    # to the web server by raising an exception.
    abort(code)

if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()  # To run: python hello.py runserver --host 0.0.0.0
