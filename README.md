# Football Players Information Scraper in Python

## Description

This project is designed to scrape player data from a list of URLs, save the scraped data into a CSV file, and then update a database with the scraped information. It includes functionality to handle command-line inputs for the URLs file and ensures data integrity by checking for valid CSV files and non-null data.

## Features

- Scrapes player data from given URLs.
- Saves valid scraped data into a CSV file.
- Loads initial database information from given playerData.CSV file.
- Updates a SQLite database with the scraped data.
- SQL queries for insight into data.
- Command-line interface for easy use.

## Requirements

- Python 3.x
- Pandas
- Other dependencies as listed in `requirements.txt`

## Installation

1. Clone the repository and navigate to the project directory.
2. Install the required Python packages:


**pip install -r requirements.txt**


## Scraping Data

1. Prepare a CSV file containing the URLs to scrape, with each URL in a new line.
2. Run the scraper script with the path to your URLs file:

**python run_scraper.py path/to/your/urls_file.csv**

3. Run rest of the code - database loading:

**python run_import_data.py**

This will save the scraped data into `scraped_player_data.csv` in the data folder.

## Running Tests

To run tests verifying the correctness of the scraping and data processing:
In tests folder:


python -m unittest test_scraper_output.py or python -m unittest test_scraper.py 



## Sql queries

In sql_queries folder, there are three sql queries that correspond to the three queries in pdf on page 2.
In csv files are results of each query.


