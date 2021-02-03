// By default, Chrome downloads files to current user's download folder,
// regardless of whether it is under the control of ChromeDriver.
// Headless Chrome blocks downloads by default, though recent versions of
// ChromeDriver configures headless Chrome to download to the current directory.

// This demo uses ChromeOptions to download a file to a location identified by
// targetdir. It works with both regular and headless Chrome.

using System.IO;
using System.Threading;

using OpenQA.Selenium.Chrome;

class DownloadFile
{
  static void Main(string[] args)
  {
    string targetDir = "Target";
    if (!Directory.Exists(targetDir)) {
      Directory.CreateDirectory(targetDir);
    }

    // Set ChromeOptions to control download target. Depending on the platform,
    // Chrome may require the target be given in absolute path.
    ChromeOptions options = new ChromeOptions();
    options.AddUserProfilePreference(
        "download.default_directory", Path.GetFullPath(targetDir));
    options.AddUserProfilePreference("download.prompt_for_download", false);

    options.AddArgument("headless");
    ChromeDriver driver = new ChromeDriver(options);

    // Download a file.
    driver.Navigate().GoToUrl(
        "https://the-internet.herokuapp.com/download/some-file.txt");

    // Try to give enough time for the download to finish.  driver.get() returns
    // before the download is complete. If driver.quit() is called too soon,
    // we get a partially downloaded file.
    Thread.Sleep(2000);
    driver.Quit();
  }
}
