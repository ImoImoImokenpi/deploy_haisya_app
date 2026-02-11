from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from ..models import Passenger, CheckedPassenger
from .. import db

passenger_bp = Blueprint("passenger", __name__)

@passenger_bp.route("/add_passenger", methods=["GET", "POST"])
@login_required
def add_passenger(): 
    if CheckedPassenger.query.first():
        db.session.query(CheckedPassenger).delete()
        db.session.commit()

    if request.method == "POST":
        name = request.form['passenger_name']
        old = request.form['passenger_old']
        jenre = request.form['passenger_jenre']
        
        new_passenger = Passenger(name=name, old=old, jenre=jenre)
        db.session.add(new_passenger)
        db.session.commit()

        return redirect(url_for("passenger.add_passenger"))
    
    passenger_by_old = {}
    all_passengers = Passenger.query.order_by(Passenger.old.desc()).all()
    for passenger in all_passengers:
        if passenger.old not in passenger_by_old:
            passenger_by_old[passenger.old] = []
        passenger_by_old[passenger.old].append(passenger)

    return render_template("passenger/select_p.html", passengers=passenger_by_old)

@passenger_bp.route("/delete_passenger/<int:passenger_id>", methods=["POST"])
@login_required
def delete_passenger(passenger_id):
    passenger = Passenger.query.get(passenger_id)
    if passenger:
        db.session.delete(passenger)
        db.session.commit()

    passenger_by_old = {}
    all_passengers = Passenger.query.all()
    for passenger in all_passengers:
        if passenger.old not in passenger_by_old:
            passenger_by_old[passenger.old] = []
        passenger_by_old[passenger.old].append(passenger)

    return render_template("passenger/select_p.html", passengers=passenger_by_old)


@passenger_bp.route("/checked_passenger", methods=["POST"])
@login_required
def checked_passenger():
    checked_passengers_ids = request.form.getlist("passengers")
    for passenger_id_str in checked_passengers_ids:
        passenger_id = int(passenger_id_str)
        section = request.form.get(f'section-{passenger_id}')
        rehersal = request.form.get(f'rehersal-{passenger_id}')
    
        passenger = Passenger.query.get(passenger_id)
        if passenger and section and rehersal:
            checked_passenger = CheckedPassenger(
                name=passenger.name, 
                old=passenger.old,
                jenre=passenger.jenre,
                section=section, 
                rehersal=rehersal
            )
            db.session.add(checked_passenger)

    db.session.commit()
    return redirect(url_for("matching.setup"))
