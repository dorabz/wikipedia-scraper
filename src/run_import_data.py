from csv_importer import import_csv_to_db
from scraper_importer import import_scraper_to_db


def main():
    db_path = "../db/database.sqlite"
    csv_file_path = "../data/playersData.csv"
    output_csv_file_path = "../data/scraped_player_data.csv"

    import_csv_to_db(db_path, csv_file_path)

    import_scraper_to_db(db_path, output_csv_file_path)

    print("Data import completed successfully.")


if __name__ == "__main__":
    main()
