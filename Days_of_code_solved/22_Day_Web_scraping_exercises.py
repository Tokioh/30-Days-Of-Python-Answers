import requests
from bs4 import BeautifulSoup
import json
import os

#####################################################################################

print('\nExercise number 1:')

'''Exercise number 1 // Scrape the following website and store the data 
as json file(url = 'http://www.bu.edu/president/boston-university-facts-stats/').'''

# URL to scrape
url1 = 'http://www.bu.edu/president/boston-university-facts-stats/'

try:
    # Lets use the requests get method to fetch the data from url
    response = requests.get(url1)
    response.raise_for_status()  # Throws an error if the status code is not 200 (OK)
    print("Request was successful!")

except requests.exceptions.RequestException as e:
    print(f"Error getting data: {e}")

content = response.content # we get all the content from the website
soup = BeautifulSoup(content, 'html.parser') # beautiful soup will give a chance to parse
#print(soup.title) # <title>UCI Machine Learning Repository: Data Sets</title>
#print(soup.title.get_text()) # UCI Machine Learning Repository: Data Sets
#print(soup.body) # gives the whole page on the website
#print(response.status_code) # Should be 200 if success


# Basic scraping - get all headings and corresponding text
data = {}

for section in soup.find_all(['h2', 'h3', 'h4']):
    title = section.get_text(strip=True)
    content_tag = section.find_next_sibling()
    if content_tag and content_tag.name in ['p', 'ul']:
        if content_tag.name == 'p':
            content_text = content_tag.get_text(strip=True)
        elif content_tag.name == 'ul':
            content_text = [li.get_text(strip=True) for li in content_tag.find_all('li')]
        data[title] = content_text


# Save as JSON
with open('data/bu_facts_stats.json', 'w', encoding='utf-8') as f: # We need to specify the output address.
    json.dump(data, f, ensure_ascii=False, indent=4)

print("\n✅ Data scraped and saved to 'bu_facts_stats.json'\n")

# Open Saved JSON
with open('data/bu_facts_stats.json', 'r', encoding='utf-8') as f:
    data = json.load(f)  # NO uses json.loads(f)
    print(data)





#####################################################################################

print('\nExercise number 2:')

'''Exercise number 2 // Extract the table in this url (https://archive.ics.uci.edu/ml/datasets.php) 
# The link is broken so I will use it (https://www.worldometers.info/world-population/population-by-country/)
and change it to a json file.'''

url2 = 'https://www.worldometers.info/world-population/population-by-country/'

try:
    response = requests.get(url2)
    response.raise_for_status()
    print("Request was successful!")

except requests.exceptions.RequestException as e:
    print(f"Error getting data: {e}")

content = response.content
soup = BeautifulSoup(content, 'html.parser')

# Get the table
#If you want to select that table with BeautifulSoup, you must do it by its class, because this specific table does not have an id.
table = soup.find('table', {'class': 'datatable'}) 

if table is not None:
    rows = table.find_all('tr')
else:
    print("❌ No tables found on the page.")

# Get headers
headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]


# Get data rows
data_list = []
for row in rows[1:]:
    cells = row.find_all('td')
    if len(cells) == len(headers):
        values = [cell.get_text(strip=True) for cell in cells] # values store the data in format ['1', 'India', '1,463,865,525', '0.89%', '12,929,734', '492', '2,973,190', '−495,753', '1.94', '28.8', '37.1%', '17.78%']
        row_dict = dict(zip(headers, values))
        data_list.append(row_dict)


# Make sure output folder exists
os.makedirs('../data', exist_ok=True)

# Save as JSON
output_file = 'data/world_population.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)

print(f"\n✅ Data saved in {output_file}")

with open('data/world_population.json', 'r', encoding='utf-8') as f:
    data = json.load(f)  # NO uses json.loads(f)
    print('\nPrint the first row as an example:')
    print(f'{data[0]}')




            
#####################################################################################

print('\nExercise number 3:')

'''Exercise number 3 // Scrape the presidents table and store the data as 
json(https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States).
The table is not very structured and the scrapping may take very long time.'''

url3 = 'https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States'

try:
    response = requests.get(url3)
    response.raise_for_status()
    print('Request was successful')

except requests.exceptions.RequestException as e:
    print(f'Error getting data: {e}')

content = response.content
soup = BeautifulSoup(content, 'html.parser')

# Get the table
table = soup.find('table', {'class': 'wikitable'})

if table is not None:
    rows = table.find_all('tr')[1:] # We use the data in the table from position 1 to avoid taking the headers
else:
    print("❌ No tables found on the page.")

# Get Header
headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]

# Get data rows
data_list = []

# The number of data contained in the row  is irregular, so we use the structure of a dictionary to store them.
for row in table.find_all('tr')[1:]:
    cells = row.find_all(['th', 'td'])


    #If the row does not contain any cells (<td> or <th>), skip it and move on to the next one.
    if not cells:
        continue

    # We extract the data conditionally
    number = cells[0].get_text(strip=True) if cells[0].name == 'th' else ''
    image = cells[1].find('img')['src'] if len(cells) > 1 and cells[1].find('img') else ''
    name = cells[2].get_text(strip=True) if len(cells) > 2 else ''
    term = cells[3].get_text(strip=True) if len(cells) > 3 else ''
    party = cells[5].get_text(strip=True) if len(cells) > 5 else ''
    elections = cells[6].get_text(strip=True) if len(cells) > 6 else ''
    vps = cells[7].get_text(strip=True) if len(cells) > 7 else ''

    data_list.append({
        'number': number,
        'image_url': f"https:{image}" if image else '',
        'name': name,
        'term': term,
        'party': party,
        'elections': elections,
        'vice_presidents': vps
    })


# Save as JSON
output_file = 'data/us_presidents.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)

print(f"\n✅ Data saved in {output_file}")

with open('data/us_presidents.json', 'r', encoding='utf-8') as f:
    data_list = json.load(f)  # NO uses json.loads(f)
    print('\nPrint the first row as an example:')
    print(f'{data_list[0]}')
