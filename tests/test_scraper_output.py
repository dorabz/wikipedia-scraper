import unittest
import pandas as pd


class TestScraperOutput(unittest.TestCase):
    def test_first_row_name(self):
        df = pd.read_csv("../data/scraped_player_data.csv")

        self.assertTrue(not df.empty, "The DataFrame is empty.")

        first_row_name = df.iloc[0]["name"]

        self.assertEqual(
            first_row_name,
            "Kostas Tsimikas",
            f"Expected 'name' to be 'Kostas Tsimikas', got '{first_row_name}' instead.",
        )


if __name__ == "__main__":
    unittest.main()
