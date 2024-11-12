<<<<<<< HEAD
<<<<<<< HEAD
from .tables import AllstarFull, Leagues, People, Schools, SeriesPost, Teams, Pitching, Appearances, Fielding, HallofFame
=======
from .tables import (
    AllstarFull,
    Leagues,
    People,
    Schools,
    SeriesPost,
    Teams,
    Pitching,
    Appearances,
    Fielding,
    Batting,
    BattingPost
)
>>>>>>> d9ac3b9 (batting post table tested)
=======
from .tables import AllstarFull, HomeGames, Leagues, People, Schools, SeriesPost, Teams, Pitching, Appearances, Fielding
>>>>>>> 6ee8472 (homegames setup!)

# Import other models as needed

# For easy access to all models
all_models = [
    AllstarFull,
    People,
    Leagues,
    Teams,
    Schools,
    SeriesPost,
    Pitching,
    Appearances,
    Fielding,
<<<<<<< HEAD
<<<<<<< HEAD
    HallofFame
=======
    Batting,
    BattingPost
>>>>>>> d9ac3b9 (batting post table tested)
=======
    HomeGames
>>>>>>> 6ee8472 (homegames setup!)
]
