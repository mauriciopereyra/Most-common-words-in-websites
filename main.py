from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

# Import most common words in English
with open('common_words_english.csv', newline='') as f:
    reader = csv.reader(f)
    common_words_english = [word[0].strip() for word in list(reader)][:500]


chrome = webdriver.Chrome("./chromedriver")
chrome.get("https://th.jobsdb.com/th/search-jobs/python/1")

collected_words = []
while True:
    cmd = input("---Commands---\nEnter - Get website words\nS - Save\nQ - Quit\n")
    if cmd == "q":
        chrome.quit()
        break
    elif cmd == "":
        # Read all words from the website
        words = chrome.find_element(By.TAG_NAME, "html").text.split()
        words_count = []
        for word in words:
            words_count.append([word,words.count(word)])
        # Sort by most common words in the website
        words_count.sort(key=lambda x: x[1],reverse=True)
        # Remove duplicates
        words_count_no_dups = []
        [words_count_no_dups.append(x) for x in words_count if x not in words_count_no_dups]
        # Remove words from the most used words in English
        words_count = [word for word in words_count_no_dups if word[0].lower() not in common_words_english]
        # Get only top 20 words
        words_count = words_count[:20]
        collected_words += words_count
        print(words_count)
    elif cmd == "s":
        with open("saved_words.csv", "a") as f:
            writer = csv.writer(f)
            for row in collected_words:
                writer.writerow(row)
        collected_words = []


# import re

# s = re.sub('[^0-9a-zA-Z]+', '*', s)


