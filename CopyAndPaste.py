# Demo of copying and pasting using Ctrl+c and Ctrl+v,
# first using send_keys and then using actions.
# On Mac, requires ChromeDriver version 86+.
# On headless Chrome, copy-and-paste operates on a Chrome internal clipboard,
# instead of the system clipboard.

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from sys import platform
from time import sleep

driver = webdriver.Chrome()

try:
  driver.execute_script('''
    document.write('<input type="text" id="text1" value="Hello World" />');
    document.write('<br/>')
    document.write('<input type="text" id="text2" />');
  ''')
  sleep(1)

  hold_key = Keys.COMMAND if platform == 'darwin' else Keys.CONTROL
  box1 = driver.find_element_by_id('text1')
  box2 = driver.find_element_by_id('text2')

  box1.send_keys(hold_key + 'ac')
  box2.send_keys(hold_key + 'v')

  text1 = box1.get_attribute('value')
  text2 = box2.get_attribute('value')
  assert text1 == text2, 'expect "%s", got "%s"' % (text1, text2)
  sleep(1)

  driver.execute_script('arguments[0].value = "Good-bye"', box1)
  box2.clear()
  sleep(1)

  (ActionChains(driver)
    .click(box1)
    .key_down(hold_key).send_keys('ac').key_up(hold_key)
    .click(box2)
    .key_down(hold_key).send_keys('v').key_up(hold_key)
    .perform())

  text1 = box1.get_attribute('value')
  text2 = box2.get_attribute('value')
  assert text1 == text2, 'expect "%s", got "%s"' % (text1, text2)
finally:
  sleep(1)
  driver.quit()
