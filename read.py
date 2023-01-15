import requests
from bs4 import BeautifulSoup
import csv
import os

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
        page = requests.get(url)
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
