require "selenium-webdriver"

caps = Selenium::WebDriver::Remote::Capabilities.chrome(
    "goog:chromeOptions" => {"args" => [ "window-size=1000,800" ]})
driver = Selenium::WebDriver.for :chrome, desired_capabilities: caps
