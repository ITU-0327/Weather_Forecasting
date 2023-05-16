from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
from config import config

options = webdriver.EdgeOptions()
prefs = {"download.default_directory": config['download_path']}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Edge(options=options)

start_date = datetime.date(2011, 11, 1)
end_date = datetime.date.today()

start_time = time.monotonic()

current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    url = f'https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?' \
          f'command=viewMain&' \
          f'station={config["station_id"]}&' \
          f'stname=%25E8%25A5%25BF%25E5%25B1%25AF&' \
          f'datepicker={date_str}&' \
          f'altitude=111m'

    driver.get(url)
    download_button = driver.find_element(By.XPATH, '//*[@id="downloadCSV"]/input')
    download_button.click()

    current_date += datetime.timedelta(days=1)

end_time = time.monotonic()
elapsed_time = end_time - start_time

print(f"Takes {elapsed_time:.2f} seconds to download all the files.")
time.sleep(5)

driver.quit()
