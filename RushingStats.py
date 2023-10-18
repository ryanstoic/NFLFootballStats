import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.cbssports.com/nfl/stats/player/rushing/nfl/regular/qualifiers/"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
table_rows = soup.select("table tr")

# Adjust headers
adjusted_headers = [
    "Player Name", "Position", "Team", "Games Played", "Rushing Attempts", "Rushing Yards",
    "Rushing Yards per Game", "Average Yards per Rush", "Rushing Touchdowns", "Longest Rush"
]

#Write to csv file
with open('rushing_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(adjusted_headers)

    for row in table_rows[1:]:
        columns = row.find_all('td')
        
        if columns:
            # Extract player's full name, had to differentiate between long and short name so used select_one
            name_element = columns[0].select_one('.CellPlayerName--long a')
            player_name = name_element.text.strip() if name_element else "N/A"

            position = columns[0].find('span', class_='CellPlayerName-position').text.strip()
            team = columns[0].find('span', class_='CellPlayerName-team').text.strip()

            # Create a new list with the extracted player data and the rest of the columns
            data = [player_name, position, team] + [col.get_text().strip() for col in columns[1:]]
            writer.writerow(data)

print("Data saved to rushing_data.csv")
