import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.cbssports.com/nfl/stats/player/receiving/nfl/regular/qualifiers/"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
table_rows = soup.select("table tr")

header_mapping = {
    'Player': 'Player Name',
    'GP': 'Games Played',
    'REC': 'Receptions',
    'YDS': 'Receiving Yards',
    'YDS/G': 'Receiving Yards per Game',
    'AVG': 'Average Yards per Reception',
    'LNG': 'Longest Reception',
    'TD': 'Receiving Touchdowns'
}

def map_header(header_text):
    clean_header = header_text.split('\n')[0].strip()
    return header_mapping.get(clean_header, clean_header)

# Adjust the headers to accommodate Player Name, Position, and Team
base_headers = [h.get_text() for h in table_rows[0].find_all('th')]
headers = ['Player Name', 'Position', 'Team'] + [map_header(h) for h in base_headers[1:]]

players_data = []
for row in table_rows[1:]:
    columns = row.find_all('td')
    
    player_name = columns[0].select_one(".CellPlayerName--long a").get_text().strip()
    position = columns[0].select_one(".CellPlayerName-position").get_text().strip()
    team = columns[0].select_one(".CellPlayerName-team").get_text().strip()

    data = [player_name, position, team] + [col.get_text().strip() for col in columns[1:]]
    players_data.append(data)

# Save to CSV
with open('receiving_stats.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(players_data)

print("Data saved to receiving_stats.csv")
