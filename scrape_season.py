from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import argparse
import time
import csv
from io import StringIO

def dump_rendered_page(team_id, year=2024, sport="cross-country" ):
    race_dict = {}
    # Format the URL with the given team ID, year, and sport
    url = f'https://www.athletic.net/CrossCountry/Results/Season.aspx?SchoolID={team_id}&S={year}'
    # Set up Selenium WebDriver (change path if needed)
    service = Service( )  # Replace with the actual path to your WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for faster execution (no browser UI)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Load the page and wait for it to render
    driver.get(url)
    time.sleep(2)  # Wait to ensure the page fully loads (adjust as necessary)
    
    # Get the rendered HTML and close the browser
    rendered_html = driver.page_source
    driver.quit()
    
    # Parse with BeautifulSoup and print the content
    soup = BeautifulSoup(rendered_html, 'html.parser')

    # for child in soup.descendants:
    #     if child.name:
  
    #         print(child.name, ":", child.get_text())

    # print(soup.prettify())  # Dump the HTML for inspection

    table = soup.find('table', class_='pull-right-sm')
    

    table_id = table.get('id', 'No ID')
    table_class = ' '.join(table.get('class', [])) if table.get('class') else 'No Class'
    
    # print(f"  ID: {table_id}")
    # print(f"  Class: {table_class}")

    # Extract and print the table rows
    rows = table.find_all('td')
    # Create a dictionary from the table data
    race_distances = {}
    for row in rows:
        sub = row.find('sub')  # Find the <sub> element
        if sub:
            key = sub.text.strip()  # Get the key
            value = row.text.replace(sub.text, '').strip()  # Remove the <sub> text from the value
            race_distances[key] = value

    # print(race_distances)
    
    tables = soup.find_all('table', id='MeetList')
    # Iterate over each table
    for i, table in enumerate(tables, start=1):
        # Get the id and class attributes
        table_id = table.get('id', 'No ID')
        table_class = ' '.join(table.get('class', [])) if table.get('class') else 'No Class'
        
        # print(f"Table {i}:")
        # print(f"  ID: {table_id}")
        # print(f"  Class: {table_class}")
        
        # Extract and print the table rows
        rows = table.find_all('tr')
        for row in rows:
            # Extract all cell data
            cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            print(','.join(cells))  # Print tab-separated row
            if len(cells) > 1:
                race_dict[cells[0]] = cells[1]
        print("-" * 40)
        # print(race_dict)


    tables = soup.find_all('table', class_='table-responsive small DataTable')

    for race in race_dict:


        for table in tables:
            # Find all rows

            rows = table.find_all('tr')
            
            # Determine the column index for the "Date" header
            # Determine the column index for the header containing "Date"
            headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]
            date_col_index = next((i for i, header in enumerate(headers) if race in header), None)
        
            if date_col_index is None:
                print(f'No column containing {race} found in table.')
                continue
        
            
            # print(f"Rows matching date {race}:")
            
            # Iterate over the remaining rows
            for row in rows[1:]:  # Skip the header row
                race_dist = [0] * 24
                for i, td in enumerate(row.find_all('td')):
                    subscript = td.find('span', class_='subscript')
                    if subscript and subscript.text.isdigit():
                        race_dist[i] = int(subscript.text)  
        

                cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                # print(f'race_dist: {race_dist}')
                # print(f'date_col_index: {date_col_index}') 
                # print(f'race_distances: {race_distances.items()}')  
                # Skip rows with no data in the date column or missing data
                if len(cells) > date_col_index and cells[date_col_index]:
                    print(f"{race} {year},{cells[0]},{cells[1]},00:{cells[date_col_index]},{race_dict[race]},{list(race_distances.items())[race_dist[date_col_index]-1][1]}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Dump rendered page content from Athletic.net")
    parser.add_argument("--team_id", type=int, help="Team ID of the team on Athletic.net")
    parser.add_argument("--year", type=int, default=2024, help="Year for the team data")
    parser.add_argument("--sport", type=str, default="cross-country", help="Sport type (e.g., cross-country, track-and-field)")

    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Call the function to dump the rendered page content
    dump_rendered_page(args.team_id, args.year, args.sport)

