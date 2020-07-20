from selenium import webdriver

cap = {
  'goog:loggingPrefs': {
    'driver': 'ALL'
  }
}

driver = webdriver.Chrome(desired_capabilities=cap)
driver.get('https://google.com/')

log = driver.get_log('driver')
for entry in log:
  ts = entry['timestamp']
  print('[%d.%03d][%s]: %s' % (
        ts / 1000, ts % 1000, entry['level'], entry['message'][:-1]))

driver.quit()
