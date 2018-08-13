import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.PreparedStatement;

public class DatabaseAccessor {

    public static void main(String[] args) {
        String url = "jdbc:postgresql://localhost/DB_MAIN_SCHEMA";
        String dbuser = "postgres";
        String dbpwd = "postgres";
        Connection conn = null;
        PreparedStatement st = null;
        ResultSet rs = null;
        String stationid = "707099999";

        try {
            conn = DriverManager.getConnection(url, dbuser,dbpwd);
            st = conn.prepareStatement("SELECT * FROM weather_station WHERE stationid = ?");
            st.setString(1, stationid);
        } catch (SQLException e) {
            System.err.println("Connection initialization failed, aborting.");
            e.printStackTrace();
            System.exit(1);
            // signal the compiler that code flow ends here:
            throw new AssertionError();
        }

        try {
            rs = st.executeQuery();
            while (rs.next()) {
                System.out.print("Column 1 returned ");
                System.out.println(rs.getString(1));
            }
        } catch (SQLException e) {
            System.err.println("Select failed: " + e.getMessage());
            System.exit(1);
            // Signal the compiler that code flow ends here.
            return;
        }
        try {
        rs.close();
        st.close();
        }
        catch (SQLException e) {
        System.err.println("Close failed: " + e.getMessage());
        System.exit(1);
        // Signal the compiler that code flow ends here.
        return;
        }
    }
}
