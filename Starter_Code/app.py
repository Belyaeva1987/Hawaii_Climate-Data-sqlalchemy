# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()



# Save references to each table
Measurement = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Climate App API!",
        "routes": {
            "precipitation": "/api/v1.0/prcp",
            "stations": "/api/v1.0/station",
            "temperature observations": "/api/v1.0/tobs",
            "temperature stats": "/api/v1.0/<start_date> and /api/v1.0/<start>/<end>"
        }
    })

# A stations route that:

# Returns jsonified data of all of the stations in the database 
@app.route("/api/v1.0/station")
def get_stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(stations.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify( all_stations)



# A precipitation route that:

# Returns jsonified data of precipitation for the last year in the database 

@app.route('/api/v1.0/prcp')
def get_precipitation():
    session = Session(engine)


    from datetime import datetime, timedelta

# Design a query to retrieve the last 12 months of precipitation data.
# Starting from the most recent data point in the database.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

# Calculate the date one year from the last date in the dataset.
    one_year_ago = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    session.close()

    all_precipitation = {date: prcp for date, prcp in results}

    return jsonify(all_precipitation)



# Temperature observations route that:
# Returns jsonified data of Temperature observations for the last year in the database 

@app.route('/api/v1.0/tobs')
def get_tobs():
    session = Session(engine)


    from datetime import datetime, timedelta

# Design a query to retrieve the last 12 months of tobs data.
# Starting from the most recent data point in the database.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

# Calculate the date one year from the last date in the dataset.
    one_year_ago = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).all()

    session.close()

    all_tobs = {date: tobs for date, tobs in results}

    return jsonify(all_tobs)



# API Dynamic Route 

# A start route that:
# Accepts the start date as a parameter from the URL 
# Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset 

@app.route('/api/v1.0/<start_date>')
def start_date_temperatures(start_date):
    from datetime import datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    temperatures_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date).all()
    tobs = [temp for (date, temp) in temperatures_data]

    min_temp = min(tobs)
    max_temp = max(tobs)
    avg_temp = sum(tobs) / len(tobs)

    return jsonify({
        'start_date': start_date.strftime('%Y-%m-%d'),
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'average_temperature': avg_temp
    })



# A start/end route that:
# Accepts the start and end dates as parameters from the URL
# Returns the min, max, and average temperatures calculated from the given start date to the given end date 


@app.route('/api/v1.0/<start>/<end>')
def start_end_date_temperatures(start, end):
    from datetime import datetime
    
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    
    temperatures_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    tobs = [temp for (date, temp) in temperatures_data]
    min_temp = min(tobs)
    max_temp = max(tobs)
    avg_temp = sum(tobs) / len(tobs)
    
    return jsonify({
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'average_temperature': avg_temp
    })

if __name__ == '__main__':
    app.run(debug=True)