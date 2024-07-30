import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_stats_table(url):
    # Send a GET request to the website
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the webpage content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with the attribute label="Stats Table"
    table = soup.find('table')

    if table is None:
        raise ValueError("No table with the label 'Stats Table' found.")

    # Extract table headers
    headers = [th.find('abbr').get_text(strip=True) for th in table.find('thead').find_all('th')]

    # Extract table rows
    tbody = table.find('tbody')
    rows = []
    for tr in tbody.find_all('tr'):
        name = tr.find('a', class_="bui-link")['aria-label']
        data = [name] + [x.get_text() for x in tr.find_all('td')]
        rows.append(data)
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(rows, columns=headers)
    return df

dfs = {}

for year in range(1973, 2025):
    # URL of the website containing the table with label="Stats Table"
    url = f'https://www.mlb.com/stats/{year}?playerPool=QUALIFIED&position=DH'
    print(year)
    # Fetch the table and display it
    try:
        stats_df = fetch_stats_table(url)
        stats_df.insert(len(stats_df.columns), "year", year)
        dfs[year] = stats_df
    except Exception as e:
        print(e)

pd.concat(dfs.values()).to_csv('ALL_DH_stats.csv')