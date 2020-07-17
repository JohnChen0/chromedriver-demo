from selenium import webdriver

caps = webdriver.DesiredCapabilities.CHROME.copy()
caps['acceptInsecureCerts'] = True
driver = webdriver.Chrome(desired_capabilities=caps)

driver.quit()
