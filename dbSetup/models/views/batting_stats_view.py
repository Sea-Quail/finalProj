from sqlalchemy import text
from utils import create_enginestr_from_values, create_session_from_str
from sqlalchemy.orm import Session

# Generate engine string from utility function
database_values = {
    "dialect": "sqlite",  # Replace with your actual database dialect
    "database": "your_database.db",  # Replace with your actual database name
}
engine_str = create_enginestr_from_values(database_values)  # Ensure this function works correctly

# Create a SQLAlchemy engine
engine = create_session_from_str(engine_str)  # Ensure this function initializes a session/engine properly

# Define the SQL query
create_view_query = """
CREATE VIEW Batting_stats AS
SELECT
    Name,
    Age,
    G,
    PA,
    HR,
    SB,
    'BB%',
    'K%',
    BABIP,
    AVG,
    SLG,
    ISO,
    b_1B,
    wOBA,
    wRCplus,
    BsR,
    Total_Defensive_Plays,
    FRAA,
    ((wRCplus - 100) / 100 * PA / 10 + BsR + FRAA +
    (CASE
        WHEN position = 'SS' THEN 2
        WHEN position = 'CF' THEN 1
        WHEN position = '1B' THEN -1
        ELSE 0
    END) + 0.5 + 25) / 10 AS WAR,
    YearID,
    TeamID,
    Team_Name
FROM (
    SELECT
        CONCAT(p.nameFirst, ' ', p.nameLast) AS Name,
        (b.yearID - p.birthYear) AS Age,
        a.G_ALL AS G,
        (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF) AS PA,
        b.b_HR AS HR,
        b.b_SB AS SB,
        (b.b_BB / (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF)) * 100 AS `BB%`,
        (b.b_SO / (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF)) * 100 AS `K%`,
        (b.b_H - b.b_HR) / (b.b_AB - b.b_SO - b.b_HR + b.b_SF) AS BABIP,
        (b.b_H / b.b_AB) AS AVG,
        ((b.b_H - (b.b_2B + b.b_3B + b.b_HR)) + (2 * b.b_2B) + (3 * b.b_3B) + (4 * b.b_HR)) / b.b_AB AS SLG,
        (((b.b_H - (b.b_2B + b.b_3B + b.b_HR)) + (2 * b.b_2B) + (3 * b.b_3B) + (4 * b.b_HR)) / b.b_AB) - (b.b_H / b.b_AB) AS ISO,
        (b.b_H - (b.b_2B + b.b_3B + b.b_HR)) AS b_1B
    FROM batting b
    JOIN player p ON b.playerID = p.playerID
    JOIN appearances a ON b.playerID = a.playerID
) subquery;
"""

# Execute the raw SQL
with Session(engine) as session:
    session.execute(text(create_view_query))
    session.commit()