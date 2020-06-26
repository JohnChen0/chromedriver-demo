import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.interactions.Actions;

class CopyAndPaste {
  public static void main(String[] args) throws Exception {
    ChromeDriver driver = new ChromeDriver();

    driver.executeScript(
        "document.write(\"<input type='text' id='t1' value='Hello World'/>\");"+
        "document.write(\"<br/>\");" +
        "document.write(\"<input type='text' id='t2'/>\");");
    Thread.sleep(1000);

    boolean isMac = System.getProperty("os.name").startsWith("Mac OS");
    Keys key = isMac ? Keys.COMMAND : Keys.CONTROL;
    WebElement box1 = driver.findElement(By.id("t1"));
    WebElement box2 = driver.findElement(By.id("t2"));

    box1.sendKeys(Keys.chord(key, "a"));
    box1.sendKeys(Keys.chord(key, "c"));
    box2.sendKeys(Keys.chord(key, "v"));

    String text1 = box1.getAttribute("value");
    String text2 = box2.getAttribute("value");
    System.out.println("Text1 is " + text1);
    System.out.println("Text2 is " + text2);
    System.out.println(text1.equals(text2) ? "Success" : "FAIL");
    System.out.println();
    Thread.sleep(1000);

    driver.executeScript("arguments[0].value = 'Good-bye'", box1);
    box2.clear();
    Thread.sleep(1000);

    new Actions(driver)
        .click(box1)
        .keyDown(key)
        .sendKeys("ac")
        .keyUp(key)
        .click(box2)
        .keyDown(key)
        .sendKeys("v")
        .keyUp(key)
        .perform();

    text1 = box1.getAttribute("value");
    text2 = box2.getAttribute("value");
    System.out.println("Text1 is " + text1);
    System.out.println("Text2 is " + text2);
    System.out.println(text1.equals(text2) ? "Success" : "FAIL");

    Thread.sleep(1000);
    driver.quit();
  }
}
