import csv
import sys
from datetime import datetime
from uuid import uuid4

from db_manager import DatabaseManager


def import_csv_to_db(db_path, csv_file_path):
    db_manager = DatabaseManager(db_path)
    db_manager.create_table()

    try:
        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                # generate a UUID as player_id if not provided
                player_id = row.get("PlayerID", str(uuid4()))
                player_data = {
                    "player_id": player_id,
                    "url": row.get("URL"),
                    "name": row.get("Name") if row.get("Name", "").strip() else None,
                    "full_name": (
                        row.get("Full name")
                        if row.get("Full name", "").strip()
                        else None
                    ),
                    "date_of_birth": (
                        row.get("Date of birth")
                        if row.get("Date of birth", "").strip()
                        else None
                    ),
                    "age": (
                        row.get("Age") if row.get("Age", "").strip().isdigit() else None
                    ),
                    "place_of_birth": (
                        row.get("City of birth")
                        if row.get("City of birth", "").strip()
                        else None
                    ),
                    "country_of_birth": (
                        row.get("Country of birth")
                        if row.get("Country of birth", "").strip()
                        else None
                    ),
                    "positions": (
                        row.get("Position") if row.get("Position", "").strip() else None
                    ),
                    "current_club": (
                        row.get("Current club")
                        if row.get("Current club", "").strip()
                        else None
                    ),
                    "national_team": (
                        row.get("National_team")
                        if row.get("National_team", "").strip()
                        else None
                    ),
                    "appearances_current_club": None,
                    "goals_current_club": None,
                    "scraping_timestamp": None,
                }

                db_manager.insert_or_update_table_from_csv(player_data)

        db_manager.close_connection()
    except Exception as e:
        print(f"Failed to read the playersData.csv file: {e}")
        sys.exit(1)
