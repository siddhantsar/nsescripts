import requests


def start_fetch():
    URL = "https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/foSecStockWatch.json"

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, fr",
    }
    raw_json = requests.get(URL, headers=header).json()
    processed_json = dict()

    processed_json["stats"] = {
        "total": (raw_json["noChg"] + raw_json["adv"] + raw_json["dec"]),
        "profit": raw_json["adv"],
        "loss": raw_json["dec"],
        "noChg": raw_json["noChg"],
    }
    stocks_list = []
    for row in raw_json["data"]:
        stocks_list.append(
            [
                row["symbol"],
                ("₹" + row["ltP"]),
                ("₹" + row["open"]),
                ("₹" + row["high"]),
                ("₹" + row["low"]),
                ("₹" + row["ptsC"]),
                row["per"],
                (row["trdVol"] + "L"),
            ]
        )

    processed_json["priceDict"] = stocks_list

    return processed_json
