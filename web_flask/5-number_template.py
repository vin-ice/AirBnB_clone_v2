#!/usr/bin/python3
"""
Starts a  flask web application
socket: 0.0.0.0:5000
"""
from flask import Flask, escape, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """
    Root location
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """hbnb location"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """Prints text from the url"""
    return "C {}".format(escape(text)).replace('_', ' ')


@app.route("/python/", defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_text(text):
    """Prints text from url"""
    return "Python {}".format(escape(text)).replace("_", " ")


@app.route("/number/<int:n>", strict_slashes=False)
def print_num(n):
    """
    Prints integer
    args:
        n (int): possible int
    """
    return "{}".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def printn_template(n):
    """
    Prints template if n is a number
    args:
        n (int): possible int
    """
    return render_template(template_name_or_list="5-number.html",
                           n=n)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
