# Recent versions of ChromeDriver supports taking full-page screenshot.
# A PR to add this command to WebDriver standard is open
# at https://github.com/w3c/webdriver/pull/1536.
# This command is not yet supported by the Selenium library,
# so some extra code is required to access it.

from selenium import webdriver
import base64

driver = webdriver.Chrome()
driver.command_executor._commands['screenshotFull'] = (
    'GET', '/session/$sessionId/screenshot/full')

driver.get('https://chromedriver.chromium.org/getting-started')
result = driver.execute('screenshotFull')
with open('test.png', 'wb') as f:
  f.write(base64.b64decode(result['value']))

driver.quit()
