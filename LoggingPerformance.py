# A demo of collecting Chrome performance logs through ChromeDriver.
# See https://chromedriver.chromium.org/logging/performance-log

from selenium import webdriver
import json

cap = {
  'goog:loggingPrefs': {
    'performance': 'ALL'
  }
}

options = webdriver.ChromeOptions()
options.add_experimental_option('perfLoggingPrefs', {
    'traceCategories': 'browser,devtools.timeline,devtools'
})

driver = webdriver.Chrome(options=options, desired_capabilities=cap)
driver.get('https://google.com/')

log = driver.get_log('performance')
for entry in log:
  ts = entry['timestamp']
  message = json.loads(entry['message'])['message']
  if message['method'] == 'Tracing.dataCollected':
    print '%d\t%s\t%s' % (ts, message['params']['ph'],
                          message['params']['name'])
  else:
    print "%d\t%s" % (ts, message['method'])

driver.quit()
