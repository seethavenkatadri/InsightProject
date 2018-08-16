package src.main.java.db;
import org.json.simple.JSONObject;
import src.main.java.db.DatabaseAccessor;

public class FlightsWithFlyingConditions {

    private String icao24;
    private String callsign;
    private String origin_country;
    private String time_position;
    private String last_contact;
    private Double Longitude;
    private Double Latitude;
    private String geo_altitude;
    private Boolean on_ground;
    private Double velocity;
    private String true_track;
    private Double vertical_rate;
    private String sensors;
    private String baro_altitude;
    private String squawk;
    private String spi;
    private String position_source;
    private String inputTime;


    private String stationId;
    private String usaf;
    private String wban;
    private String Elevation;
    private String Country_Code;
    private Double WLatitude;
    private Double WLongitude;
    private String Date;
    private String Year;
    private String Month;
    private String Day;
    private String Mean_Temp;
    private Integer Mean_Temp_Count;
    private String Mean_Dewpoint;
    private Integer Mean_Dewpoint_Count;
    private String Mean_Sea_Level_Pressure;
    private Integer Mean_Sea_Level_Pressure_Count;
    private String Mean_Station_Pressure;
    private Integer Mean_Station_Pressure_Count;
    private Double Mean_Visibility;
    private Integer Mean_Visibility_Count;
    private Double Mean_Windspeed;
    private Integer Mean_Windspeed_Count;
    private String Max_Windspeed;
    private String Max_Gust;
    private Double Max_Temp;
    private String Max_Temp_Quality_Flag;
    private Double Min_Temp;
    private String Min_Temp_Quality_Flag;
    private String Precipitation;
    private String Precip_Flag;
    private String Snow_Depth;
    private String Fog;
    private Boolean Rain_or_Drizzle;
    private Boolean Snow_or_Ice;
    private Boolean Hail;
    private Boolean Thunder;
    private Boolean Tornado;
    private String WInputTime;

    private Double FlyingConditionsIndex;

    private Double getFlyingConditions(Double visibility,Double windSpeed){
        Double flyingConditions = 0.0;
        flyingConditions = windSpeed / visibility;
        return flyingConditions;

    }

    public FlightsWithFlyingConditions(String flight, String weather) {
        JSONObject flightObject = DatabaseAccessor.convertStringToJson(flight);
        JSONObject weatherObject = DatabaseAccessor.convertStringToJson(weather);
        this.icao24 = (String) flightObject.get("icao24");
        this.Latitude = (Double) flightObject.get("Latitude");
        this.Longitude = (Double) flightObject.get("Latitude");
        this.Longitude = (Double) flightObject.get("Latitude");
        this.origin_country = (String) flightObject.get("origin_country");
        this.velocity = (Double) flightObject.get("velocity");
        this.true_track = (String) flightObject.get("true_track");
        this.stationId = (String) weatherObject.get("ID");
        this.Mean_Visibility = (Double) weatherObject.get("Mean_Visibility");
        this.Mean_Windspeed = (Double) weatherObject.get("Mean_Windspeed");
        this.Max_Temp = (Double) weatherObject.get("Max_Temp");
        this.Min_Temp = (Double) weatherObject.get("Min_Temp");
        this.Precipitation = (String) weatherObject.get("Precipitation");
        this.inputTime = (String) flightObject.get("inputTime");
        System.out.println("Inside constructor");
        this.FlyingConditionsIndex = getFlyingConditions(this.Mean_Visibility,this.Mean_Windspeed);
    }

}