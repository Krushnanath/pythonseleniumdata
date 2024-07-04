from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import pandas as pd

chrome_options = ChromeOptions()
#chrome_options.add_argument('--headless')  # Runs Chrome in headless mode
#chrome_options.add_argument('--disable-gpu')  # Disables GPU hardware acceleration
chrome_options.add_argument('--log-level=3')  # Suppress Selenium logs

# Initialize the WebDriver using WebDriverManager
#driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
# Read Excel file, process each name, and update in place
input_output_file = 'data.xlsx'
df = pd.read_excel(input_output_file, engine='openpyxl')


try:
    for index, row in df.iterrows():
        name = row['name']  # Replace with actual column name containing names   
           # Step 1: Go to the website
        driver.get("https://www.google.com/")

    # Step 2: Find the search bar and enter "names"
        search_bar = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
        search_bar.send_keys(name)
        search_bar.send_keys(Keys.RETURN)

    # Step 3: Wait for the search results to load and click on the first result
        # time.sleep(4)
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//span[contains(text(), 'Wikipedia')])[1]")
            )
        )
        # first_result = driver.find_element(By.XPATH, "(//span[contains(text(), 'Wikipedia')])[1]")
        first_result.click()

    # # Step 4: Click on the "More" button


    # Wait for element visibility
    # element = WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located((By.XPATH, "//div[@id='example']"))
    # )

    # if element.is_displayed():
    #     print("Element is visible on the page")
    # else:
    #     print("Element is not visible on the page")
    # more_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "xpath_for_more_button"))
    # )
    # more_button.click()

    # Step 5: Collect the job description text
        job_desc_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="mw-content-text"]/div[1]/p[3]'))
        )
        job_desc = job_desc_element.text

        # print(job_desc)
        df.at[index, 'job_description'] = job_desc
    
    # Write updated DataFrame back to the same Excel file
        df.to_excel(input_output_file, index=False, engine='openpyxl')

finally:
    # Close the WebDriver
    driver.quit()
# Iterate over each row




