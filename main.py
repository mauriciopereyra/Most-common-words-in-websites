from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
import re

# Import most common words in English
# Dataset downloaded from https://www.kaggle.com/datasets/rtatman/english-word-frequency
with open('common_words_english.csv', newline='') as f:
    reader = csv.reader(f)
    common_words_english = [word[0].strip() for word in list(reader)][:500]

# Import words to ignore
with open('words_to_ignore.csv', newline='') as f:
    reader = csv.reader(f)
    words_to_ignore = [word[0].strip() for word in list(reader)][1:]

# Import saved words
with open('saved_words.csv', newline='') as f:
    reader = csv.reader(f)
    saved_words = [word for word in list(reader)][1:]    

if os.name == 'nt':
    chrome = webdriver.Chrome("./chromedriver.exe")
else:
    chrome = webdriver.Chrome("./chromedriver")
chrome.get("https://th.jobsdb.com/th/en/job/data-scientist-advanced-analytics-300003002681842")

tag = None
words_count = []
while True:
    if not tag:
        tag = input("Please type the tag you want to use for your next saved words -> ")
    print("Current tag is \"{}\"".format(tag))

    cmd = input("---Commands---\nG - Get website words\nT - Change tag\nI - Ignore words\nS - Save\nQ - Quit\n")
    if cmd.lower() == "q":
        chrome.quit()
        print('\n--- Thanks! ---\n')
        break
    elif cmd.lower() == "" or cmd.lower() == "g":
        # Read all words from the website
        words = chrome.find_element(By.TAG_NAME, "html").get_attribute("innerText").split()
        # Remove not alphabetic characters
        words = [(re.sub('[^a-zA-Z]+', '', word)) for word in words]
        # Remove empty words
        words = [word for word in words if len(word) > 2]
        # Remove words from the most used words in English
        words = [word.strip() for word in words if (not word.lower().strip() in common_words_english and not word.lower().strip() in words_to_ignore)]
        # Count words occurrences
        words_count = []
        for word in words:
            words_count.append([word,words.count(word)])
        # Remove duplicates
        words_no_dups = []
        [words_no_dups.append([x[0].lower(),x[1]]) for x in words_count if [x[0].lower(),x[1]] not in words_no_dups]
        # Sort by most common words in the website
        words_no_dups.sort(key=lambda x: x[1],reverse=True)
        # Get only top 20 words
        words_count = words_no_dups[:20]
        print('\n--- Top words ---\n')
        print(words_count)
    elif cmd.lower() == "s":
        # Save collected words to a csv and sum occurrences if already saved the same word and tag 
        for new_word in words_count:
            duplicated = False
            print(saved_words)
            for saved_word in saved_words:
                print(saved_word,"saved")
                print(new_word,"new")
                if saved_word[0] == new_word[0].lower() and saved_word[2].lower() == tag.lower():
                    saved_word[1] = int(saved_word[1]) + int(new_word[1])
                    duplicated = True
                    break   

            if not duplicated:
                saved_words.append(new_word+[tag])

        with open("saved_words.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['Word','Occurrences','Tag'])
            for row in saved_words:
                writer.writerow(row[:2]+[tag])
        words_count = []
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
        print(words_to_ignore)

    elif cmd.lower() == 't':
        tag = input("Please type the tag you want to use for your next saved words -> ")
    else:
        print("Command incorrect")
    print('\n')
