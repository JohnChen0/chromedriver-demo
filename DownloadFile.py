# By default, Chrome downloads files to current user's download folder,
# regardless of whether it is under the control of ChromeDriver.
# Headless Chrome blocks downloads by default, though recent versions of
# ChromeDriver configures headless Chrome to download to the current directory.

# This demo uses ChromeOptions to download a file to a location identified by
# target_dir. It works with both regular and headless Chrome.

from selenium import webdriver
import os
import time

target_dir = 'Target'
if not os.path.isdir(target_dir):
  os.mkdir(target_dir)

# Set ChromeOptions to control download target. Depending on the platform,
# Chrome may require the target be given in absolute path.
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
  'download': {
    'default_directory': os.path.abspath(target_dir),
    'prompt_for_download': False
  }
})

options.set_headless()
driver = webdriver.Chrome(options=options)

# Download a file.
driver.get('http://the-internet.herokuapp.com/download/some-file.txt')

# Try to give enough time for the download to finish.  driver.get() returns
# before the download is complete. If driver.quit() is called too soon,
# we get a partially downloaded file.
time.sleep(2)

driver.quit()
