using Microsoft.AspNetCore.Mvc;

public class HomeController : Controller
{
    public IActionResult Raw(string html)
    {
        // variable content returned as text/html
        return Content(html, "text/html");
    }
}
