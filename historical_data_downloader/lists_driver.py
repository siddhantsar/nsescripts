"""
This module consists of 3 dunctions:
Nifty 50,
Nifty 100,
Nifty 500,
These are indices provided by National Stock Exchange, India.
"""
import os
import csv
import pickle
import requests
from bs4 import BeautifulSoup as bs


def download_data(filename, url):
    symbols_list = []
    response = requests.get(url).content.decode("utf-8")
    stocks_list = list(csv.reader(response.splitlines(), delimiter=","))

    for stocks in stocks_list[1:]:
        symbols_list.append(stocks[2])

    with open(filename + ".pickle", "wb") as file:
        pickle.dump(symbols_list, file)

    return symbols_list


def nifty_50(refresh):
    filename = "nifty_50"
    if refresh:
        nifty_50_list = download_data(
            filename, "https://www1.nseindia.com/content/indices/ind_nifty50list.csv"
        )
    elif not refresh and not os.path.exists(filename + ".pickle"):
        nifty_50_list = download_data(
            filename, "https://www1.nseindia.com/content/indices/ind_nifty50list.csv"
        )
    else:
        with open(filename + ".pickle", "rb") as file:
            nifty_50_list = pickle.load(file)

    return nifty_50_list


def nifty_100(refresh):
    filename = "nifty_100"
    if refresh:
        nifty_50_list = download_data(
            filename, "https://www1.nseindia.com/content/indices/ind_nifty100list.csv"
        )
    elif not refresh and not os.path.exists(filename + ".pickle"):
        nifty_50_list = download_data(
            filename, "https://www1.nseindia.com/content/indices/ind_nifty100list.csv"
        )
    else:
        with open(filename + ".pickle", "rb") as file:
            nifty_50_list = pickle.load(file)

    return nifty_50_list


def nifty_500(refresh):
    filename = "nifty_500"
    if refresh:
        nifty_50_list = download_data(
            filename, "https://www1.nseindia.com/content/indices/ind_nifty500list.csv"
        )
    elif not refresh and not os.path.exists(filename + ".pickle"):
        nifty_50_list = download_data(
            filename, "https://www1.nseindia.com/content/indices/ind_nifty500list.csv"
        )
    else:
        with open(filename + ".pickle", "rb") as file:
            nifty_50_list = pickle.load(file)

    return nifty_50_list
