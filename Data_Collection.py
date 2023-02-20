from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime

# set up the Edge driver
driver = webdriver.Edge()

# set the station ID and date range
station_id = 'C0F9T0'
start_date = datetime.date(2011, 11, 1)
end_date = datetime.date(2012, 1, 5)

# loop over the date range and download the CSV file for each date
current_date = start_date
while current_date <= end_date:
    # generate the URL for the current date
    date_str = current_date.strftime('%Y-%m-%d')
    url = f'https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?' \
          f'command=viewMain&' \
          f'station={station_id}&' \
          f'stname=%25E8%25A5%25BF%25E5%25B1%25AF&' \
          f'datepicker={date_str}&' \
          f'altitude=111m'

    # navigate to the URL and click the download button
    driver.get(url)
    download_button = driver.find_element(By.XPATH, '//*[@id="downloadCSV"]/input')
    download_button.click()

    # move to the next date
    current_date += datetime.timedelta(days=1)
time.sleep(5)
# close the browser
driver.quit()
