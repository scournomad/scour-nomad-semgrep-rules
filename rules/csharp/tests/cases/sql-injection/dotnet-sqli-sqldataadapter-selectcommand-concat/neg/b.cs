using System.Data;
using System.Data.SqlClient;

class B
{
    void Run(string user)
    {
        using var cn = new SqlConnection("Server=.;Trusted_Connection=True;");
        var ad = new SqlDataAdapter();
        string sql = "SELECT * FROM Users WHERE name=@name"; // parameterized
        ad.SelectCommand = new SqlCommand(sql, cn);
        ad.SelectCommand.Parameters.AddWithValue("@name", user);
        var dt = new DataTable();
        ad.Fill(dt);
    }
}
