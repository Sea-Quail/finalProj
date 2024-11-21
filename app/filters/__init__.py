<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 33d1249 (query filters)
from .query_filter import (
    CareerStatFilter,
    MiscFilter,
    PositionFilter,
    SeasonStatFilter,
    TeamFilter,
)
<<<<<<< HEAD

# Optionally, you can define a list of available filters for easier imports
FILTERS = {
    "career_stat": CareerStatFilter,
    "season_stat": SeasonStatFilter,
    "position": PositionFilter,
    "misc": MiscFilter,
    "team": TeamFilter,
=======
from .position_filter import PositionFilter
from .team_filter import TeamFilter
=======
>>>>>>> 33d1249 (query filters)

# Optionally, you can define a list of available filters for easier imports
FILTERS = {
    "career_stat": CareerStatFilter,
    "season_stat": SeasonStatFilter,
    "position": PositionFilter,
<<<<<<< HEAD
>>>>>>> f0fd25d (Creating initial filter structure and some refactoring)
=======
    "misc": MiscFilter,
    "team": TeamFilter,
>>>>>>> 33d1249 (query filters)
}
