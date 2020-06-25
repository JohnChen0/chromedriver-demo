'use strict';

const webdriver = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

function usage() {
  console.log('usage: "' + process.argv[0]
      + '" "' + process.argv[1] + '" [optins...]');
  console.log('\t-driver driverPath');
  console.log('\t-chrome chromePath');
  console.log('\t-data userDataPath');
  console.log('\t-service (use ChromeDriver service)');
  console.log('\t-remote http://ipAddress:port (connect to existing ChromeDriver)');
  console.log('\t-url URL');
  console.log('\t-log logFilePath');
  console.log('\t-save htmlFilePath (save page contents to file)');
  console.log('\t-name (display browser name)');
  console.log('\t-title (display page title)');
  console.log('\t-cookies (cookies demo)');
  console.log('\t-position (set position demo)');
  console.log('\t-size (set size demo)');
  console.log('\t-keep (do not quit ChromeDriver)');
  process.exit(1);
}

let driverPath = undefined;
let chromePath = undefined;
let userDataDir = undefined;
let useService = false;
let remotePort = undefined;
let url = 'https://www.google.com/';
let logPath = undefined;
let html = undefined;
let remoteDebuggingPort = undefined;
let name = false;
let title = false;
let testCookies = false;
let testPosition = false;
let testSize = false;
let quit = true;

// process.argv[0] is path to node, process.argv[1] is path to JS file.
// User arguments start with process.argv[2].
for (let argi = 2; argi < process.argv.length; argi++) {
  if (process.argv[argi][0] !== '-') usage();

  if (process.argv[argi] === '-driver' && argi + 1 < process.argv.length)
    driverPath = process.argv[++argi];
  else if (process.argv[argi] === '-chrome' && argi + 1 < process.argv.length)
    chromePath = process.argv[++argi];
  else if (process.argv[argi] === '-data' && argi + 1 < process.argv.length)
    userDataDir = process.argv[++argi];
  else if (process.argv[argi] === '-service')
    useService = true;
  else if (process.argv[argi] === '-remote' && argi + 1 < process.argv.length)
    remotePort = process.argv[++argi];
  else if (process.argv[argi] === '-url' && argi + 1 < process.argv.length)
    url = process.argv[++argi];
  else if (process.argv[argi] === '-log' && argi + 1 < process.argv.length)
    logPath = process.argv[++argi];
  else if (process.argv[argi] === '-save' && argi + 1 < process.argv.length)
    html = process.argv[++argi];
  else if (process.argv[argi] === '-debug' && argi + 1 < process.argv.length)
    remoteDebuggingPort = process.argv[++argi];
  else if (process.argv[argi] === '-name')
    name = true;
  else if (process.argv[argi] === '-title')
    title = true;
  else if (process.argv[argi] === '-cookies')
    testCookies = true;
  else if (process.argv[argi] === '-position')
    testPosition = true;
  else if (process.argv[argi] === '-size')
    testSize = true;
  else if (process.argv[argi] === '-keep')
    quit = false;
  else
    usage();
}

let driver;

if (remotePort !== undefined) {
  driver = new webdriver.Builder()
      .forBrowser('chrome')
      .usingServer(remotePort)
      .build();
} else {
  let builder = new chrome.ServiceBuilder(driverPath);
  const options = new chrome.Options();

  if (chromePath !== undefined)
    options.setChromeBinaryPath(chromePath);

  if (userDataDir !== undefined)
    options.addArguments('user-data-dir=' + userDataDir);

  if (logPath !== undefined)
    builder = builder.loggingTo(logPath).enableVerboseLogging();

  const service = builder.build();
  driver = chrome.Driver.createSession(options, service);
}

let promise = Promise.resolve();

if (name) {
  promise = promise.then(() => {
    driver.getCapabilities().then(capabilities => {
      console.log('Browser name: '
          + capabilities.get(webdriver.Capability.BROWSER_NAME));
    });
  });
}

promise = promise.then(() => driver.get(url));

if (title) {
  promise = promise.then(() => {
    driver.getTitle().then(title => console.log('Page title: ' + title));
  });
  promise = promise.then(() => {
    driver.getCurrentUrl().then(url => console.log('Page URL: ' + url));
  });
}

if (quit) {
  promise = promise
      .then(() => new Promise(resolve => setTimeout(resolve, 3000)))
      .then(() => driver.quit());
}
