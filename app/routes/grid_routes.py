<<<<<<< HEAD
<<<<<<< HEAD
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db

from ..filters import (
    CareerStatFilter,
    MiscFilter,
    PositionFilter,
    SeasonStatFilter,
    TeamFilter,
)
from ..models import Appearances, People, Teams
from ..static.constants import OPTION_GROUPS, TEAM_MAPPINGS

from app import db

from ..filters import (
    CareerStatFilter,
    MiscFilter,
    PositionFilter,
    SeasonStatFilter,
    TeamFilter,
)
from ..models import Appearances, People, Teams
from ..static.constants import OPTION_GROUPS, TEAM_MAPPINGS
=======
from flask import Blueprint, render_template
>>>>>>> 546a4c9 (adding routes for the grid solver)
=======
from flask import Blueprint, flash, redirect, render_template, request, url_for
>>>>>>> 484ee0f (Fixing bug with dropdown menus being linked)

grid_routes = Blueprint("grid_routes", __name__, template_folder="templates")


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> a1ea04f (Adding logic to remember form fields when invalid input occurs)
def extract_form_data():
    return {
        "prompt1": {
            "prompt1-option": request.form.get("prompt1-option"),
            "prompt1-operator": request.form.get("prompt1-operator"),
            "prompt1-number": request.form.get("prompt1-number"),
            "prompt1-team": request.form.get("prompt1-team"),
        },
        "prompt2": {
            "prompt2-option": request.form.get("prompt2-option"),
            "prompt2-operator": request.form.get("prompt2-operator"),
            "prompt2-number": request.form.get("prompt2-number"),
            "prompt2-team": request.form.get("prompt2-team"),
        },
    }


def validate_form_data(form_data):
    errors = []

    # Check required fields
    if not form_data["prompt1"]["prompt1-option"]:
        errors.append("Prompt 1 is required.")
    if not form_data["prompt2"]["prompt2-option"]:
        errors.append("Prompt 2 is required.")

    # Check additional fields for prompt1
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    if (
        form_data["prompt1"]["prompt1-option"] in OPTION_GROUPS["Career Options"].keys()
        or form_data["prompt1"]["prompt1-option"]
        in OPTION_GROUPS["Season Options"].keys()
    ):
=======
    if form_data["prompt1"]["prompt1-option"] in [
        "avg_career",
        "era_career",
        "wins_career",
        "k_career",
        "hits_career",
        "hr_career",
        "save_career",
        "war_career",
        "avg_season",
        "era_season",
        "hr_season",
        "win_season",
        "rbi_season",
        "run_season",
        "hits_season",
        "k_season",
        "hr_sb_season",
        "save_season",
        "war_season",
    ]:
>>>>>>> a1ea04f (Adding logic to remember form fields when invalid input occurs)
=======
    if form_data["prompt1"]["prompt1-option"] in career_and_season_options:
>>>>>>> f0fd25d (Creating initial filter structure and some refactoring)
=======
    if (
        form_data["prompt1"]["prompt1-option"] in OPTION_GROUPS["Career Options"].keys()
        or form_data["prompt1"]["prompt1-option"]
        in OPTION_GROUPS["Season Options"].keys()
    ):
>>>>>>> 33d1249 (query filters)
        if not form_data["prompt1"]["prompt1-operator"]:
            errors.append("Operator for Prompt 1 is required.")
        if not form_data["prompt1"]["prompt1-number"]:
            errors.append("Number for Prompt 1 is required.")
    if (
        form_data["prompt1"]["prompt1-option"] == "played_for_team"
        and not form_data["prompt1"]["prompt1-team"]
    ):
        errors.append("Team for Prompt 1 is required.")

    # Check additional fields for prompt2
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    if (
        form_data["prompt2"]["prompt2-option"] in OPTION_GROUPS["Career Options"].keys()
        or form_data["prompt2"]["prompt2-option"]
        in OPTION_GROUPS["Season Options"].keys()
    ):
=======
    if form_data["prompt2"]["prompt2-option"] in [
        "avg_career",
        "era_career",
        "wins_career",
        "k_career",
        "hits_career",
        "hr_career",
        "save_career",
        "war_career",
        "avg_season",
        "era_season",
        "hr_season",
        "win_season",
        "rbi_season",
        "run_season",
        "hits_season",
        "k_season",
        "hr_sb_season",
        "save_season",
        "war_season",
    ]:
>>>>>>> a1ea04f (Adding logic to remember form fields when invalid input occurs)
=======
    if form_data["prompt2"]["prompt2-option"] in career_and_season_options:
>>>>>>> f0fd25d (Creating initial filter structure and some refactoring)
=======
    if (
        form_data["prompt2"]["prompt2-option"] in OPTION_GROUPS["Career Options"].keys()
        or form_data["prompt2"]["prompt2-option"]
        in OPTION_GROUPS["Season Options"].keys()
    ):
>>>>>>> 33d1249 (query filters)
        if not form_data["prompt2"]["prompt2-operator"]:
            errors.append("Operator for Prompt 2 is required.")
        if not form_data["prompt2"]["prompt2-number"]:
            errors.append("Number for Prompt 2 is required.")
    if (
        form_data["prompt2"]["prompt2-option"] == "played_for_team"
        and not form_data["prompt2"]["prompt2-team"]
    ):
        errors.append("Team for Prompt 2 is required.")

    return errors


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 33d1249 (query filters)
# Returns an array of two dictionaries, one for each prompt
def parse_prompts(form_data):
    params = []
    if form_data["prompt1"]:
        params.append(
            {
                "option": form_data["prompt1"]["prompt1-option"],
                "operator": form_data["prompt1"]["prompt1-operator"],
                "number": form_data["prompt1"]["prompt1-number"],
                "team": form_data["prompt1"]["prompt1-team"],
            }
        )

    if form_data["prompt2"]:
        params.append(
            {
                "option": form_data["prompt2"]["prompt2-option"],
                "operator": form_data["prompt2"]["prompt2-operator"],
                "number": form_data["prompt2"]["prompt2-number"],
                "team": form_data["prompt2"]["prompt2-team"],
            }
        )

    return params
<<<<<<< HEAD


def perform_query(form_data):
    # Get base query
    query = db.session.query(People)

    # Extract parameters from the form data
    params = parse_prompts(form_data)

    flash(params, "info")

    # Apply filters based on the form data
    for param in params:
        option = param["option"]
        operator = param["operator"]
        number = param["number"]
        team = param["team"]

        if option in OPTION_GROUPS["Career Options"].keys():
            query = CareerStatFilter(
                query, option, operator, float(number), team
            ).apply()
        elif option in OPTION_GROUPS["Season Options"].keys():
            query = SeasonStatFilter(
                query, option, operator, float(number), team
            ).apply()
        elif option == "played_for_team":
            query = TeamFilter(query, team).apply()
        elif option.startswith("played_"):
            query = PositionFilter(query, option, team).apply()
        else:
            query = MiscFilter(query, option, team).apply()

    result = query.first()

    if result:
        player_name = f"{result.nameFirst} {result.nameLast}"
        return player_name

    return None


=======
>>>>>>> 484ee0f (Fixing bug with dropdown menus being linked)
=======
>>>>>>> a1ea04f (Adding logic to remember form fields when invalid input occurs)
=======
def perform_query(form_data):
    return


>>>>>>> f0fd25d (Creating initial filter structure and some refactoring)
=======
def parse_prompts(form_data, params):
    return
=======
>>>>>>> 33d1249 (query filters)


def perform_query(form_data):
    # Get base query
    query = db.session.query(People)

    # Extract parameters from the form data
    params = parse_prompts(form_data)

    flash(params, "info")

    # Apply filters based on the form data
    for param in params:
        option = param["option"]
        operator = param["operator"]
        number = param["number"]
        team = param["team"]

        if option in OPTION_GROUPS["Career Options"].keys():
            query = CareerStatFilter(
                query, option, operator, float(number), team
            ).apply()
        elif option in OPTION_GROUPS["Season Options"].keys():
            query = SeasonStatFilter(
                query, option, operator, float(number), team
            ).apply()
        elif option == "played_for_team":
            query = TeamFilter(query, team).apply()
        elif option.startswith("played_"):
            query = PositionFilter(query, option, team).apply()
        else:
            query = MiscFilter(query, option, team).apply()

    result = query.first()

    if result:
        player_name = f"{result.nameFirst} {result.nameLast}"
        return player_name

    return None


>>>>>>> 361e2af (adding a test query and transfering tables from dbsetup to prod)
@grid_routes.route("/", methods=["GET", "POST"])
def get_player():
    if request.method == "POST":
        # Extract form data
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> a1ea04f (Adding logic to remember form fields when invalid input occurs)
        form_data = extract_form_data()

        # Validate form data
        errors = validate_form_data(form_data)
        if errors:
            for error in errors:
                flash(error, "error")

            flash(form_data, "info")
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 736ea61 (major refactoring)
            return render_template(
                "immaculate_grid.html",
                team_mappings=TEAM_MAPPINGS,
                option_groups=OPTION_GROUPS,
                form_data=form_data,
            )

        # Add this step when table definitions allow for proper querying
        # name = perform_query(form_data)

        flash(form_data, "info")
        return redirect(url_for("grid_routes.get_player"))

    return render_template(
        "immaculate_grid.html", team_mappings=TEAM_MAPPINGS, option_groups=OPTION_GROUPS
    )
<<<<<<< HEAD
=======
@grid_routes.route("/")
def prompts():
=======
        prompt1 = request.form.get("prompt1")
        prompt2 = request.form.get("prompt2")
        operator = request.form.get("operator")
        number = request.form.get("number")
        team = request.form.get("team")
        position = request.form.get("position")
=======
            return render_template("immaculate_grid.html", form_data=form_data)
>>>>>>> a1ea04f (Adding logic to remember form fields when invalid input occurs)

        # Add this step when table definitions allow for proper querying
        # name = perform_query(form_data)

        flash(form_data, "info")
        return redirect(url_for("grid_routes.get_player"))

>>>>>>> 484ee0f (Fixing bug with dropdown menus being linked)
    return render_template("immaculate_grid.html")
>>>>>>> 546a4c9 (adding routes for the grid solver)
=======
>>>>>>> 736ea61 (major refactoring)
