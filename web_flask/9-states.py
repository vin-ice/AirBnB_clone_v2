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


@app.route("/states", strict_slashes=False)
def states_list():
    """Displays States List"""
    states = storage.all(State).items()
    teardown_session()
    if states:
        states = ["{}.{}".format(v.name, v.id) for _, v in states]
    return render_template("9-states.html", states=states)


@app.route("/states/<id>", strict_slashes=False)
def cities_list(id):
    """States' cities list"""
    states, state, cities = storage.all(State).items(), None, None
    if states:
        for _, v in states:
            if v.id == id:
                state = v.name
                if getenv('HBNB_TYPE_STORAGE') == "db":
                    cities = ["{}.{}".format(c.name, c.id) for c in v.cities]
                else:
                    cities = ["{}.{}".format(c.name, c.id) for c in v.cities()]
                break
    teardown_session()
    return render_template("9-states.html", state=state, cities=cities)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
