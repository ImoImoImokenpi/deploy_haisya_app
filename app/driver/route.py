from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from ..models import Driver, CheckedDriver
from .. import db

driver_bp = Blueprint("driver", __name__)

@driver_bp.route("/add_driver", methods=["GET", "POST"])
@login_required
def add_driver():
    if CheckedDriver.query.first():
        db.session.query(CheckedDriver).delete()
        db.session.commit()

    if request.method == "POST":
        name = request.form['driver_name']
        old = request.form['driver_old']
        jenre = request.form['driver_jenre']
        capacity = request.form['driver_capacity']
        
        new_driver = Driver(name=name, old=old, jenre=jenre, capacity=capacity)
        db.session.add(new_driver)
        db.session.commit()

        return redirect(url_for("driver.add_driver"))
    
    all_drivers = Driver.query.order_by(Driver.old.desc()).all()
    driver_by_old = {}
    for driver in all_drivers:
        if driver.old not in driver_by_old:
            driver_by_old[driver.old] = []
        driver_by_old[driver.old].append(driver)

    return render_template("driver/select_d.html", drivers=driver_by_old)

@driver_bp.route("/delete_driver/<int:driver_id>", methods=["POST"])
@login_required
def delete_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if driver:
        db.session.delete(driver)
        db.session.commit()

    all_drivers = Driver.query.all()
    driver_by_old = {}
    for driver in all_drivers:
        if driver.old not in driver_by_old:
            driver_by_old[driver.old] = []
        driver_by_old[driver.old].append(driver)

    return render_template("driver/select_d.html", drivers=driver_by_old)

@driver_bp.route("/checked_driver", methods=["POST"])
@login_required
def checked_driver():
    checked_drivers_ids = request.form.getlist("drivers")
    for  driver_id_str in checked_drivers_ids:
        driver_id = int(driver_id_str)
        section = request.form.get(f'section-{driver_id}')
        rehersal = request.form.get(f'rehersal-{driver_id}')
    
        driver = Driver.query.get(driver_id)
        if driver and section and rehersal:
            checked_driver = CheckedDriver(
                name=driver.name, 
                old=driver.old,
                jenre=driver.jenre,
                section=section,
                rehersal=rehersal,
                capacity=driver.capacity
            )
            db.session.add(checked_driver)

    db.session.commit()
    return redirect(url_for("passenger.add_passenger"))
