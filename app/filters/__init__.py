<<<<<<< HEAD
from .query_filter import (
    CareerStatFilter,
    MiscFilter,
    PositionFilter,
    SeasonStatFilter,
    TeamFilter,
)

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

# Optionally, you can define a list of available filters for easier imports
FILTERS = {
    "team": TeamFilter,
    "position": PositionFilter,
>>>>>>> f0fd25d (Creating initial filter structure and some refactoring)
}
