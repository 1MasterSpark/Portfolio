from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://en.wikipedia.org/w/index.php?returnto=Main+Page&title=Special:UserLogin")
usernamebox = driver.find_element(By.ID, "wpName1")
passwordbox = driver.find_element(By.ID, "wpPassword1")
login_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[2]/div/form/div[4]/div/button")

usernamebox.send_keys("[censored]")
passwordbox.send_keys("[censored]")
login_button.click()
WebDriverWait(driver, 10).until(EC.url_to_be("https://en.wikipedia.org/wiki/Main_Page"))

driver.get("https://en.wikipedia.org/w/index.php?title=User:[censored]/sandbox&action=edit")

edittextarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "wpTextbox1")))
text = edittextarea.get_attribute("value")
print(text)

driver.quit()