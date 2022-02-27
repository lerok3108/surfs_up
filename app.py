#import dependencies
import datetime as dt
import numpy as np

import pandas as pd

#import sqlalchemy 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



engine = create_engine("sqlite:///hawaii.sqlite")

#reflect database into classes
Base=automap_base()
Base.prepare(engine, reflect=True)
Measurement=Base.classes.measurement
Station=Base.classes.station

session=Session(engine)

#set up Flask
app=Flask(__name__)

#Define welcome route
@app.route("/")

#create a welcome function
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br>
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/temp/start/end
    ''')    

#create precipitaion route
@app.route("/api/v1.0/precipitation")

#create precipitation function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
    
#create stations route
@app.route("/api/v1.0/stations")

#create stations function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# create temperature observation route
@app.route("/api/v1.0/tobs")

#create a temperature function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))


    return jsonify(temps=temps)

#create the route for statistical analysis
#provide starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#create start and end function
def stats(start=None, end=None):
    #create a query to select min, average and max temps
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    
    return jsonify(temps)
