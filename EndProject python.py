import pymongo
import requests
import json
import csv
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["jokesdatabase"]
table = db["numjokes"]


# this function getting random jokes from the joke api
def get_a_jokes(num_of_jokes):
    url = "https://official-joke-api.appspot.com/random_joke"

    jokes = []
    for i in range(num_of_jokes):
        response = requests.request("GET", url)
        currnet_joke = json.loads(response.text)
        jokes.append(currnet_joke)

    return jokes


# this function saves the jokes to mongodb and removes the ID field
def save_to_mongodb(jokes):
    for joke in jokes:
        joke.pop('id')

    table.insert_many(jokes)


# this function reads from mongodb all the jokes and returns them
def read_from_mongodb():
    res = table.find()
    rows = []
    for row in res:
        rows.append(row)
    return rows


# this function gets list of jokes and saves them to a csv file
# and adds 'setup_length' and 'punchline_length'
def to_csv(jokes):
    for joke in jokes:
        joke['setup_length'] = len(joke['setup'])
        joke['punchline_length'] = len(joke['punchline'])

    # gets array of keys from the first joke
    # because all jokes have the same keys
    fields = jokes[0].keys()

    with open('jokes.csv', 'w', encoding='UTF8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(jokes)


def get_stats(jokes_csv):
    pd.value_counts(jokes_csv['type']).plot.bar()
    plt.show()
    print(tabulate(jokes_csv, headers='firstrow', showindex='always',tablefmt='fancy_grid'))


def main():
    # get how many jokes the user wants
    num_of_jokes = int(input("Please enter the number of jokes:"))

    if num_of_jokes <= 0:
        print('You must request at least one joke')
        return

    jokes = get_a_jokes(num_of_jokes)
    save_to_mongodb(jokes)
    rows = read_from_mongodb()
    to_csv(rows)

    # reads the jokes csv
    jokes_csv = pd.read_csv("jokes.csv")

    get_stats(jokes_csv)


if __name__ == '__main__':
    main()




