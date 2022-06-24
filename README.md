# job-hunting
I was the Job Hunter who wrote this Hobby Project

# Purpose

Have you ever tried going through 20 job postings without being tempted to skim, missing out on opportunities you're qualified for because of your boredom or timidity? I knew if I could automate the selection of the minimum requirements section and the tokenization of each requirement I could train a predictive model that would both train me to be brutally honest about my own capabilities and direct me to apply for jobs that I would get a high chance of being interviewed for.

Originally I was just emailed a CSV of reqs from the government, but I have since adapted that to ingest lists of URLs taken from search results emailed to me from Indeed and Glassdoor. I use Conditional Random Fields to figure out which navigable html in the posting itself or in the email is the minimum requirements section and then tokenize the qualification sentences. Those child strings are then further tokenized with a special regex tokenizer that treats "C++", for instance, as its own token and then transformed into a Bag of Words and further, into a TF-IDF to highlight the importance of individual tokens. ("and" and "or", for instance, are not stop words in qualification strings, but very important distinctions.)

## Installation
Right now, <code>C:\Users\dev\Documents\Repositories\job-hunting</code> is where I'm keeping this, so you need to search for every instance of <code>C:\Users\dev</code> (in the .gitignore, jupyter_notebook_config.py, *.yml; and *.ps1; files) and figure out which needs to be replaced with the path to your home folder, and which needs <code>C:\Users\dev\Documents\Repositories\job-hunting</code> replaced with the path to this job-hunting folder you pulled or downloaded. If your os.sep isn't a backslash, you need to replace the backslashes in the rest of the path strings with what works on your OS.
