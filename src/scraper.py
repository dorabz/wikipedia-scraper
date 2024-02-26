import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def calculate_age_from_dob(dob_str):
    """
    Calculate age given a date of birth string in YYYY-MM-DD format.
    """
    dob = datetime.strptime(dob_str, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


def scrape_text_based_info(soup):
    """
    Scrape information from text paragraphs when structured data is missing.
    """
    text = soup.get_text()
    player_info = {}

    dob_regex_patterns = [
        re.compile(r"born on (\d{1,2} [A-Za-z]+ \d{4})"),
        re.compile(r"\b(\d{1,2} [A-Za-z]+ \d{4})\b"),
        re.compile(r"\((\d{1,2} [A-Za-z]+ \d{4})\)"),
    ]

    for regex in dob_regex_patterns:
        dob_match = regex.search(text)
        if dob_match:
            dob_str = dob_match.group(1)
            try:
                dob_datetime = datetime.strptime(dob_str, "%d %B %Y")
                player_info["date_of_birth"] = dob_datetime.strftime("%Y-%m-%d")
                break
            except ValueError:
                continue

    place_of_birth_regex = re.compile(r"born in ([A-Za-z\s,]+)")
    place_of_birth_match = place_of_birth_regex.search(text)
    if place_of_birth_match:
        player_info["place_of_birth"] = place_of_birth_match.group(1)

    if "date_of_birth" in player_info:
        player_info["age"] = calculate_age_from_dob(player_info["date_of_birth"])

    positions_regex = re.compile(r"is a ([A-Za-z\s,]+) footballer")
    positions_match = positions_regex.search(text)
    if positions_match:
        player_info["country_of_birth"] = positions_match.group(1)

    national_team_regex = re.compile(r"has represented the ([A-Za-z\s]+) national team")
    national_team_match = national_team_regex.search(text)
    if national_team_match:
        player_info["national_team"] = national_team_match.group(1)

    current_club_and_position_regex = re.compile(
        r"plays as a ([\w\s]+) for local club ([\w\s\.\-]+?)(?=\.)"
    )
    match = current_club_and_position_regex.search(text)
    if match:
        player_info["positions"] = match.group(1).strip()
        player_info["current_club"] = match.group(2).strip()

    return player_info


def remove_text_in_brackets(text):
    pattern = r"\s*\[.*?\]|\s*\([^)]*\)"
    cleaned_text = re.sub(pattern, "", text).strip()
    return cleaned_text


def clean_text(text):
    return re.sub("\[.*?\]", "", text).strip()


def extract_date_of_birth(dob_string):
    """
    Extracts the ISO format date of birth from the given string, handling both
    '(YYYY-MM-DD) DD Month YYYY (age XX)', 'DD Month YYYY', and 'Month DD, YYYY' formats.
    """
    # try ISO format
    iso_match = re.search(r"\((\d{4}-\d{2}-\d{2})\)", dob_string)
    if iso_match:
        return iso_match.group(1)

    # try 'DD Month YYYY' format
    common_format_match = re.search(r"\b(\d{1,2}\s+[A-Za-z]+\s+\d{4})\b", dob_string)
    if common_format_match:
        date_in_common_format = common_format_match.group(1)
        try:
            parsed_date = datetime.strptime(date_in_common_format, "%d %B %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            pass

    # try 'Month DD, YYYY' format
    alternative_format_match = re.search(
        r"\b([A-Za-z]+\s+\d{1,2},\s+\d{4})\b", dob_string
    )
    if alternative_format_match:
        date_in_alternative_format = alternative_format_match.group(1)
        try:
            parsed_date = datetime.strptime(date_in_alternative_format, "%B %d, %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return None


def extract_age(dob_string):
    """
    Extracts or calculates the age from the given string.
    First tries to extract explicitly mentioned age, if not available,
    calculates based on the date of birth.
    """

    # try to extract explicitly mentioned age first
    age_match = re.search(r"\(age\xa0?(\d+)\)", dob_string)
    if age_match:
        return int(age_match.group(1))

    # calculate based on date of birth
    dob = extract_date_of_birth(dob_string)
    if dob:
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        age = (
            today.year
            - dob_date.year
            - ((today.month, today.day) < (dob_date.month, dob_date.day))
        )
        return age


def extract_place_and_country(place_of_birth_string):
    """
    Splits the place of birth string into city and country if possible.
    If there's only one component and it's assumed to be a country, it returns None for the city.
    Example input: 'Thessaloniki, Greece' or 'Botswana'
    Returns: ('Thessaloniki', 'Greece') or (None, 'Botswana')
    """
    parts = place_of_birth_string.rsplit(",", maxsplit=1)

    if len(parts) == 2:
        place_of_birth = parts[0].strip()
        country_of_birth = parts[1].strip()
        return place_of_birth, country_of_birth
    else:
        country_of_birth = parts[0].strip()
        return None, country_of_birth


def find_international_career_header(soup):
    th_elements = soup.find_all("th")
    for th in th_elements:
        if "International career" in th.get_text():
            return th
    return None


def find_most_recent_national_team(soup):
    international_career_header = find_international_career_header(soup)

    if international_career_header:
        all_rows = international_career_header.find_parent("table").find_all("tr")
        header_index = all_rows.index(international_career_header.find_parent("tr"))
        career_rows = all_rows[header_index + 1 :]

        # Reverse iterate through the career rows to find the last valid team entry
        for row in reversed(career_rows):
            team_cell = row.find("td", class_="infobox-data")
            if team_cell and team_cell.find("a"):
                team_name = team_cell.find("a").text.strip()
                return team_name
            # if the row has the class 'infobox-below', it's considered a footer/note and skipped
            if row.get("class") == ["infobox-below"]:
                continue

    return None


def find_current_club_and_stats(soup):
    senior_career_header = soup.find("th", text="Senior career*")
    international_career_header = find_international_career_header(soup)

    if senior_career_header:
        senior_career_rows = []
        current_row = senior_career_header.find_parent("tr").find_next_sibling("tr")

        # iterate through the rows until reaching either the "International career" section or the end.
        while current_row:
            if (
                international_career_header
                and current_row == international_career_header.find_parent("tr")
            ):
                break
            senior_career_rows.append(current_row)
            current_row = current_row.find_next_sibling("tr")

        for row in reversed(senior_career_rows):
            year_cell = row.find("th", class_="infobox-label")
            if (
                year_cell
                and "–" in year_cell.text
                and year_cell.text.strip().endswith("–")
            ):
                club_info = {
                    "current_club": None,
                    "appearances_current_club": None,
                    "goals_current_club": None,
                }
                club_cell = row.find("td", class_="infobox-data")
                if club_cell and club_cell.find("a"):
                    club_info["current_club"] = club_cell.find("a").text.strip()
                stats_cells = row.find_all("td", class_="infobox-data")
                if len(stats_cells) >= 3:
                    club_info["appearances_current_club"] = stats_cells[1].text.strip()
                    club_info["goals_current_club"] = (
                        stats_cells[2].text.strip().strip("()")
                    )
                return club_info

    return {
        "current_club": None,
        "appearances_current_club": None,
        "goals_current_club": None,
    }


def is_football_player(soup):
    # check infobox for football related words
    infobox = soup.find("table", class_="infobox vcard")
    if infobox and any(
        keyword in infobox.text.lower()
        for keyword in ["football", "soccer", "midfielder", "forward", "defender"]
    ):
        return True

    # check categories for football related words
    categories = soup.find_all("div", class_="mw-normal-catlinks")
    if categories and any(
        "footballers" in category.text.lower() for category in categories
    ):
        return True

    return False


def scrape_player_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if is_football_player(soup):
        # dictionary to store all player info
        player_info = {
            "url": url,
            "name": None,
            "full_name": None,
            "date_of_birth": None,
            "age": int,
            "place_of_birth": None,
            "country_of_birth": None,
            "positions": None,
            "current_club": None,
            "national_team": None,
            "appearances_current_club": None,
            "goals_current_club": None,
            "scraping_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dead": False,
        }

        player_info["name"] = remove_text_in_brackets(soup.find("h1").text)

        infobox = soup.find("table", class_="infobox vcard")
        if infobox:
            for row in infobox.find_all("tr"):
                header = row.find("th")
                data = row.find("td")
                if header and data:
                    header_text = header.text.strip()
                    data_text = clean_text(data.text)

                    if "Full name" in header_text:
                        player_info["full_name"] = data_text
                    elif "Date of birth" in header_text:
                        player_info["date_of_birth"] = extract_date_of_birth(data_text)
                        player_info["age"] = extract_age(data_text)
                    elif "Place of birth" in header_text:
                        place_of_birth, country_of_birth = extract_place_and_country(
                            data_text
                        )
                        player_info["place_of_birth"] = place_of_birth
                        player_info["country_of_birth"] = country_of_birth
                    elif "Country" in header_text:
                        player_info["country_of_birth"] = data_text
                    elif "Position" in header_text:
                        player_info["positions"] = data_text
                    elif "Date of death" in header_text:
                        player_info["dead"] = True
        else:
            text_based_info = scrape_text_based_info(soup)
            player_info.update(text_based_info)

        player_info["national_team"] = find_most_recent_national_team(soup)
        current_club_info = find_current_club_and_stats(soup)
        player_info.update(current_club_info)

        return player_info

    else:
        pass
