import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def index():
    return (
        f"Hawaii Temperatures<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all measures
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_measures = []
    for date, prcp in results:
        measure_dict = {}
        measure_dict["date"] = date
        measure_dict["prcp"] = prcp
        all_measures.append(measure_dict)

    return jsonify(all_measures)


@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)

    # Query all measures
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Query all measures
    results = session.query(Measurement.date, Measurement.tobs, Station.station).all()

    session.close()
    last_year = []
    for station, tobs, date in results:
        if date > '2016-08-22':
            last_year_dict = {}
            last_year_dict["station"] = station
            last_year_dict["tobs"] = tobs
            last_year_dict["date"] = date
            last_year.append(last_year_dict)
    return jsonify(last_year)

@app.route("/api/v1.0/<start>")
def start():
    email = "peleke@example.com"

    return f"Questions? Comments? Complaints? Shoot an email to {email}."

@app.route("/api/v1.0/<start>/<end>")
def startEnd():
    email = "peleke@example.com"

    return f"Questions? Comments? Complaints? Shoot an email to {email}."


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
