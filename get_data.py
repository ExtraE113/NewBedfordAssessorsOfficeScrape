import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

SKIP_LIST = [1098, 1380, 2596, 3837, 7965, 7966, 10431, 10432, 11940]

driver = webdriver.Firefox()

driver.implicitly_wait(10)

driver.get("https://www.newbedford-ma.gov/assessors/parcel-lookup/")
driver.set_window_size(1379, 964)
driver.switch_to.frame(0)
driver.find_element(By.ID, "LUC").click()
dropdown = driver.find_element(By.ID, "LUC")
dropdown.find_element(By.XPATH, "//option[. = '101-Single Famly']").click()
# time.sleep(5)
e = driver.find_element(By.ID, "oSearch")
driver.execute_script('arguments[0].scrollIntoView(true);', e)
e.click()

for i in range(11938, 1000000):

	# skip some vals because for some reason you can't extract it from the website (you get 500 ise)
	if i in SKIP_LIST:
		continue

	for j in range(3, i, 150):
		element = driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({j}) a")
		driver.execute_script('arguments[0].scrollIntoView(true);', element)
		time.sleep(random.uniform(0.05, 0.2)/5)

	element = driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({i}) a")
	driver.execute_script('arguments[0].scrollIntoView(true);', element)
	time.sleep(random.uniform(0.1, 0.3)/5)

	time.sleep(random.uniform(0.1, 1)/10)
	element.click()

	driver.switch_to.default_content()
	iframe = driver.find_element(By.TAG_NAME, "iframe")
	driver.switch_to.frame(iframe)
	src = driver.page_source

	# save src to a file
	with open(f"html/{i}.html", "w") as f:
		f.write(src)

	time.sleep(random.uniform(1.1, 2)/20)
	# scroll to top
	driver.switch_to.default_content()
	driver.execute_script('window.scrollTo(0, 0);')
	driver.switch_to.frame(iframe)
	element = driver.find_element(By.CSS_SELECTOR, ".back")
	time.sleep(random.uniform(0.1, 1)/20)
	element.click()
	driver.switch_to.default_content()
	driver.switch_to.frame(0)
	time.sleep(random.uniform(0.1, 1)/20)
