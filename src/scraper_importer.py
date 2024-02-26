import csv
import sys
from datetime import datetime
from uuid import uuid4
import pandas as pd

from db_manager import DatabaseManager
from scraper import scrape_player_info


def import_scraper_to_db(db_path, output_csv_file_path):
    db_manager = DatabaseManager(db_path)

    try:
        with open(output_csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            for row in reader:
                player_data = {
                    "url": row.get("url"),
                    "name": row.get("name") if row.get("name", "").strip() else None,
                    "full_name": (
                        row.get("full_name")
                        if row.get("full_name", "").strip()
                        else None
                    ),
                    "date_of_birth": (
                        row.get("date_of_birth")
                        if row.get("date_of_birth", "").strip()
                        else None
                    ),
                    "age": row.get("age") if row.get("age", "").strip() else None,
                    "place_of_birth": (
                        row.get("place_of_birth")
                        if row.get("place_of_birth", "").strip()
                        else None
                    ),
                    "country_of_birth": (
                        row.get("country_of_birth")
                        if row.get("country_of_birth", "").strip()
                        else None
                    ),
                    "positions": (
                        row.get("positions")
                        if row.get("positions", "").strip()
                        else None
                    ),
                    "current_club": (
                        row.get("current_club")
                        if row.get("current_club", "").strip()
                        else None
                    ),
                    "national_team": (
                        row.get("national_team")
                        if row.get("national_team", "").strip()
                        else None
                    ),
                    "appearances_current_club": (
                        row.get("appearances_current_club")
                        if row.get("appearances_current_club", "").strip()
                        else None
                    ),
                    "goals_current_club": (
                        row.get("goals_current_club")
                        if row.get("goals_current_club", "").strip()
                        else None
                    ),
                    "scraping_timestamp": row.get("scraping_timestamp"),
                }

                db_manager.insert_or_update_table_from_scraper(player_data)

        db_manager.close_connection()
    except Exception as e:
        print(f"Failed to read the CSV file: {e}")
        sys.exit(1)
