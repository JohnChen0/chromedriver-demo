(async function() {
  const chrome = require('selenium-webdriver/chrome');
  const options = new chrome.Options();
  options.setUserPreferences({
    'profile.managed_default_content_settings.images': 2
  });
  const driver = chrome.Driver.createSession(options);
  await driver.get('https://selenium.dev/');
  await new Promise(resolve => setTimeout(resolve, 2000));
  await driver.quit();
})();
