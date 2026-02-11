from flask import Blueprint
from flask import render_template
from flask_login import login_required
import random

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
@login_required
def toppage():
    return render_template("toppage.html")
