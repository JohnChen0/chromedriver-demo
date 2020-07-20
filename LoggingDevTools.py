from selenium import webdriver
import json

cap = {
  'goog:loggingPrefs': {
    'devtools': 'ALL'
  }
}

options = webdriver.ChromeOptions()
options.add_experimental_option('devToolsEventsToLog', [
    'DOM.childNodeCountUpdated',
    'Page.frameAttached',
    'Page.frameDetached',
    'Page.frameNavigated',
    'Page.frameStartedLoading',
    'Page.frameStoppedLoading',
    'Runtime.executionContextCreated',
    'Runtime.executionContextDestroyed',
    'Runtime.executionContextsCleared',
])

driver = webdriver.Chrome(options=options, desired_capabilities=cap)
driver.get('https://google.com/')

log = driver.get_log('devtools')
for entry in log:
  ts = entry['timestamp']
  message = json.loads(entry['message'])
  print '%d\t%s\t%s' % (ts, entry['level'], message['method'])

driver.quit()
