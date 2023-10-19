import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.cbssports.com/nfl/stats/player/defense/nfl/regular/qualifiers/"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# Construct a list of headers based on the table structure
headers = ["Player Name", "Position", "Team", "Games Played", "Solo Tackles", "Assisted Tackles", 
           "Total Tackles", "Interceptions", "Interception Yards", "Longest Interception",
           "Interception Touchdowns", "Fumbles", "Fumbles Recovered", "Fumble Touchdowns",
           "Sacks", "Passes Defended", "Safeties"]

with open('defense_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    for row in soup.select("table tbody tr"):
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

print("Data saved to defense_data.csv")
