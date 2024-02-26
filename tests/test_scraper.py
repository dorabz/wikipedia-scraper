import pandas as pd
from scraper import scrape_player_info
import unittest


class TestScraper(unittest.TestCase):
    def test_scraper(self):
        urls_df = pd.read_csv("../data/playersURLs.csv", header=None, names=["URL"])

        first_url = urls_df.iloc[0, 0]

        self.assertTrue(first_url, "https://en.wikipedia.org/wiki/Kostas_Tsimikas")

        player_data = scrape_player_info(first_url)

        first_row_name = player_data["name"]

        self.assertEqual(
            first_row_name,
            "Kostas Tsimikas",
            f"Expected 'name' to be 'Kostas Tsimikas', got '{first_row_name}' instead.",
        )


if __name__ == "__main__":
    unittest.main()
