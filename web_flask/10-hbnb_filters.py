#!/usr/bin/python3
"""
Starts a  flask web application
socket: 0.0.0.0:5000
"""
from flask import Flask, escape, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from os import getenv
app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception=None):
    """removes current SQLAlchemy session"""
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """States' cities list"""
    states = storage.all(State).items()
    amenities = storage.all(Amenity).items()
    if getenv('HBNB_TYPE_STORAGE') == "db":
        if states:
            states = {state.name: [city.name for city in state.cities]
                      for _, state in states}
        if amenities:
            amenities = [amenity.name for _, amenity in amenities]
    else:
        if states:
            states = {state.name: [city.name for city in state.cities()]
                      for _, state in states}
        if amenities:
            amenities = [amenity.name for _, amenity in amenities]
    return render_template("10-hbnb_filters.html",
                           states=states,
                           amenities=amenities)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
