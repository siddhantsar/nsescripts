import os
import csv
import json
import datetime as dt
from pathlib import Path
import requests


HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, fr",
}


def create_files(base_path):
    directory = Path(str(base_path) + "/" + "csv_files")

    if not os.path.exists(directory):
        os.mkdir("csv_files")

    gainer_file_path = Path(str(directory) + "/" + str(dt.date.today()) + "_g.csv")

    if not os.path.exists(gainer_file_path):
        file = open(gainer_file_path, "w")
        file.close()

    loser_file_path = Path(str(directory) + "/" + str(dt.date.today()) + "_l.csv")

    if not os.path.exists(loser_file_path):
        file = open(loser_file_path, "w")
        file.close()


def write_csv(json_data, file):
    file.writerow(json_data["data"][0].keys())

    for row in json_data["data"]:
        file.writerow(row.values())


def top_gainer(filepath):
    top_gainer_url = "http://www1.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json"
    result = requests.get(top_gainer_url, headers=HEADER)
    json_data = json.loads(result.text)

    output_raw = open(filepath + str(dt.date.today()) + "_g.csv", "w")
    output_file = csv.writer(output_raw)
    write_csv(json_data, output_file)


def top_loser(filepath):
    top_loser_url = "http://www1.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json"
    result = requests.get(top_loser_url, headers=HEADER)
    json_data = json.loads(result.text)

    output_raw = open(filepath + str(dt.date.today()) + "_l.csv", "w")
    output_file = csv.writer(output_raw)
    write_csv(json_data, output_file)


if __name__ == "__main__":
    BASE_PATH = Path(os.getcwd())
    create_files(BASE_PATH)
    DIRECTORY_BASE_PATH = str(BASE_PATH) + "/csv_files/"

    print("National Stock Exchange Top Gainer/Loser CSV Downloader")
    option = input(
        "Please select your option:\n1. Download Top Gainer\n2. Download Top Loser\n3. Download Both\n\nYour choice: "
    )

    if option == "1":
        top_gainer(DIRECTORY_BASE_PATH)
        print("Top Gainer File Saved")
    elif option == "2":
        top_loser(DIRECTORY_BASE_PATH)
        print("Top Loser File Saved")
    elif option == "3":
        top_gainer(DIRECTORY_BASE_PATH)
        top_loser(DIRECTORY_BASE_PATH)
        print("Both Files Saved")
    else:
        print("Try Again!")
