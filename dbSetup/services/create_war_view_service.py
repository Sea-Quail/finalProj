import csv
import os
import csi3335f2024 as cfg
from sqlalchemy import text
from utils import create_session_from_str, create_enginestr_from_values

from sqlalchemy import (
    Column,
    Float,
    Integer,
    SmallInteger,
    String,
)
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class WarData(Base):
    __tablename__ = "WarData"
    wardata_ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    playerID = Column(String, nullable=False)
    Name = Column(String(255), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    WRC_Plus = Column(Integer, nullable=True)

def create_table_if_not_exists(session):
    # SQL query to create the WARtable
    create_table_query = """
    CREATE TABLE IF NOT EXISTS WarData (
        wardata_ID INT AUTO_INCREMENT PRIMARY KEY,
        playerID VARCHAR(9),
        Name VARCHAR(255) NOT NULL,
        yearID SMALLINT NOT NULL,
        WRC_Plus INT
    );
    """
    
    try:
        # Wrap the query with text() to ensure it's correctly interpreted
        session.execute(text(create_table_query))
        session.commit()  # Commit the transaction
        print("Table 'WARtable' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
        session.rollback()  # Rollback in case of error



def insert_csv_data(session, csv_file_path):
    try:
        with open(csv_file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                wardata = WarData(
                    playerID=row["key_bbref"],
                    Name=row["player_name"],
                    yearID=int(row["year_ID"]),
                    WRC_Plus = int(row["wRC_plus"]) if row["wRC_plus"] != 'NA' else None
                )
                session.add(wardata)
        session.commit()  # Commit the changes to insert the data
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"Error during processing or data insertion: {e}")
        session.rollback()  # Rollback in case of error

def create_warstats_csv_view():
    # Get the absolute path of the project root directory (going up two levels from 'dbSetup')
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_path = os.path.join(project_root, 'static', 'csv', 'BattingWarData.csv')
    
    

    # Create engine string and session
    engine_str = create_enginestr_from_values(mysql=mysql)
    session = create_session_from_str(engine_str)

    # Step 1: Create the table
    create_table_if_not_exists(session)

    # Step 2: Insert data from CSV
    insert_csv_data(session, csv_file_path)

    # Close the session after everything is done
    session.close()

    