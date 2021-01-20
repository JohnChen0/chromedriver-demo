// Demo of using ChromeDriver --readable-timestamp options with Selenium Java

import java.io.File;
import com.google.common.collect.ImmutableList;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeDriverService;

public class ReadableTimestamp {
  static class ReadableTimestampBuilder extends ChromeDriverService.Builder {
    // If using latest Selenium 4.0.0 beta, need to return List<String> instead.
    @Override
    protected ImmutableList<String> createArgs() {
      ImmutableList.Builder<String> argsBuilder = ImmutableList.builder();
      argsBuilder.addAll(super.createArgs());
      argsBuilder.add("--readable-timestamp");
      return argsBuilder.build();
    }
  }

  public static void main(String[] args) throws Exception {
    ChromeDriverService service = new ReadableTimestampBuilder()
        .withLogFile(new File("chromedriver.log"))
        .withVerbose(true)
        .build();

    ChromeDriver driver = new ChromeDriver(service);

    driver.get("https://google.com/");

    Thread.sleep(2000);
    driver.quit();
  }
}
