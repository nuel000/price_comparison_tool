# task.py
import concurrent.futures
import subprocess
from scrappers.config import search_term

def run_scrapers(search_term):
    # Set the search term
    search_term = str(input('Enter Your Search Term: '))

    with open('config.py', 'w') as config_file:
        config_file.write(f'search_term = "{search_term}"')

    scripts = ['ebay.py', 'walmart.py']
    scraped_data = []

    def run_script(script):
        process = subprocess.run(['python', script], capture_output=True, text=True)
        output = process.stdout.strip()
        scraped_data.append(output)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_script, scripts)

    return scraped_data
