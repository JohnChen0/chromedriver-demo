import java.util.HashMap;
import java.util.logging.Level;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.logging.LogEntry;
import org.openqa.selenium.logging.LogType;
import org.openqa.selenium.logging.LoggingPreferences;
import org.openqa.selenium.remote.CapabilityType;

public class LoggingConsole {
  public static void main(String[] args) {
    LoggingPreferences prefs = new LoggingPreferences();
    prefs.enable(LogType.BROWSER, Level.ALL);
    ChromeOptions options = new ChromeOptions();
    options.setCapability(CapabilityType.LOGGING_PREFS, prefs);
    ChromeDriver driver = new ChromeDriver(options);

    driver.executeScript("console.log('Hello World!')");
    driver.executeScript("console.log(window)");

    for (LogEntry entry: driver.manage().logs().get(LogType.BROWSER)) {
      System.out.println(entry);
      System.out.println(entry.getLevel());
      System.out.println(entry.getMessage());
    }

    driver.quit();
  }
}
