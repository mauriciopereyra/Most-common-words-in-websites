from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
import re

# Import most common words in English
with open('common_words_english.csv', newline='') as f:
    reader = csv.reader(f)
    common_words_english = [word[0].strip() for word in list(reader)][:500]

# Import words to ignore
with open('words_to_ignore.csv', newline='') as f:
    reader = csv.reader(f)
    words_to_ignore = [word[0].strip() for word in list(reader)][1:]

if os.name == 'nt':
    chrome = webdriver.Chrome("./chromedriver.exe")
else:
    chrome = webdriver.Chrome("./chromedriver")
chrome.get("https://th.jobsdb.com/th/search-jobs/python/1")

collected_words = []
tag = None
while True:
    if not tag:
        tag = input("Please type the tag you want to use for your next saved words -> ")
    print("Current tag is \"{}\"".format(tag))

    cmd = input("---Commands---\nG - Get website words\nI - Ignore words\nS - Save\nQ - Quit\n")
    if cmd.lower() == "q":
        chrome.quit()
        print('\n--- Thanks! ---\n')
        break
    elif cmd.lower() == "" or cmd.lower() == "g":
        # Read all words from the website
        words = chrome.find_element(By.TAG_NAME, "html").text.split()
        words_count = []
        for word in words:
            words_count.append([word,words.count(word)])
        # Sort by most common words in the website
        words_count.sort(key=lambda x: x[1],reverse=True)
        # Remove words from the most used words in English
        words_count = [word for word in words_count if (word[0].lower() not in common_words_english and word[0].lower() not in words_to_ignore)]
        # Remove not alphabetic characters
        words_count = [[(re.sub('[^a-zA-Z]+', '', word[0])),word[1]] for word in words_count]
        # Remove empty words
        words_count = [word for word in words_count if len(word[0]) > 2]
        # Remove duplicates
        words_count_no_dups = []
        [words_count_no_dups.append([x[0].lower(),x[1]]) for x in words_count if [x[0].lower(),x[1]] not in words_count_no_dups]
        # Get only top 20 words
        words_count = words_count_no_dups[:20]
        collected_words += words_count
        print('\n--- Top words ---\n')
        print(words_count)
    elif cmd.lower() == "s":
        # Save collected words to a csv
        with open("saved_words.csv", "a") as f:
            writer = csv.writer(f)
            for row in collected_words:
                writer.writerow(row+[tag])
        collected_words = []
        print('\n--- Saved! ---')
    elif cmd.lower() == 'i':
        words = [word.strip() for word in input("What words to ignore?\ni.e. word1, word2, word3\n-> ").split(',')]
        words_to_ignore += [word for word in words if word not in words_to_ignore]
        
        # Save words to ignore to a csv
        with open("words_to_ignore.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['Word','Tag'])
            for word in words_to_ignore:
                writer.writerow([word,tag])

        print("--- Ignoring {} ---".format(words))

    elif cmd.lower() == 't':
        tag = input("Please type the tag you want to use for your next saved words -> ")
    else:
        print("Command incorrect")
    print('\n')


