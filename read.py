import requests
from bs4 import BeautifulSoup
import csv
import os

# TODO:
# from fake_useragent import UserAgent
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# ua=UserAgent()
# hdr = {'User-Agent': ua.random,
#       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#       'Accept-Encoding': 'none',
#       'Accept-Language': 'en-US,en;q=0.8',
#       'Connection': 'keep-alive'}

hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Create the 'read' folder if it doesn't exist
if not os.path.exists("read"):
    os.makedirs("read")

article_num = 0

with open("articles.csv", "r") as file:
    reader = csv.reader(file)
    # Skip the first row, which contains the column headers
    next(reader)
    # Iterate over each row in the CSV file
    for row in reader:
        url = row[0]
        page = requests.get(url, headers=hdr)
        soup = BeautifulSoup(page.content, "html.parser")

        # Find all the text elements on the page
        text_elements = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "strong", "em"])

        # Filter out elements that are inside navigation links or buttons
        text_elements = [element for element in text_elements if element.find_parent("a") is None and element.find_parent("button") is None]

        # Filter out elements that are inside navigation links or buttons
        text_elements = [element for element in text_elements if element.find_parent("a") is None and element.find_parent("button") is None]

        # Filter out elements that are inside header or footer
        text_elements = [element for element in text_elements if element.find_parents(["header", "footer","nav"]) == []]

        # Extract the text from each element
        article_text = " ".join([element.get_text() for element in text_elements])

        # Add a line break after every period
        article_text = article_text.replace(".", ".\n")

        # Write to a new .txt file in the 'read' folder
        filename = str(article_num) + ".txt"
        article_num += 1

        with open(os.path.join("read", filename), "w") as f:
            f.write(url + "\n")
            f.write(article_text)
