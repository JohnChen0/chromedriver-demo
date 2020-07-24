from selenium import webdriver
from time import sleep

opt = webdriver.ChromeOptions()
opt.add_experimental_option('prefs', {
    'profile.managed_default_content_settings.images': 2
})
driver = webdriver.Chrome(options=opt)
driver.get('https://selenium.dev/')

sleep(2)
driver.quit()
