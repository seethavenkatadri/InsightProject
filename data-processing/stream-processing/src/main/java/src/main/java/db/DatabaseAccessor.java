package src.main.java.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.PreparedStatement;

public class DatabaseAccessor {

    public static String  getNearestStation(Double latitude, Double longitude) {
        String url = "jdbc:postgresql://localhost/postgres";
        String dbuser = "postgres";
        String dbpwd = "postgres";
        Connection conn = null;
        PreparedStatement st = null;
        ResultSet rs = null;
        String stationId = null;

        try
        {
            Class.forName("org.postgresql.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

        try {
            conn = DriverManager.getConnection(url, dbuser,dbpwd);
            st = conn.prepareStatement("SELECT stationid FROM (SELECT stationid, distance FROM (SELECT stationid,ST_Distance(point1, point2) distance FROM (SELECT stationid,geolocation point1, ST_GeogFromText('SRID=4326;POINT(? ?)') point2 FROM weather_station) a) b ORDER BY distance DESC) c limit 1;");
            st.setDouble(1, latitude);
            st.setDouble(2, longitude);
        } catch (SQLException e) {
            System.err.println("Connection initialization failed, aborting.");
            e.printStackTrace();
            System.exit(1);
            // signal the compiler that code flow ends here:
            throw new AssertionError();
        }

        try {
            rs = st.executeQuery();
            stationId = rs.getString(1);
            System.out.print("Nearest station: "+stationId);
            while (rs.next()) {
                System.out.print("Column 1 returned ");
                stationId = rs.getString(1);
                System.out.print("Nearest station: "+stationId);
            }
        } catch (SQLException e) {
            System.err.println("Select failed: " + e.getMessage());
            System.exit(1);
            // Signal the compiler that code flow ends here.
            return "error";
        }
        try {
        rs.close();
        st.close();
        }
        catch (SQLException e) {
        System.err.println("Close failed: " + e.getMessage());
        System.exit(1);
        // Signal the compiler that code flow ends here.
        return "error";
        }
        return stationId;
    }

}
