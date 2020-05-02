"""
Selenium based Python script to download historical stocks data
    from National Stock Exchange, India.
This script should only be used for personal/educational purpose.


To facilitate faster response time, this script do not validate the
stock symbol dynamically from National Stock Exchange, India.
Please use correct stock symbol provided by National Stock Exchange
only for accurate result and to avoid script failure.
"""
import os
import time
import datetime
from pathlib import Path
from time import time as timer
from selenium import webdriver as wd
from selenium.webdriver.support.ui import Select
import stocks_lists


def create_directory(base_path):
    """
    Method creates directory with date to keep data feasible and clean.
    """
    csv_files_directory_path = Path(str(base_path) + "/csv_files")
    if not os.path.exists(csv_files_directory_path):
        os.mkdir(csv_files_directory_path)
    directory_path = Path(base_path + "/csv_files/" + str(datetime.date.today()))
    if os.path.exists(directory_path):
        print("Directory already exists.")
    else:
        os.mkdir(directory_path)
    return str(directory_path)


def create_driver(base_path):
    """
    Method loads the profile which is required to auto download files without prompt
    regarding opening/saving file.
    Method creates browser driver which is essential for Selenium.
    """
    profile_path = str(Path(base_path + "/profiles/nuacbya2.nseprofile/"))
    profile = wd.FirefoxProfile(profile_path)

    download_directory = create_directory(base_path)
    profile.set_preference("browser.download.dir", download_directory)

    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")

    driver = wd.Firefox(firefox_profile=profile)
    driver.get(
        "https://www1.nseindia.com/products/content/equities/equities/eq_security.htm"
    )
    return driver


def set_static_values(driver):
    """
    Method sets the values to dropdown menu items.
    These are static values which can be set once per session.
    These can be changed according to the user needs.

    1. select_datatype is used to select the type of data format.
        Values which can be selected:
            1. value="priceVolume": Security wise price volume data (Default)
            2. value="deliverable": Security-wise Deliverable Positions Data
            3. value="priceVolumeDeliverable": Security-wise Price volume & Deliverable
                sposition data
    2. select_series is used to set the series of symbols.
        Only works with "EQ"
    3. select_time_period is usedd to select the time period of historic data.
        Values which can be selected:
            1. value="day": 1 Day
            2. value="week": 7 Days
            3. value="15days": 2 weeks
            4. value="1month": 1 month
            5. value="3month": 3 months
            6. value="12month": 365 Days
            7. value="24month": 24 Months
    """
    select_datatype = Select(driver.find_element_by_id("dataType"))
    select_datatype.select_by_value("priceVolume")

    select_series = Select(driver.find_element_by_id("series"))
    select_series.select_by_value("EQ")

    select_time_period = Select(driver.find_element_by_id("dateRange"))
    select_time_period.select_by_value("3month")


def set_symbol(driver, comp_symbol):
    """
    Method enters the SYMBOL to the symbol field.
    """
    symbol_bar = driver.find_element_by_id("symbol")
    symbol_bar.send_keys(comp_symbol)


def clear_options(driver):
    """
    Method clears the symbol field to avoid concatenation.
    """
    symbol_bar = driver.find_element_by_id("symbol")
    symbol_bar.clear()


def download_csv(driver):
    """
    Method to populate the table online and download the CSV file.
    """
    get_data_button = driver.find_element_by_id("submitMe")
    driver.execute_script("arguments[0].click()", get_data_button)
    time.sleep(
        2
    )  # Data takes time to load. Necessary to wait for download button to appear.
    try:
        download_csv_file = driver.find_element_by_css_selector(
            "span.download-data-link"
        )
        download_csv_file.click()
    except Exception as e_exception:
        print("Exception while downloading file: " + str(e_exception))


if __name__ == "__main__":
    BASE_PATH = os.path.abspath(os.getcwd())
    BROWSER = create_driver(BASE_PATH)
    set_static_values(BROWSER)
    START = timer()
    for symbol in stocks_lists.nifty_50:
        set_symbol(BROWSER, symbol)
        download_csv(BROWSER)
        clear_options(BROWSER)

    print("Fetched 50 files in: " + str(timer() - START))
    BROWSER.quit()
