using System.Data;
using System.Data.SqlClient;

class A
{
    void Run(string user)
    {
        var ad = new SqlDataAdapter();
        string sql = "SELECT * FROM Users WHERE name='" + user + "'"; // concat
        ad.SelectCommand = new SqlCommand(sql, new SqlConnection("Server=.;Trusted_Connection=True;"));
        var dt = new DataTable();
        ad.Fill(dt);
    }
}
