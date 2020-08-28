from selenium import webdriver
from time import sleep

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
  'custom_handlers.registered_protocol_handlers': [
    {
      'default': True,
      'protocol': 'mailto',
      'url': "https://mail.google.com/mail/?extsrc=mailto&url=%s"
    }
  ]
})

driver = webdriver.Chrome(options=options)
driver.get('mailto:test@test.com')

sleep(2)
driver.quit()
