import sys
from pathlib import Path
import pandas as pd
from src.scraper import scrape_player_info


def main(urls_file_path):
    urls_file = Path(urls_file_path)
    if urls_file.suffix.lower() != ".csv":
        print("Error: The file provided is not a CSV file.")
        sys.exit(1)

    try:
        urls_df = pd.read_csv(urls_file, header=None, names=["URL"])
    except Exception as e:
        print(f"Failed to read the URLs file: {e}")
        sys.exit(1)

    valid_player_infos = []

    for url in urls_df["URL"]:
        player_info = scrape_player_info(url)
        if player_info is not None:
            valid_player_infos.append(player_info)
        else:
            print(f"No player data found for the URL: {url}; skipping.")

    if valid_player_infos:
        player_infos_df = pd.DataFrame(valid_player_infos)
        output_csv_file_path = "data/scraped_player_data.csv"
        player_infos_df.to_csv(output_csv_file_path, sep=";", index=False)
        print(f"Scraped data saved to {output_csv_file_path}")
    else:
        print("No valid player data was scraped.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage format: python scraper.py path/to/urls_file.csv")
        sys.exit(1)

    main(sys.argv[1])
