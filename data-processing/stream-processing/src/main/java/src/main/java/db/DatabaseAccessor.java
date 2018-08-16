package src.main.java.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.PreparedStatement;
import org.json.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class DatabaseAccessor {

    public static String  getNearestStation(String jsonAsString) {
        String url = "jdbc:postgresql://localhost/postgres";
        String dbuser = "postgres";
        String dbpwd = "postgres";
        Connection conn = null;
        PreparedStatement st = null;
        ResultSet rs = null;
        String stationId = null;
        JSONParser parser = new JSONParser();
        JSONObject jsonObject = null;

        try {
            jsonObject = (JSONObject) parser.parse(jsonAsString);
        } catch (ParseException e)
        {
            System.err.println("JSON parse failed: " + e.getMessage());
            System.exit(1);
            // Signal the compiler that code flow ends here.
            return "error";
        }


        try
        {
            Class.forName("org.postgresql.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

        try {
            conn = DriverManager.getConnection(url, dbuser,dbpwd);
            st = conn.prepareStatement("SELECT stationid FROM (SELECT stationid, distance FROM (SELECT stationid,ST_Distance(point1, point2) distance FROM (SELECT stationid,geolocation point1, ST_GeogFromText('SRID=4326;POINT("+jsonObject.getDouble("latitude")+" "+jsonObject.getDouble("longitude")+")') point2 FROM weather_station) a) b ORDER BY distance DESC) c limit 1;");
         //   st.setDouble(1, latitude);
         //   st.setDouble(2, longitude);
        } catch (SQLException e) {
            System.err.println("Select failed.");
            e.printStackTrace();
            System.exit(1);
            // signal the compiler that code flow ends here:
            throw new AssertionError();
        }

        try {
            rs = st.executeQuery();
            while (rs.next()) {
                System.out.print("Column 1 returned ");
                stationId = rs.getString(1);
                System.out.print("Nearest station: "+stationId);
            }
        } catch (SQLException e) {
            System.err.println("Iteration failed: " + e.getMessage());
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
