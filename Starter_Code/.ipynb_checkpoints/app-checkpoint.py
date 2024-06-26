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
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()



# Save references to each table
# Measurement = Base.classes.measurement
# stations = Base.classes.station

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
            "precipitation": "/api/v1.0/precipitation",
            "stations": "/api/v1.0/station",
            "temperature observations": "/api/v1.0/tobs",
            "temperature stats": "/api/v1.0/<start> and /api/v1.0/<start>/<end>"
        }
    })

if __name__ == '__main__':
    app.run(debug=True)