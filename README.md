# Most common words in websites
Python script using Selenium to check what are the most common words of a website. 

It ignores the most common words of English like "of", "and", "the", etc. 

It also allows to add more words to ignore.

It uses tags to group the most common words you save from different topics.

## Instructions 
1. Run main.py

2. A chrome browser will open. Browse the website that you want to analyze for its top words

3. In the command line, type the tag that you want to use for the words you save next

4. Type G and press enter to get most repeated words in the website you opened
You will see a list of the top 20 most common words

5. If you want to ignore some of those words, type I and press enter. Then type the words that you want to ignore.

6. You can type G and enter again to see the new list, after removing the words you want to ignore. These words will be saved in words_to_ignore.csv

7. Type S and press enter to save the list to saved_words.csv

8. Browse another website and repeat from step 4

## All commands
G - Get website words

T - Change tag

I - Ignore words

S - Save

Q - Quit
