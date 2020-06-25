#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from sys import argv
import time

def usage():
  print('usage: "%s" [optins...]' % argv[0])
  print('\t-driver driverPath')
  print('\t-chrome chromePath')
  print('\t-data userDataPath')
  print('\t-service (use ChromeDriver service)')
  print('\t-remote http://ipAddress:port (connect to existing ChromeDriver)')
  print('\t-url URL')
  print('\t-log logFilePath')
  print('\t-save htmlFilePath (save page contents to file)')
  print('\t-debug ipAddress:port')
  print('\t-name (display browser name)')
  print('\t-title (display page title)')
  print('\t-cookies (cookies demo)')
  print('\t-position (set position demo)')
  print('\t-size (set size demo)')
  print('\t-keep (do not quit ChromeDriver)')
  exit(1)

executable_path = 'chromedriver'
use_service = False
remote_port = None
chrome_options = None
service_args = None
url = 'http://www.google.com/'
html = None
name = False
title = False
quit = True

testCookies = False
testPosition = False
testSize = False

def initChromeOptions():
  global chrome_options
  if chrome_options == None:
    chrome_options = webdriver.ChromeOptions()

argi = 1
while argi < len(argv):
  if not argv[argi].startswith('-'):
    usage()

  if argv[argi] == '-driver' and argi + 1 < len(argv):
    executable_path = argv[argi + 1]
    argi += 1
  elif argv[argi] == '-chrome' and argi + 1 < len(argv):
    initChromeOptions()
    chrome_options.binary_location = argv[argi + 1]
    argi += 1
  elif argv[argi] == '-data' and argi + 1 < len(argv):
    initChromeOptions()
    chrome_options.add_argument('user-data-dir=' + argv[argi + 1])
    argi += 1
  elif argv[argi] == '-service':
    use_service = True
  elif argv[argi] == '-remote' and argi + 1 < len(argv):
    remote_port = argv[argi + 1]
    argi += 1
  elif argv[argi] == '-url' and argi + 1 < len(argv):
    url = argv[argi + 1]
    argi += 1
  elif argv[argi] == '-log' and argi + 1 < len(argv):
    service_args = ['--verbose', '--log-path=' + argv[argi + 1]]
    argi += 1
  elif argv[argi] == '-save' and argi + 1 < len(argv):
    html = argv[argi + 1]
    argi += 1
  elif argv[argi] == '-debug' and argi + 1 < len(argv):
    # Chrome should have been started with --remote-debugging-port=port
    initChromeOptions()
    chrome_options.add_experimental_option('debuggerAddress', argv[argi + 1])
    argi += 1
  elif argv[argi] == '-name':
    name = True;
  elif argv[argi] == '-title':
    title = True;
  elif argv[argi] == '-cookies':
    testCookies = True;
  elif argv[argi] == '-position':
    testPosition = True;
  elif argv[argi] == '-size':
    testSize = True;
  elif argv[argi] == '-keep':
    quit = False;
  else:
    usage()

  argi += 1

if use_service and remote_port != None:
  print("Can't use both -service and -remote options")
  exit(1)

# Connect to ChromeDriver
#
# There are three different ways to start the ChromeDriver:
# 1. Start ChromeDriver by some means not under the control of Python WebDriver
#    library, e.g., manually on the command line. In this case, we need to know
#    the host and port that ChromeDriver is listening on. This is stored in
#    remote_port variable, in the format http://hostname:port. We then use
#    webdriver.Remote class (an alias of webdriver.remote.webdriver.WebDriver)
#    to connect to ChromeDriver.
# 2. Use Service class to start ChromeDriver and to control its lifetime. The
#    variable use_service would be True in this case. Once ChromeDriver is
#    started by Service, we ask for its port, and then the rest is identical to
#    case 1.
# 3. Use webdriver.Chrome (an alias of webdriver.chrome.webdriver.WebDriver)
#    class to start ChromeDriver and then immediately connect to it. This class
#    inherits from webdriver.Remote (the class used in cases 1 & 2). It
#    overrides __init__() to start ChromeDriver using Service class, and quit()
#    to stop ChromeDriver. Chrome class also has two additional methods not
#    available in its base class: launch_app() to launch a Chrome app, and
#    create_options() to create an instance of chrome.options.Options class.
#
# The constructor for webdriver.Remote (case 1) takes several parameters, two
# of which are important:
# * command_executor (required) is the host/port of the WebDriver to connect to.
# * desired_capabilities (required) is the set of capabilities to send to the
#   WebDriver after connection is made.
#
# The constructor for Chrome's Service class (case 2) takes several parameters:
# * executable_path (required) is the executable file containing ChromeDriver.
# * port is the port that ChromeDriver will listen on. By default a free port is
#   automatically chosen. The option "--port=%d" is automatically added to
#   the command line that is used to start ChromeDriver.
# * service_args is a list of args passed to ChromeDriver without changes.
# * log_path is location of ChromeDriver log file. If specified, "--log-path=%s"
#   is automatically added to service_args.
# * env contains the environment variables to pass to ChromeDriver.
#
# The constructor for Chrome class (case 3) takes the following parameters:
# * executable_path, port, and service_args are passed to Service class, with
#   executable_path defaults to 'chromedriver' and not required.
# * service_log_path is passed to Service class as log_path parameter.
# * chrome_options allows a more structured way to specify Chrome-specific
#   capabilities. ChromeOptions.to_capabilities() converts the options into
#   capabilities format, with all Chrome-specific options under "chromeOptions"
#   key.  While desired_capabilities is a dict, chrome_options (if specified)
#   is an instance of ChromeOptions, with named properties that can be set.
#   Anything that can be specified in chrome_options can also be specified in
#   desired_capabilities instead.
# * desired_capabilities is passed to webdriver.Remote. If both chrome_options
#   and desired_capabilities are specified, they are merged together. If neither
#   are specified, a default set of capabilities are used.
if use_service:
  service = Service(
    executable_path=executable_path,
    service_args=service_args)
  service.start()
  remote_port = service.service_url
  print('Service URL: ' + remote_port)

if remote_port != None:
  driver = webdriver.Remote(remote_port, options=chrome_options)
else:
  driver = webdriver.Chrome(
    executable_path=executable_path,
    chrome_options=chrome_options,
    service_args=service_args)

if name:
  print('Browser name: ' + driver.name)

driver.get(url)

if title:
  print('Page title: ' + driver.title)
  print('Page URL: ' + driver.current_url)

if html is not None:
  with open(html, 'w') as f:
    f.write(driver.page_source.encode('utf-8'))

if testCookies:
  driver.add_cookie({
      'path': '/',
      'expiry': 2000000000,
      'name': 'foo',
      'value': 'bar'})
  print('Cookies = ' + str(driver.get_cookies()))

if testPosition:
  pos = driver.get_window_position()
  x = pos['x']
  y = pos['y']
  print('Current window position (%d, %d)' % (x, y))

  x += 100
  y += 100
  print('Attempting to change window position to (%d, %d)' % (x, y))
  driver.set_window_position(x, y)

  pos = driver.get_window_position()
  print('New window position (%d, %d)' % (pos['x'], pos['y']))

if testSize:
  size = driver.get_window_size()
  width = size['width']
  height = size['height']
  print('Current window size %dx%d' % (width, height))

  width /= 2
  height /= 2
  print('Attempting to change window size to %dx%d' % (width, height))
  driver.set_window_size(width, height)

  size = driver.get_window_size()
  print('New window size %dx%d' % (size['width'], size['height']))

if quit:
  time.sleep(3)
  driver.quit()
