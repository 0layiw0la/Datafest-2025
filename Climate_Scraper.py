from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

# 1. 36 states + centroid coords
states_coords = {
    'Abia': (5.5320, 7.4860),
    'Adamawa': (9.3265, 12.3984),
    'Akwa Ibom': (5.0300, 7.9400),
    'Anambra': (6.2109, 7.0710),
    'Bauchi': (10.3100, 9.8400),
    'Bayelsa': (4.6400, 6.0000),
    'Benue': (7.3363, 8.8393),
    'Borno': (11.8333, 13.1500),
    'Cross River': (5.9667, 8.3333),
    'Delta': (5.5853, 5.0184),
    'Ebonyi': (5.7630, 7.9083),
    'Edo': (6.6313, 5.5516),
    'Ekiti': (7.6248, 6.8228),
    'Enugu': (6.5207, 7.4139),
    'Gombe': (10.2899, 11.1678),
    'Imo': (5.5273, 7.0258),
    'Jigawa': (12.9000, 9.5167),
    'Kaduna': (10.5105, 7.4165),
    'Kano': (12.0022, 8.5919),
    'Katsina': (12.9855, 7.6088),
    'Kebbi': (12.4500, 4.2000),
    'Kogi': (7.7986, 6.7394),
    'Kwara': (8.3983, 4.5414),
    'Lagos': (6.5244, 3.3792),
    'Nasarawa': (8.5173, 8.5167),
    'Niger': (9.6148, 6.5564),
    'Ogun': (7.1600, 4.2833),
    'Ondo': (7.2500, 5.2000),
    'Osun': (7.5000, 4.5000),
    'Oyo': (7.8731, 3.8450),
    'Plateau': (9.0000, 8.6775),
    'Rivers': (4.8500, 6.5500),
    'Sokoto': (13.0578, 5.2438),
    'Taraba': (8.0000, 10.0000),
    'Yobe': (12.0035, 11.8307),
    'Zamfara': (12.1700, 6.6700),
}
exists = set()

# 2. Selenium setup
service = Service("./chromedriver-win64/chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

base_url = "https://aquastat.fao.org/climate-information-tool/complete-climate-data"

for state, (lat, lon) in states_coords.items():
    if state in exists:
        print(f"→ {state} already exists, skipping.")
        continue
    else:
        exists.add(state)
        
    url = f"{base_url}?lat={lat}&lon={lon}&year=2022&datasource=agera5"
    driver.get(url)

    # optional short pause for JS boot
    time.sleep(15)

    # wait until table is present, with retry on timeout
    try:
        table = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table.data-table-2 tbody tr")))
    except TimeoutException:

        print(f"⚠ Timeout loading table for {state}")
        driver.save_screenshot(f"{state}_timeout.png")
        continue

    # now fetch rows
    rows = driver.find_elements(By.CSS_SELECTOR, "table.data-table-2 tr")

    # parse header
    headers = [th.text.strip() for th in rows[0].find_elements(By.TAG_NAME, "th")]

    data = []
    for tr in rows[1:]:
        cols = [td.text.strip().replace("\n", " ") for td in tr.find_elements(By.TAG_NAME, ("td"))]
        if cols:
            data.append(cols)

    # build DataFrame and save
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(f"Datasets/AquaStat Data Each state/{state.replace(' ', '_')}_climate_2022.csv", index=False)
    print(f"→ Saved {state}.csv")
    time.sleep(2)   # be gentle on the server

driver.quit()