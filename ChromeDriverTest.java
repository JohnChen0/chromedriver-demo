import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Set;
import org.openqa.selenium.Cookie;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.Point;
import org.openqa.selenium.Proxy;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeDriverService;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;

public class ChromeDriverTest {
  static void usage() {
    System.err.println("Available options:");
    System.err.println("\t-driver driverPath");
    System.err.println("\t-chrome chromePath");
    System.err.println("\t-data userDataPath");
    System.err.println("\t-service (use ChromeDriver service)");
    System.err.println("\t-remote http://ipAddress:port (connect to existing ChromeDriver)");
    System.err.println("\t-url URL");
    System.err.println("\t-log logFilePath");
    System.err.println("\t-save htmlFilePath (save page contents to file)");
    System.err.println("\t-debug ipAddress:port");
    System.err.println("\t-name (display browser name)");
    System.err.println("\t-title (display page title)");
    System.err.println("\t-cookies (cookies demo)");
    System.err.println("\t-position (set position demo)");
    System.err.println("\t-size (set size demo)");
    System.err.println("\t-proxy proxyServer:port");
    System.err.println("\t-keep (do not quit ChromeDriver)");
    System.exit(1);
  }

  public static void main(String[] args) throws Exception {
    String driverPath = null;
    boolean useService = false;
    URL remotePort = null;
    ChromeOptions chromeOptions = new ChromeOptions();
    String logPath = null;
    String url = "http://www.google.com/";
    String htmlPath = null;
    boolean name = false;
    boolean title = false;
    boolean quit = true;
    boolean testCookies = false;
    boolean testPosition = false;
    boolean testSize = false;

    for (int argi = 0; argi < args.length; argi++) {
      if (!args[argi].startsWith("-"))
        usage();

      if (args[argi].equals("-driver") && argi + 1 < args.length)
        driverPath = args[++argi];
      else if (args[argi].equals("-chrome") && argi + 1 < args.length)
        chromeOptions.setBinary(args[++argi]);
      else if (args[argi].equals("-data") && argi + 1 < args.length)
        chromeOptions.addArguments("user-data-dir=" + args[++argi]);
      else if (args[argi].equals("-service"))
        useService = true;
      else if (args[argi].equals("-remote") && argi + 1 < args.length)
        remotePort = new URL(args[++argi]);
      else if (args[argi].equals("-url") && argi + 1 < args.length)
        url = args[++argi];
      else if (args[argi].equals("-log") && argi + 1 < args.length)
        logPath = args[++argi];
      else if (args[argi].equals("-save") && argi + 1 < args.length)
        htmlPath = args[++argi];
      else if (args[argi].equals("-debug") && argi + 1 < args.length)
        // Chrome should have been started with --remote-debugging-port=port
        chromeOptions.setExperimentalOption("debuggerAddress", args[++argi]);
      else if (args[argi].equals("-name"))
        name = true;
      else if (args[argi].equals("-title"))
        title = true;
      else if (args[argi].equals("-cookies"))
        testCookies = true;
      else if (args[argi].equals("-position"))
        testPosition = true;
      else if (args[argi].equals("-size"))
        testSize = true;
      else if (args[argi].equals("-proxy") && argi + 1 < args.length) {
        Proxy proxy = new Proxy();
        proxy.setHttpProxy(args[++argi]);
        chromeOptions.setCapability("proxy", proxy);
      }
      else if (args[argi].equals("-keep"))
        quit = false;
      else
        usage();
    }

    if (useService && remotePort != null)
    {
      System.err.println("Can't use both -service and -remote options");
      System.exit(1);
    }

    ChromeDriverService service = null;
    if (remotePort == null) {
      ChromeDriverService.Builder builder = new ChromeDriverService.Builder();
      if (driverPath != null)
        builder
            .usingDriverExecutable(new File(driverPath));
      if (logPath != null)
        builder
            .withLogFile(new File(logPath))
            .withVerbose(true);
      service = builder.build();
    }

    if (useService) {
      service.start();
      remotePort = service.getUrl();
      System.out.println("Service URL: " + remotePort);
    }

    RemoteWebDriver driver;

    if (remotePort != null)
      driver = new RemoteWebDriver(remotePort, chromeOptions);
    else {
      driver = new ChromeDriver(service, chromeOptions);
      /* Alternative code. The following code is probably more commonly seen.
       * However, it is not multi-thread safe, as System.setProperty affects
       * the entire process.
      if (driverPath != null)
        System.setProperty("webdriver.chrome.driver", driverPath);
      if (logPath != null) {
        System.setProperty("webdriver.chrome.logfile", logPath);
        System.setProperty("webdriver.chrome.verboseLogging", "true");
      }
      driver = new ChromeDriver(chromeOptions);
      */
    }

    if (name)
      System.out.println("Browser name: " + driver.getCapabilities().getBrowserName());

    driver.get(url);

    if (title)
    {
      System.out.println("Page title: " + driver.getTitle());
      System.out.println("Page URL: " + driver.getCurrentUrl());
    }

    if (htmlPath != null)
    {
      OutputStreamWriter out = new OutputStreamWriter(
          new FileOutputStream(htmlPath), StandardCharsets.UTF_8);
      out.write(driver.getPageSource());
    }

    if (testCookies)
    {
      driver.manage().addCookie(new Cookie("foo", "bar", "/"));
      System.out.println("Cookies:");
      for (Cookie cookie: driver.manage().getCookies())
        System.out.println("\t" + cookie);
    }

    if (testPosition)
    {
        WebDriver.Window window = driver.manage().window();
        Point position = window.getPosition();
        int x = position.x;
        int y = position.y;
        System.out.printf("Current window position (%d, %d)\n", x, y);

        x += 100;
        y += 100;
        System.out.printf("Attempting to change window position to (%d, %d)\n", x, y);
        window.setPosition(new Point(x, y));

        position = window.getPosition();
        System.out.printf("New window position (%d, %d)\n", position.x, position.y);
    }

    if (testSize)
    {
        WebDriver.Window window = driver.manage().window();
        Dimension size = window.getSize();
        int width = size.width;
        int height = size.height;
        System.out.printf("Current window size %dx%d\n", width, height);

        width /= 2;
        height /= 2;
        System.out.printf("Attempting to change window size to %dx%d\n", width, height);
        window.setSize(new Dimension(width, height));

        size = window.getSize();
        System.out.printf("New window size %dx%d\n", size.width, size.height);
    }

    if (quit)
    {
      Thread.sleep(3000);
      driver.quit();
    }
  }
}
