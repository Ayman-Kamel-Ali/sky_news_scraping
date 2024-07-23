import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

# URL of the Sky News homepage
base_url = "https://news.sky.com/"

# Send a GET request to the webpage
response = requests.get(base_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    sky_news = {}
    titles_list = []
    content_list = []
    link_list = []

    # Find all sections with news content
    sections = soup.find_all('section', class_="wrap gap-400")

    for section in sections:
        title = section.find('span', class_="ui-section-header-title").get_text(strip=True)
        titles_list.append(title)
        cels = section.find_all('div', class_='grid-cell')
        contents = []
        links = []
        for cel in cels:
            content = cel.find('div', class_='ui-story-headline').get_text(strip=True)
            link_tag = cel.find('div', class_='ui-story-headline').find('a')
            if link_tag:
                link = urljoin(base_url, link_tag.get('href'))
                links.append(link)
            contents.append(content)
        content_list.append(contents)
        link_list.append(links)

    # Create a DataFrame
    data = {'Title': titles_list, 'Content': content_list, 'Link': link_list}
    df = pd.DataFrame(data)

    print(df)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
