import csv
from csi3335f2024 import mysql
from models import Manager
from sqlalchemy.exc import SQLAlchemyError
from utils import create_enginestr_from_values, create_session_from_str, get_csv_path


def upload_managers_csv():
    print("Updating managers table")
    
    # Read the CSV paths for both Managers.csv and ManagersHalf.csv
    managers_csv_file_path = get_csv_path("Managers.csv")
    managers_half_csv_file_path = get_csv_path("ManagersHalf.csv")

    if len(managers_csv_file_path) == 0 and len(managers_half_csv_file_path) == 0:
        raise FileNotFoundError("Error: Neither Managers.csv nor ManagersHalf.csv found")

    # Process the CSV file(s)
    try:
        if managers_csv_file_path:
            result = update_managers_from_csv(managers_csv_file_path, in_season=1)
            print(f"Managers file processed successfully: {result}")
        
        if managers_half_csv_file_path:
            result = update_managers_from_csv(managers_half_csv_file_path, in_season=2)
            print(f"ManagersHalf file processed successfully: {result}")
    
    except Exception as e:
        raise RuntimeError(f"Error processing files: {str(e)}")


def update_managers_from_csv(file_path, in_season):
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            session = create_session_from_str(create_enginestr_from_values(mysql))
            counts = {"updated_rows": 0, "new_rows": 0}
            # Process rows
            for row in reader:
                process_row(row, session, counts, in_season)
            # Commit updates
            session.commit()
    except (csv.Error, SQLAlchemyError) as e:
        session.rollback()
        raise RuntimeError(f"Error updating managers from CSV: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")

    return counts


def process_row(row, session, counts, in_season):
    try:
        playerID = row["playerID"]
        yearID = int(row["yearID"])
        teamID = row["teamID"]
        # In case of ManagersHalf.csv, there is no plyrMgr field
        plyrMgr = row.get("plyrMgr") if "plyrMgr" in row else None
        half = row.get("half") if "half" in row else None  # Only present in ManagersHalf.csv

        # Handle "half season" (from ManagersHalf.csv)
        if in_season == 2 and not half:
            raise ValueError("Error: Missing 'half' field in ManagersHalf.csv for player: " + playerID)

        # Create the Manager entry
        manager_entry = Manager(
            playerID=playerID,
            yearID=yearID,
            teamID=teamID,
            inSeason=in_season,  # Full season = 1, Half season = 2
            manager_G=int(row["G"]) if row["G"] else None,
            manager_W=int(row["W"]) if row["W"] else None,
            manager_L=int(row["L"]) if row["L"] else None,
            teamRank=int(row["rank"]) if row["rank"] else None,
            plyrMgr=plyrMgr,
            half=int(half) if half else None  # Only populate half for ManagersHalf.csv
        )

        # Check if a row with the same playerID and yearID exists
        existing_entry = (
            session.query(Manager)
            .filter_by(
                playerID=playerID,
                yearID=yearID,
                teamID=teamID
            )
            .first()
        )

        if existing_entry:
            counts["updated_rows"] += 1
        else:
            counts["new_rows"] += 1

        session.merge(manager_entry)

    except SQLAlchemyError as e:
        raise RuntimeError(f"Error processing row: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")
