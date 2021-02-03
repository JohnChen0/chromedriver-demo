// By default, Chrome downloads files to current user's download folder,
// regardless of whether it is under the control of ChromeDriver.
// Headless Chrome blocks downloads by default, though recent versions of
// ChromeDriver configures headless Chrome to download to the current directory.

// This demo uses ChromeOptions to download a file to a location identified by
// targetdir. It works with both regular and headless Chrome.

import java.io.*;
import java.util.*;

import org.openqa.selenium.chrome.*;

class DownloadFile
{
  public static void main(String[] args) throws Exception {
    File targetDir = new File("Target");
    if (!targetDir.isDirectory()) {
      targetDir.mkdirs();
    }

    // Set ChromeOptions to control download target. Depending on the platform,
    // Chrome may require the target be given in absolute path.
    ChromeOptions options = new ChromeOptions();
    Map<String, Object> prefs = new HashMap<>();
    prefs.put("download.default_directory", targetDir.getAbsolutePath());
    prefs.put("download.prompt_for_download", false);
    options.setExperimentalOption("prefs", prefs);

    options.setHeadless(true);
    ChromeDriver driver = new ChromeDriver(options);

    // Download a file.
    driver.get("https://the-internet.herokuapp.com/download/some-file.txt");

    // Try to give enough time for the download to finish.  driver.get() returns
    // before the download is complete. If driver.quit() is called too soon,
    // we get a partially downloaded file.
    Thread.sleep(2000);
    driver.quit();
  }
}
