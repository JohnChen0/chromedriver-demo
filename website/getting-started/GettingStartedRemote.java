import java.net.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.*;
import org.openqa.selenium.remote.*;

public class GettingStartedRemote {

  public static void main(String[] args) throws MalformedURLException {
    WebDriver driver = new RemoteWebDriver(
        new URL("http://127.0.0.1:9515"),
        new ChromeOptions());
    driver.get("http://www.google.com");
    driver.quit();
  }
}
