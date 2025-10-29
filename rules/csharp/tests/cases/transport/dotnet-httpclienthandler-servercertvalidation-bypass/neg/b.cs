using System.Net.Http;

class B
{
    void Run()
    {
        var handler = new HttpClientHandler();
        // default validation, not bypassed
        var client = new HttpClient(handler);
    }
}
