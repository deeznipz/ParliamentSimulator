"""
MPscrape.py
A script to scrape MP transcripts from parliament.nz
"""

import re
import requests
from requests.exceptions import ReadTimeout
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import csv
import nltk
from unidecode import unidecode
nltk.download('punkt')

MP = "Seymour" #Member of Parliament's last name
BASE_URL = 'https://www.parliament.nz/en/pb/hansard-debates/rhr/search?criteria.Keyword=&criteria.ParliamentNumber=-1&criteria.Timeframe=&criteria.DateFrom=&criteria.DateTo=&parliamentStartDate=&parliamentEndDate=&criteria.Mp=David+Seymour&criteria.Portfolio=' #URL from Hansard Report search page with your search parameters

TXT_PATH = f'C:\\Users\\deezn\\Desktop\\py\\SCRAPERS\\{MP}script.txt'
CLEAN_TXT_PATH = f'C:\\Users\\deezn\\Desktop\\py\\SCRAPERS\\{MP}clean.txt'
CSV_PATH = f'C:\\Users\\deezn\\Desktop\\py\\SCRAPERS\\{MP}script.csv'
CLEAN_CSV_PATH = f'C:\\Users\\deezn\\Desktop\\py\\SCRAPERS\\{MP}clean.csv'




def get_transcript_urls(url):
    """
    Get the URLs of the transcripts.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=5)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    base = "https://www.parliament.nz"
    transcript_urls = set()
    for link in links:
        href = link.get('href', '')
        if href.startswith('/en/pb/hansard-debates/rhr/document/HansS'):
            full_url = base + href
            transcript_urls.add(full_url)
    return list(transcript_urls)

def scrape_transcript(transcript_url):
    """
    Scrape the transcript from the given URL.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(transcript_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    speeches = set()

    for tag in soup.find_all('strong'):
        if unidecode(MP.lower()) in unidecode(tag.get_text().lower()):
            next_node = tag.next_sibling
            while next_node and isinstance(next_node, NavigableString):
                speech_text = next_node.strip().lstrip(": ")
                speeches.add(speech_text)
                print(f"FOUND: {speech_text[0:20]} ({len(speeches)})")
                next_node = next_node.next_sibling
                if next_node and next_node.name == 'strong':
                    print("FOUND NEXT SPEAKER - BREAK EXTRACTION")
                    break

    return speeches

def clean_text(text_content):
    cleaned_text = []
    for line in text_content.split('\n'):  # Split the text into lines
        line = re.sub('ö', 'o', line)  # Replace 'ö' with 'o' using regular expression
        cleaned_line = ''.join(ch for ch in line if ch.isalpha() or ch.isspace())  # Keep only alphabetic and space characters
        cleaned_text.append(cleaned_line.lower())  # Convert to lowercase and add to the list
    return '\n'.join(cleaned_text)  # Join the lines back together with line breaks


def main():
    transcript_urls = get_transcript_urls(BASE_URL)

    print(f"""
          HANSARD REPORT SEARCH BASE URL:
          {BASE_URL}""")
    print(f"""
          TOTAL UNIQUE TRANSCRIPTS: {len(transcript_urls)}
    """)

    scraped_count = 0
    all_speeches = set()
    unsuccesful = []
    for url in transcript_urls:
        speeches = scrape_transcript(url)
        all_speeches.update(speeches)
        scraped_count += 1
        if len(speeches) > 0:
            print(f"""URL END: {url[-50:]}
                  SCRAPE SUCCESSFUL ({scraped_count}/{len(transcript_urls)})
                  """)
        else:
            unsuccesful.append(url)
            print(f"""URL END: {url[-50:]})
                  SCRAPE UNSUCCESSFUL ({scraped_count}/{len(transcript_urls)})
                  """)

    with open(TXT_PATH, 'w', encoding='utf-8') as file:
        for speech in all_speeches:
            file.write(speech + '\n')

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for speech in all_speeches:
            writer.writerow([speech])

    with open(TXT_PATH, 'r', encoding='utf-8') as file:
        text_content = file.read()

    cleaned_text = clean_text(text_content)

    with open(CLEAN_TXT_PATH, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    with open(CLEAN_TXT_PATH, 'r', encoding='utf-8') as txt_file:
        with open(CLEAN_CSV_PATH, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            for line in txt_file:
                writer.writerow([line.strip()]) 
    
    word_count = 0
    with open(CLEAN_TXT_PATH, 'r', encoding='utf-8') as file:
         for line in file:
            words = line.split()
            word_count += len(words)

    print(f"TEXT: {TXT_PATH}")
    print(f"CLEAN TEXT: {CLEAN_TXT_PATH}")
    print(f"CSV {CSV_PATH}")
    print(f"CLEAN CSV {CLEAN_CSV_PATH}")
    speech_hrs = round(word_count/140/60, 2)
    print(f"""
          WORDCOUNT: {word_count} (~{speech_hrs} hours of speech)""")
            
    if len(unsuccesful) > 0:
        print("Unsuccesful scrapes:")
        for url in unsuccesful:
            print(url)



if __name__ == "__main__":
    main()
