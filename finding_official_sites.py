import pandas as pd
import time
import re
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Loading Excel file
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

def process_nbfc(index, nbfc_name):
    print(f"Searching for: {nbfc_name}")
    official_website = find_official_website(nbfc_name)
    return index, official_website

# Adding a new column for the official website
df['Official Website'] = ''

# Start timing
start_time = time.time()

# Using ThreadPoolExecutor for multithreading
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_nbfc, index, row['NBFC Name']) for index, row in df.iterrows()]

    for future in as_completed(futures):
        index, official_website = future.result()
        df.at[index, 'Official Website'] = official_website
        time.sleep(1)  # Adjust sleep to avoid detection; it will be distributed among threads

# End timing
end_time = time.time()
total_time = end_time - start_time

# Save the results to a new Excel file
df.to_excel(output_file, index=False)

print(f"Output saved to {output_file}")
print(f"Total time taken: {total_time:.2f} seconds")





