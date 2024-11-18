from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import RosterForm

from dbSetup.models.tables import Teams

home_routes = Blueprint("roster_routes", __name__, template_folder="templates")

# /login
@home_routes.route("/teamRoster", methods=["GET", "POST"])
def login():
    form = RosterForm()
    if form.validate_on_submit():
        # Retrieve the team and year combo from the database
        team = Teams.query.filter_by(team_name=form.team_name.data, yearID=form.year.data).first()

        if team:
            return redirect(url_for("roster_routes.home"))

        flash("Invalid team name and/or year", "danger")

    return render_template("login.html", title="Sign In", form=form)


@home_routes.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home_routes.login"))
