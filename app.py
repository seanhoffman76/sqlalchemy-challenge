import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    """Return a list of all precipitation values by date (8-23-2016 to 8-23-2017)"""
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_prior).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_rain
    all_rain = []
    for date, prcp in results:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        all_rain.append(rain_dict)

    return jsonify(all_rain)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation values by date (8-23-2016 to 8-23-2017)"""
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_rain
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        stat_dict = {}
        stat_dict["station"] = station
        stat_dict["name"] = name
        stat_dict["latitude"] = latitude
        stat_dict["longitude"] = longitude
        stat_dict["elevation"] = elevation
        all_stations.append(stat_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temps():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    """Return a list of all temperature values by date (8-23-2016 to 8-23-2017)"""
    # Convert the query results to a Dictionary using date as the key and tobs as the value.

    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date > year_prior).order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_rain
    all_temps = []
    for station, date, tobs in results:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/start/<start>")
# This function called `calc_temps1` will accept start date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for dates from the start date given through the last date in the dataset

def calc_temps1(start_date):
    """TMIN, TAVG, and TMAX for a single date.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of start_calc
    start_calc = []
    for date, minimum, average, maximum in results:
        start_dict = {}
        start_dict["date"] = date
        start_dict["minimum"] = minimum
        start_dict["average"] = average
        start_dict["maximum"] = maximum
        start_calc.append(start_dict)

    return jsonify(start_calc)

@app.route("/api/v1.0/start/end/<start>/<end>")

# This function called `calc_temps2` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates

def calc_temps2(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)

    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of end_calc
    end_calc = []
    for date, minimum, average, maximum in results:
        end_dict = {}
        end_dict["date"] = date
        end_dict["minimum"] = minimum
        end_dict["average"] = average
        end_dict["maximum"] = maximum
        end_calc.append(end_dict)

    return jsonify(end_calc)



if __name__ == "__main__":
    app.run(debug=True)