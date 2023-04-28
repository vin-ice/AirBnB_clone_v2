#!/usr/bin/python3
"""
Starts a  flask web application
socket: 0.0.0.0:5000
"""
from flask import Flask, escape, render_template
from models import storage
from models.state import State
from os import getenv
app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception=None):
    """removes current SQLAlchemy session"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Lists states"""
    states = storage.all(State).items()

    if states:
        states = {v.name: v.id for _, v in states}
    return render_template("7-states_list.html", states=states)


@app.route("/cities_by_states", strict_slashes=False)
def cities_list():
    """Cities list"""
    states = storage.all(State).items()
    if states:
        if getenv('HBNB_TYPE_STORAGE') == "db":
            states = {"{}.{}".format(v.name, v.id):
                      ["{}.{}".format(c.name, c.id) for c in v.cities]
                      for _, v in states}
        else:
            states = {"{}.{}".format(v.name, v.id):
                      ["{}.{}".format(c.name, c.id) for c in v.cities()]
                      for _, v in states}
    return render_template("8-cities_by_states.html", states=states)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
