# Use Chrome's perf log to get a list of all network requests

from selenium import webdriver
import json

cap = {
  'goog:loggingPrefs': {
    'performance': 'ALL'
  }
}

driver = webdriver.Chrome(desired_capabilities=cap)
driver.get('https://google.com/')

log = driver.get_log('performance')
for entry in log:
  message = json.loads(entry['message'])['message']
  if message['method'] == 'Network.requestWillBeSent':
    print entry['timestamp'], \
          message['params']['request']['method'], \
          message['params']['request']['url'], \
          message['params']['documentURL']

driver.quit()
