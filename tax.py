import glob,os
import time
import json
import pandas as pd
import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select

calculate_btn = 'button[value=Beregn skat !]'

html_file = glob.glob(f"{os.getcwd()}/*.htm")[0]

options = ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(10)

page =  driver.get(f'file://{html_file}')

# define elements
total_tax = driver.find_element(By.CSS_SELECTOR,'input[name=skatIalt]')
salary_input = driver.find_element(By.CSS_SELECTOR,value='input[name=MloenFoerAMB1]')
calc_btn = driver.find_element(By.CSS_SELECTOR,'input[type=button]')

income_dict = {}

maximum_income = 2000_000
step = 10_00

tax_df = pd.DataFrame(data={'pretax_income':[],'tax':[],'after_tax_income':[]})

# bor i kbh
select= Select(driver.find_element(By.CSS_SELECTOR,'select[name="kommune"]'))
select.select_by_visible_text("København")

# ikke medlem af folkekirken
driver.find_element(By.CSS_SELECTOR,"input[value=Mikkemedlem]").click()

with tqdm.tqdm(total=maximum_income+step) as bar:
    for income in range(0,maximum_income+step,step):
        salary_input.send_keys(income)
        calc_btn.click()

        tax_paid = float(total_tax.get_attribute('value').replace('.',""))
        salary_input.clear()

        tax_df = tax_df.append(other={'pretax_income':float(income),'tax':tax_paid,'after_tax_income':income-float(tax_paid)},ignore_index=True)

        bar.update(income)

print("Saving dataframe")
tax_df.to_csv(path_or_buf='tax_df.csv',index=False)
