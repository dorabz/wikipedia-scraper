import sqlite3
from uuid import uuid4


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = self._connect_to_db()

    def _connect_to_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def _execute_sql(self, sql, params=None):
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def _get_player_id_by_url(self, url):
        """Fetches the player_id for a given URL if exists."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT player_id FROM players WHERE url = ?", (url,))
            result = cursor.fetchone()
            if result:
                return result[0]
        except sqlite3.Error as e:
            print(f"Database error when fetching player_id by URL: {e}")
        return None

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS players (
                    player_id TEXT PRIMARY KEY,
                    url TEXT UNIQUE,
                    name TEXT,
                    full_name TEXT,
                    date_of_birth TEXT,
                    age INTEGER,
                    place_of_birth TEXT,
                    country_of_birth TEXT,
                    positions TEXT,
                    current_club TEXT,
                    national_team TEXT,
                    appearances_current_club INTEGER,
                    goals_current_club INTEGER,
                    scraping_timestamp DATETIME
                );
                """
        self._execute_sql(create_table_sql)

    def insert_or_update_table_from_csv(self, player_data):
        insert_sql = """
        INSERT INTO players(player_id, url, name, full_name, date_of_birth, age, place_of_birth, 
        country_of_birth, positions, current_club, national_team, appearances_current_club, goals_current_club, scraping_timestamp)
        VALUES(:player_id, :url, :name, :full_name, :date_of_birth, :age, :place_of_birth, 
        :country_of_birth, :positions, :current_club, :national_team, :appearances_current_club, :goals_current_club, :scraping_timestamp)
        ON CONFLICT(url) DO UPDATE SET
        name=excluded.name,
        full_name=excluded.full_name,
        date_of_birth=excluded.date_of_birth,
        age=excluded.age,
        place_of_birth=excluded.place_of_birth,
        country_of_birth=excluded.country_of_birth,
        positions=excluded.positions,
        current_club=excluded.current_club,
        national_team=excluded.national_team,
        appearances_current_club=excluded.appearances_current_club,
        goals_current_club=excluded.goals_current_club,
        scraping_timestamp=excluded.scraping_timestamp;
        """
        self._execute_sql(insert_sql, player_data)

    def insert_or_update_table_from_scraper(self, player_data):
        if "url" in player_data:
            existing_id = self._get_player_id_by_url(player_data["url"])
            if existing_id:
                # for updates use existing player_id
                player_data["player_id"] = existing_id
            else:
                # for new insertions generate player_id if not provided
                if "player_id" not in player_data or not player_data["player_id"]:
                    player_data["player_id"] = str(uuid4())

        insert_sql = """
            INSERT INTO players (player_id, url, name, full_name, date_of_birth, age, place_of_birth, 
            country_of_birth, positions, current_club, national_team, appearances_current_club, 
            goals_current_club, scraping_timestamp)
            VALUES (:player_id, :url, :name, :full_name, :date_of_birth, :age, :place_of_birth, 
            :country_of_birth, :positions, :current_club, :national_team, :appearances_current_club, 
            :goals_current_club, :scraping_timestamp)
            ON CONFLICT(url) DO UPDATE SET
            name=CASE WHEN excluded.name IS NOT name OR (name IS NULL AND excluded.name IS NOT NULL) THEN excluded.name ELSE name END,
            full_name=CASE WHEN excluded.full_name IS NOT full_name OR (full_name IS NULL AND excluded.full_name IS NOT NULL) THEN excluded.full_name ELSE full_name END,
            date_of_birth=CASE WHEN excluded.date_of_birth IS NOT date_of_birth OR (date_of_birth IS NULL AND excluded.date_of_birth IS NOT NULL) THEN excluded.date_of_birth ELSE date_of_birth END,
            age=CASE WHEN excluded.age IS NOT age OR (age IS NULL AND excluded.age IS NOT NULL) THEN excluded.age ELSE age END,
            place_of_birth=CASE WHEN excluded.place_of_birth IS NOT place_of_birth OR (place_of_birth IS NULL AND excluded.place_of_birth IS NOT NULL) THEN excluded.place_of_birth ELSE place_of_birth END,
            country_of_birth=CASE WHEN excluded.country_of_birth IS NOT country_of_birth OR (country_of_birth IS NULL AND excluded.country_of_birth IS NOT NULL) THEN excluded.country_of_birth ELSE country_of_birth END,
            positions=CASE WHEN excluded.positions IS NOT positions OR (positions IS NULL AND excluded.positions IS NOT NULL) THEN excluded.positions ELSE positions END,
            current_club=CASE WHEN excluded.current_club IS NOT current_club OR (current_club IS NULL AND excluded.current_club IS NOT NULL) THEN excluded.current_club ELSE current_club END,
            national_team=CASE WHEN excluded.national_team IS NOT national_team OR (national_team IS NULL AND excluded.national_team IS NOT NULL) THEN excluded.national_team ELSE national_team END,
            appearances_current_club=CASE WHEN excluded.appearances_current_club IS NOT appearances_current_club OR (appearances_current_club IS NULL AND excluded.appearances_current_club IS NOT NULL) THEN excluded.appearances_current_club ELSE appearances_current_club END,
            goals_current_club=CASE WHEN excluded.goals_current_club IS NOT goals_current_club OR (goals_current_club IS NULL AND excluded.goals_current_club IS NOT NULL) THEN excluded.goals_current_club ELSE goals_current_club END,
            scraping_timestamp=excluded.scraping_timestamp
            WHERE (excluded.url IS NOT NULL);
            """
        self._execute_sql(insert_sql, player_data)

    def close_connection(self):
        if self.conn:
            self.conn.close()
