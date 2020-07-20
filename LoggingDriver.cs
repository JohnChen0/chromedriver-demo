using System;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;

class LoggingDriver
{
    static void Main()
    {
        ChromeOptions options = new ChromeOptions();
        options.SetLoggingPreference(LogType.Driver, LogLevel.All);

        ChromeDriver driver = new ChromeDriver(options);
        driver.Navigate().GoToUrl("https://google.com/");

        Console.WriteLine(driver.Manage().Logs);
        foreach (LogEntry entry in driver.Manage().Logs.GetLog(LogType.Driver))
        {
            Console.Write(entry);
        }

        driver.Quit();
    }
}
