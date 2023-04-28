#!/usr/bin/python3
"""
Starts a  flask web application
socket: 0.0.0.0:5000
"""
from flask import Flask, escape, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User
from os import getenv
app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception=None):
    """removes current SQLAlchemy session"""
    storage.close()


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """States' cities list"""
    states = storage.all(State).items()
    amenities = storage.all(Amenity).items()
    places = storage.all(Place).values()
    if getenv('HBNB_TYPE_STORAGE') == "db":
        if states:
            states = {state.name: [city.name for city in state.cities]
                      for _, state in states}
        if amenities:
            amenities = [amenity.name for _, amenity in amenities]
        if places:
            places = list(places)
            p = {}
            for place in places:
                place = place.to_dict()
                p_dict, owner = {}, {}
                for k, v in place.items():
                    if k == "user_id":
                        users = storage.all(User).items()
                        if users:
                            for _, user in users:
                                if user.id == v:
                                    owner["first_name"] = user.first_name
                                    owner["last_name"] = user.last_name
                                    p_dict["owner"] = owner
                                continue
                        continue
                    p_dict[k] = v
                p[place['name']] = p_dict
            places = p
    else:
        if states:
            states = {state.name: [city.name for city in state.cities()]
                        for _, state in states}
        if amenities:
            amenities = [amenity.name for _, amenity in amenities]
        if places:
            places = list(places)
            p = {}
            for place in places:
                place = place.to_dict()
                p_dict, owner = {}, {}
                for k, v in place.items():
                    if k == "user_id":
                        users = storage.all(User).items()
                        if users:
                            for _, user in users:
                                if user.id == v:
                                    owner["first_name"] = user.first_name
                                    owner["last_name"] = user.last_name
                                    p_dict["owner"] = owner
                                continue
                        continue
                    p_dict[k] = v
                p[place['name']] = p_dict
            places = p
    return render_template("100-hbnb.html", states=states,
                           amenities=amenities,
                           places=places)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
