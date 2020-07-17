import java.util.Arrays;
import org.openqa.selenium.chrome.*;

public class BlockPopups {
  public static void main(String[] args) throws Exception {
    ChromeOptions options = new ChromeOptions();
    options.setExperimentalOption("excludeSwitches",
        Arrays.asList("disable-popup-blocking"));
    ChromeDriver driver = new ChromeDriver(options);

    driver.executeScript("window.open()");

    Thread.sleep(2000);
    driver.quit();
  }
}
