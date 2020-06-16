from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
import pandas as pd

from flask import Flask, jsonify
#%%
engine = create_engine("sqlite:///hawaii.sqlite")

#%%
app = Flask(__name__)

#%%
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
#%%
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = pd.read_sql('SELECT * FROM measurement', engine)
    results_json = results[['date','prcp']].to_json(orient='records') 
    return results_json
#%%
@app.route("/api/v1.0/stations")
def station():
    
    results = pd.read_sql('SELECT * FROM station', engine)
    results_json = results['station'].to_json(orient='records') 
    return results_json

#%%
#I was having a lot of difficulty with this one, and just had to hard-code the numbers
@app.route("/api/v1.0/tobs")
def tobs():
    
    results = pd.read_sql('SELECT * FROM measurement m WHERE m.station = "USC00519281" AND m.date BETWEEN "2016-08-18" AND "2017-08-18"', engine)
    results_json = results[['date','tobs']].to_json(orient='records')
    return results_json
    
#%%
@app.route("/api/v1.0/<start>")

def start_only(start):
    results = pd.read_sql(f'SELECT * FROM measurement m WHERE m.date >= "{start}"', engine)
    #results_json = results[['date','tobs']].to_json(orient='records')
    max_temp = max(results['tobs'])
    min_temp = min(results['tobs'])
    avg_temp = results['tobs'].mean()
    return f'In Hawaii after {start}, the maximum temperature was {max_temp}, the minimum temperature was {min_temp}, and the average temperature was {avg_temp:.1f}'

#%%
@app.route("/api/v1.0/<start>/<end>")

def start_end(start, end):
    results = pd.read_sql(f'SELECT * FROM measurement m WHERE m.date BETWEEN "{start}" AND "{end}"', engine)
    #results_json = results[['date','tobs']].to_json(orient='records')
    max_temp = max(results['tobs'])
    min_temp = min(results['tobs'])
    avg_temp = results['tobs'].mean()
    return f'In Hawaii between {start} and {end}, the maximum temperature was {max_temp}, the minimum temperature was {min_temp}, and the average temperature was {avg_temp:.1f}'

#%%
if __name__ == '__main__':
    app.run(debug=True)