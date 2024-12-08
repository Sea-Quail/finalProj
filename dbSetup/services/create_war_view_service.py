import csv
import os
from sqlalchemy import text
from utils import create_session_from_str, create_enginestr_from_values
from models import WarData  # Ensure you import the WarData model
import csi3335f2024 as cfg

def insert_csv_data(session, csv_file_path):
    """Insert data from a CSV into the WarData table."""
    try:
        with open(csv_file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure data is valid before inserting
                wardata = WarData(
                    playerID=row["key_bbref"],
                    Name=row["player_name"],
                    yearID=int(row["year_ID"]),
                    WRC_Plus=int(row["wRC_plus"]) if row["wRC_plus"] != 'NA' else None,
                    WAR=float(row["bwar162"]) if row["bwar162"] != 'NA' else None
                )
                session.add(wardata)
        session.commit()  # Commit the changes to insert the data
        print("Data inserted successfully.")
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"Error during processing or data insertion: {e}")
        session.rollback()  # Rollback in case of error

def create_warstats_csv_view():
    """Create the WarData table and insert data from the CSV."""
    # Get the absolute path of the project root directory (going up two levels from 'dbSetup')
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_path = os.path.join(project_root, 'static', 'csv', 'BattingWarData.csv')

    if not os.path.exists(csv_file_path):
        print(f"Error: The file '{csv_file_path}' does not exist.")
        return  # Exit early if file doesn't exist

    # Create engine string and session
    engine_str = create_enginestr_from_values(mysql=cfg.mysql)
    session = create_session_from_str(engine_str)


    # Step 1: Insert data from the CSV
    insert_csv_data(session, csv_file_path)

    # Close the session after everything is done
    session.close()
    print("Session closed.")

