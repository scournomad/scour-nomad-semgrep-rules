using Microsoft.AspNetCore.Mvc;

public class HomeController : Controller
{
    public IActionResult Safe(string html)
    {
        // do not render as HTML
        return Content(html, "text/plain");
    }
}
