require "selenium-webdriver"

cap = {
    'goog:loggingPrefs': {
      'driver': 'ALL'
    }
}

driver = Selenium::WebDriver.for :chrome, desired_capabilities: cap

driver.get("http://www.google.com/")

log = driver.manage.logs.get('driver')
for entry in log
  ts = entry.timestamp
  print '[%d.%03d][%s]: %s' % [ts / 1000, ts % 1000, entry.level, entry.message]
end
