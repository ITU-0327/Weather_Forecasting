from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
from config import config

# set the default download directory for Edge
options = webdriver.EdgeOptions()
# replace with your preferred download directory
prefs = {"download.default_directory": config['download_path']}
options.add_experimental_option("prefs", prefs)

# set up the Edge driver
driver = webdriver.Edge(options=options)

# set the date range
# the data from the CWB starts from 2011/11/1
start_date = datetime.date(2023, 2, 19)
end_date = datetime.date.today()

# start the timer
start_time = time.monotonic()

# loop over the date range and download the CSV file for each date
current_date = start_date
while current_date <= end_date:
    # generate the URL for the current date
    date_str = current_date.strftime('%Y-%m-%d')
    url = f'https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?' \
          f'command=viewMain&' \
          f'station={config["station_id"]}&' \
          f'stname=%25E8%25A5%25BF%25E5%25B1%25AF&' \
          f'datepicker={date_str}&' \
          f'altitude=111m'

    # navigate to the URL and click the download button
    driver.get(url)
    download_button = driver.find_element(By.XPATH, '//*[@id="downloadCSV"]/input')
    download_button.click()

    # move to the next date
    current_date += datetime.timedelta(days=1)

# end the timer and calculate the elapsed time
end_time = time.monotonic()
elapsed_time = end_time - start_time

# print the elapsed time
print(f"Takes {elapsed_time:.2f} seconds to download all the files.")
time.sleep(5)

# close the browser
driver.quit()
