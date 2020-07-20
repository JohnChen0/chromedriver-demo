# ChromeDriver users the 'browser' logging type to provide console logs.

from selenium import webdriver

if webdriver.__version__[0] <= '3':
  cap = {
    'se:options': {
      'loggingPrefs': {
        'browser': 'ALL'
      }
    }
  }
  driver = webdriver.Chrome(desired_capabilities=cap)
else:
  options = webdriver.ChromeOptions()
  options.set_capability('se:options', {
    'loggingPrefs': {
      'browser': 'ALL'
    }
  })
  driver = webdriver.Chrome(options=options)

# Both ChromeDriver & DevTools: "Hello World!"
driver.execute_script('console.log("Hello World!")')

# ChromeDriver: Object
# DevTools: <Expandable UI representation of the object>
driver.execute_script('console.log({ str: "Some text", id: 5 })')

# ChromeDriver: Window
# DevTools: <Expandable UI representation of the Window object>
driver.execute_script('console.log(window)');

# ChromeDriver: "Hello" Object "more text"
# DevTools Hello <Expandable UI representation of the object> more text
driver.execute_script(
    'console.log("Hello", { str: "Some text", id: 5 }, "more text")')

# ChromeDriver: "Hello, %s = %d." "foo" 3 "etc"
# DevTools: Hello, foo = 3. etc
driver.execute_script('console.log("Hello, %s = %d.", "foo", 3, "etc")')

# ChromeDriver: "Hello, %d = %s." "foo" 3 Window
# DevTools: Hello, NaN = 3. <the Window object>
driver.execute_script('console.log("Hello, %d = %s.", "foo", 3, window)')

log = driver.get_log('browser')
for entry in log:
  print(entry['source'] + '\t' + entry['message'])

driver.quit()
