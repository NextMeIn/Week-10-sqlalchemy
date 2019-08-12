import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

# Save reference to the table
#Passenger = Base.classes.passenger
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Available Routes:"
        f"<br/>/api/v1.0/precipitation"
        f"<br/>/api/v1.0/stations"
        f"<br/>/api/v1.0/tobs"
        f"<br/>/api/v1.0/<start>"
        f"<br/>/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    data = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date).all()
    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    return jsonify(session.query(Measurement.station).group_by(Measurement.station).all())

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lastdate = str(lastdate[0])
    lastdate = dt.datetime(*[int(lstdt) for lstdt in lastdate.split("-")]) - dt.timedelta(days=365)
    data = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>lastdate).order_by(Measurement.date.desc()).all()    
    return jsonify(data)

@app.route("/api/v1.0/<stdt>")
def calcu1(stdt):
    session = Session(engine)
    data = session.query(func.min(Measurement.tobs).label('Min'),func.avg(Measurement.tobs).label('Avg'),func.max(Measurement.tobs).label('Max')).filter(Measurement.date>stdt).all()
    return jsonify(data)

@app.route("/api/v1.0/<stdt>/<endt>")
def calcu2(stdt,endt):
    if stdt<endt:
        session = Session(engine)
        data = session.query(func.min(Measurement.tobs).label('Min'),func.avg(Measurement.tobs).label('Avg'),func.max(Measurement.tobs).label('Max')).filter(Measurement.date>stdt).filter(Measurement.date<endt).all()
        return jsonify(data)
    return jsonify("Wrong date range!!")

if __name__ == "__main__":    
    app.run(debug=True)    