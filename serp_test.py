# did this in replit instead
# wrote it out in serp.json
# https://replit.com/@steven4354/CreepySlimString#serp.json

# get the articles from serp.json

import json
import csv

with open('serp.json') as f:
    data = json.load(f)

    # iterate through data["organic_results"]
    for result in data["organic_results"]:
        # write the url to a csv file
        with open('articles.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([result["link"]])
