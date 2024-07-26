import pandas as pd
import time
import re
from googlesearch import search
from bs4 import BeautifulSoup
import requests

#loading excel file
input_file = 'NBFCsandARCs10012023 (5).XLSX'
output_file = 'NBFC_Websites_Output.xlsx'
df = pd.read_excel(input_file)

def is_official_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.lower() if soup.title else ''
        
        # Checking for common indicators of an official website
        official_keywords = ['official', 'nbfc', 'company', 'finance', 'ltd', 'limited', 'pvt']
        
        # Validating based on URL or title
        if any(keyword in url.lower() for keyword in official_keywords) or any(keyword in title for keyword in official_keywords):
            return True
    except Exception as e:
        print(f"Error validating URL {url}: {e}")
    return False

def find_official_website(nbfc_name):
    query = f"{nbfc_name} official site"
    try:
        search_results = search(query, num=5, stop=5)
        
        for result in search_results:
            if is_official_website(result):
                return result
    except Exception as e:
        print(f"Error searching for {nbfc_name}: {e}")
    
    return 'Not Found'

# Adding a new column for the official website
df['Official Website'] = ''

# Processing each NBFC in the dataframe
for index, row in df.iterrows():
    nbfc_name = row['NBFC Name']
    print(f"Searching for: {nbfc_name}")
    official_website = find_official_website(nbfc_name)
    df.at[index, 'Official Website'] = official_website
    
    # Wait a few seconds to avoid detection
    time.sleep(5)

# Save the results to a new Excel file
df.to_excel(output_file, index=False)

print(f"Output saved to {output_file}")
