from selenium import webdriver
from selenium.webdriver.common.by import By

chrome = webdriver.Chrome("./chromedriver")
chrome.get("https://th.jobsdb.com/th/search-jobs/python/1")

while True:
    if input("Get website text") == "q":
        chrome.quit()
        break
    words = chrome.find_element(By.TAG_NAME, "html").text.split()

    words_count = []
    for word in words:
        words_count.append([word,words.count(word)])

    words_count.sort(key=lambda x: x[1],reverse=True)
    words_count_no_dups = []
    words_count = [words_count_no_dups.append(x) for x in words_count if x not in words_count_no_dups]
    print(words_count_no_dups[:20])