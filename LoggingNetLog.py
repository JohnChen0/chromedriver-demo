from selenium import webdriver

opt = webdriver.ChromeOptions()
opt.add_argument('log-net-log=netlog')
opt.add_argument('net-log-capture-mode=IncludeCookiesAndCredentials')
driver = webdriver.Chrome(options=opt)

driver.get('http://google.com')

driver.quit()
