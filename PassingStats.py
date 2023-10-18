import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.cbssports.com/nfl/stats/player/passing/nfl/regular/qualifiers/"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
table_rows = soup.select("table tr")

# Create a mapping to adjust headers
header_mapping = {
    'Player\n                \n                                                        \n                            Player on team': "Player Name",
    'GP\n                            Games played': "Games Played",
    'ATT\n                            Pass Attempts': "Pass Attempts",
    'CMP\n                            Pass Completions': "Pass Completions",
    'PCT\n                            Completion Percentage': "Completion Percentage",
    'YDS\n                            Passing Yards': "Passing Yards",
    'YDS/G\n                            Passing Yards per Game': "Passing Yards per Game",
    'LNG\n                            Longest Completion': "Longest Pass",
    'TD\n                            Touchdown Passes': "Passing Touchdowns",
    'INT\n                            Interceptions Thrown': "Interceptions",
    'SCK\n                            Times Sacked': "Times Sacked",
    'YDSL\n                            Sack Yards Lost': "Yards Lost due to Sacks",
    'RATE\n                            Passer Rating': "Quarterback Rating"
}

# Map the original headers to the new ones
headers = [header_mapping[col.get_text().strip()] for col in table_rows[0].find_all('th')]

# Insert the Position and Team columns after Player Name
headers.insert(1, "Position")
headers.insert(2, "Team")

with open('passing_data.csv', 'w', newline='', encoding='utf-8') as file:
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

print("Data saved to passing_data.csv")
