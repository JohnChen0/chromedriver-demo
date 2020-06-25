using System;
using System.Drawing;
using System.IO;
using System.Threading;

using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Remote;

class ChromeDriverTest
{
    static void Usage()
    {
        Console.Error.WriteLine("usage: \"{0}\" [optins...]", Environment.GetCommandLineArgs()[0]);
        Console.Error.WriteLine("\t-driver driverPath");
        Console.Error.WriteLine("\t-chrome chromePath");
        Console.Error.WriteLine("\t-data userDataPath");
        Console.Error.WriteLine("\t-service (use ChromeDriver service)");
        Console.Error.WriteLine("\t-remote http://ipAddress:port (connect to existing ChromeDriver)");
        Console.Error.WriteLine("\t-url URL");
        Console.Error.WriteLine("\t-log logFilePath");
        Console.Error.WriteLine("\t-append (append to existing log file)");
        Console.Error.WriteLine("\t-save htmlFilePath (save page contents to file)");
        Console.Error.WriteLine("\t-debug ipAddress:port");
        Console.Error.WriteLine("\t-name (display browser name)");
        Console.Error.WriteLine("\t-title (display page title)");
        Console.Error.WriteLine("\t-cookies (cookies demo)");
        Console.Error.WriteLine("\t-position (set position demo)");
        Console.Error.WriteLine("\t-size (set size demo)");
        Console.Error.WriteLine("\t-keep (do not quit ChromeDriver)");
        Environment.Exit(1);
    }

    static void Main(string[] args)
    {
        string executablePath = null;
        string executableName = null;
        bool useService = false;
        Uri remotePort = null;
        ChromeOptions chromeOptions = new ChromeOptions();
        string logPath = null;
        string url = "http://www.google.com/";
        string htmlPath = null;
        bool append = false;
        bool name = false;
        bool title = false;
        bool quit = true;
        bool testCookies = false;
        bool testPosition = false;
        bool testSize = false;

        for (int argi = 0; argi < args.Length; argi++)
        {
            if (!args[argi].StartsWith("-"))
                Usage();

            if (args[argi] == "-driver" && argi + 1 < args.Length)
            {
                executablePath = Path.GetFullPath(args[++argi]);
                if (File.Exists(executablePath))
                {
                    executableName = Path.GetFileName(executablePath);
                    executablePath = Path.GetDirectoryName(executablePath);
                }
            }
            else if (args[argi] == "-chrome" && argi + 1 < args.Length)
                chromeOptions.BinaryLocation = args[++argi];
            else if (args[argi] == "-data" && argi + 1 < args.Length)
                chromeOptions.AddArgument("user-data-dir=" + args[++argi]);
            else if (args[argi] == "-service")
                useService = true;
            else if (args[argi] == "-remote" && argi + 1 < args.Length)
                remotePort = new Uri(args[++argi]);
            else if (args[argi] == "-url" && argi + 1 < args.Length)
                url = args[++argi];
            else if (args[argi] == "-log" && argi + 1 < args.Length)
                logPath = args[++argi];
            else if (args[argi] == "-append")
                append = true;
            else if (args[argi] == "-save" && argi + 1 < args.Length)
                htmlPath = args[++argi];
            else if (args[argi] == "-debug" && argi + 1 < args.Length)
            {
                // Chrome should have been started with --remote-debugging-port=port
                chromeOptions.DebuggerAddress = args[++argi];
            }
            else if (args[argi] == "-name")
                name = true;
            else if (args[argi] == "-title")
                title = true;
            else if (args[argi] == "-cookies")
                testCookies = true;
            else if (args[argi] == "-position")
                testPosition = true;
            else if (args[argi] == "-size")
                testSize = true;
            else if (args[argi] == "-keep")
                quit = false;
            else
                Usage();
        }

        if (useService && remotePort != null)
        {
            Console.Error.WriteLine("Can't use both -service and -remote options");
            Environment.Exit(1);
        }

        ChromeDriverService service =
            executablePath == null ? ChromeDriverService.CreateDefaultService() :
            executableName == null ? ChromeDriverService.CreateDefaultService(executablePath) :
                                        ChromeDriverService.CreateDefaultService(executablePath, executableName);
        if (logPath != null)
        {
            service.LogPath = logPath;
            service.EnableVerboseLogging = true;
        }

        if (append)
            service.EnableAppendLog = true;

        if (useService)
        {
            service.Start();
            remotePort = service.ServiceUrl;
            Console.WriteLine("Service URL: {0}", remotePort);
        }

        RemoteWebDriver driver;

        if (remotePort != null)
            driver = new RemoteWebDriver(remotePort, chromeOptions);
        else
            driver = new ChromeDriver(service, chromeOptions);

        if (name)
            Console.WriteLine("Browser name: {0}", driver.Capabilities.GetCapability("browserName"));

        driver.Navigate().GoToUrl(url);

        if (title)
        {
            Console.WriteLine("Page title: {0}", driver.Title);
            Console.WriteLine("Page URL: {0}", driver.Url);
        }

        if (htmlPath != null)
        {
            using (TextWriter f = File.CreateText(htmlPath))
            {
                f.Write(driver.PageSource);
            }
        }

        if (testCookies)
        {
            ICookieJar cookieJar = driver.Manage().Cookies;
            cookieJar.AddCookie(new Cookie("foo", "bar", "/"));
            Console.WriteLine("Cookies:");
            foreach (Cookie cookie in cookieJar.AllCookies)
                Console.WriteLine("\t{0}", cookie);
        }

        if (testPosition)
        {
            IWindow window = driver.Manage().Window;
            Point position = window.Position;
            int x = position.X;
            int y = position.Y;
            Console.WriteLine("Current window position ({0}, {1})", x, y);

            x += 100;
            y += 100;
            Console.WriteLine("Attempting to change window position to ({0}, {1})", x, y);
            window.Position = new Point(x, y);

            position = window.Position;
            Console.WriteLine("New window position ({0}, {1})", position.X, position.Y);
        }

        if (testSize)
        {
            IWindow window = driver.Manage().Window;
            Size size = window.Size;
            int width = size.Width;
            int height = size.Height;
            Console.WriteLine("Current window size {0}x{1}", width, height);

            width /= 2;
            height /= 2;
            Console.WriteLine("Attempting to change window size to {0}x{1}", width, height);
            window.Size = new Size(width, height);

            size = window.Size;
            Console.WriteLine("New window size {0}x{1}", size.Width, size.Height);
        }

        if (quit)
        {
            Thread.Sleep(3000);
            driver.Quit();
        }
    }
}
