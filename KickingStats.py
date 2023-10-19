import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.cbssports.com/nfl/stats/player/kicking/nfl/regular/qualifiers/"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
table_rows = soup.select("table tr")

# Create a mapping to adjust headers
header_mapping = {
    'Player\n                \n                                                        \n                            Player on team': "Player Name",
    'GP\n                            Games played': "Games Played",
    'FGM-A\n                            Field Goals Made - Field Goals Attempted': "FGM-A",
    'FG%\n                            Field Goal Percentage': "FG%",
    'LNG\n                            Longest field goal in terms of yards by a kicker': "LNG",
    '1-19\n                            Field Goals 1-19 Yards (Made - Attempted)': "1-19",
    '20-29\n                            Field Goals 20-29 Yards (Made - Attempted)': "20-29",
    '30-39\n                            Field Goals 30-39 Yards (Made - Attempted)': "30-39",
    '40-49\n                            Field Goals 40-49 Yards (Made - Attempted)': "40-49",
    '50+\n                            Field Goals 50+ Yards (Made - Attempted)': "50+",
    'XPM-A\n                            Extra Points Made - Extra Points Attempted': "XPM-A",
    'XP%\n                            Extra Point Percentage': "XP%",
    'PTS\n                            Kicking Points': "PTS"
}

# Map the original headers to the new ones
headers = [header_mapping[col.get_text().strip()] for col in table_rows[0].find_all('th')]

# Insert the Position and Team columns after Player Name
headers.insert(1, "Position")
headers.insert(2, "Team")

with open('kicking_stats.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    for row in table_rows[1:]:
        columns = row.find_all('td')
        
        if columns:
            # Extract player's full name
            name_element = columns[0].select_one('.CellPlayerName--long a')
            player_name = name_element.text.strip() if name_element else "N/A"

            position = columns[0].find('span', class_='CellPlayerName-position').text.strip()
            team = columns[0].find('span', class_='CellPlayerName-team').text.strip()

            # Create a new list with the extracted player data and the rest of the columns
            data = [player_name, position, team] + [col.get_text().strip() for col in columns[1:]]
            writer.writerow(data)

print("Data saved to kicking_stats.csv")
