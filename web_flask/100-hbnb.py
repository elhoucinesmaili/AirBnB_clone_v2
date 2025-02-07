#!/usr/bin/python3
"""
A script that starts a Flask web application
listening on 0.0.0.0, port 5000
"""
from flask import Flask, render_template
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """Function to remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Function that displays HBNB web page"""
    st = storage.all(State).values()
    st = sorted(st, key=lambda k: k.name)
    sc = []

    for state in st:
        sc.append([state, sorted(state.cities, key=lambda k: k.name)])

    am = storage.all(Amenity).values()
    am = sorted(am, key=lambda k: k.name)

    pl = storage.all(Place).values()
    pl = sorted(pl, key=lambda k: k.name)

    return render_template('100-hbnb.html', states=sc, amenities=am, places=pl)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
