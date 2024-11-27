import csv

import csi3335f2024 as cfg
from models import HallofFame, People
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_halloffame_csv():
    print("Updating halloffame table")
    csv_file_path = get_csv_path("HallOfFame.csv")

    if len(csv_file_path) == 0:
        print("Error: HallOfFame.csv not found")
        return

    # Process the CSV file
    try:
        print(update_halloffame_from_csv(csv_file_path))
        print("File processed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")


def update_halloffame_from_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = 0
        updated_rows = 0
        peopleNotExist=0
        teamNotExist=0

        # Create session
        session = create_session_from_str(create_enginestr_from_values(mysql=cfg.mysql))

        for row in reader:
            halloffame_record = HallofFame(
                playerID=row['playerID'],
                yearID=int(row['yearid']),
                votedBy=row['votedBy'],
                ballots=int(row['ballots']) if row['ballots'].isdigit() else None,
                needed = int(row["needed"]) if row["needed"].isdigit() else None,
                votes = int(row["votes"]) if row["votes"].isdigit() else None,
                inducted = row["inducted"] if row["inducted"] else None,
                category = row["category"] if row["category"] else None,
                note = row["needed_note"][:25] if row["needed_note"] else None,
            )

            # Check if playerID exists in the people table
            player_exists = session.query(People).filter_by(playerID=halloffame_record.playerID).first()

            if not player_exists:
                peopleNotExist+=1
                #if we make an error log, message could go here.
                continue

            # Check if a row with the same playerID, yearID, teamID, and stint exists
            existing_entry = (
                session.query(HallofFame)
                .filter_by(
                    playerID=halloffame_record.playerID,
                    yearID=halloffame_record.yearID,
                )
                .first()
            )
            if existing_entry:
                updated_rows += 1
            
            else:
                new_rows += 1

            session.merge(halloffame_record)
        session.commit()
    session.close()
    return {
        "new_rows: ": new_rows,
        "updated_rows: ": updated_rows,
        "rows skipped bc their playerid didn't exist in people table: ": peopleNotExist, 
        "rows skipped bc their teamid didnt exist in teams table: ": teamNotExist
    }
