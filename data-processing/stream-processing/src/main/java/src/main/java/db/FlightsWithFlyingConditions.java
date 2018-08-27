package src.main.java.db;
import org.json.simple.JSONObject;
import src.main.java.db.DatabaseAccessor;

public class FlightsWithFlyingConditions {

    private String icao24;
    private String origin;
    private String longitude;
    private String latitude;
    private String velocity;
    private String track;
    private String inputTime;

    private String stationId;
    private Double visibility;
    private Double windspeed;
    private Double maxTemp;
    private Double minTemp;
    private String precipitation;

    private Double flyingConditionsIndex;

    public String getIcao24() {
        return this.icao24;
    }

    public String getOrigin() {
        return this.origin;
    }
    public String getLatitude() {
        return this.latitude;
    }
    public String getLongitude() {
        return this.longitude;
    }
    public String getVelocity() {
        return this.velocity;
    }
    public String getTrack() {
        return this.track;
    }
    public String getInputTime() {
        return this.inputTime;
    }

    public String getStationId() {
        return this.stationId;
    }
    public Double getVisibility() {
        return this.visibility;
    }
    public Double getWindspeed() {
        return this.windspeed;
    }
    public Double getMaxTemp() {
        return this.maxTemp;
    }
    public Double getMinTemp() {
        return this.minTemp;
    }
    public String getPrecipitation() {
        return this.precipitation;
    }
    public Double getFlyingConditionsIndex() {
        return this.flyingConditionsIndex;
    }

/*  private String callsign;
    private String time_position;
    private String last_contact;
    private String geo_altitude;
    private Boolean on_ground;
    private String vertical_rate;
    private String sensors;
    private String baro_altitude;
    private String squawk;
    private String spi;
    private String position_source;*/

   /* private String usaf;
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
    private Integer Mean_Visibility_Count;
    private Integer Mean_Windspeed_Count;
    private String Max_Windspeed;
    private String Max_Gust;
    private String Max_Temp_Quality_Flag;
    private String Min_Temp_Quality_Flag;
    private String Precip_Flag;
    private String Snow_Depth;
    private String Fog;
    private Boolean Rain_or_Drizzle;
    private Boolean Snow_or_Ice;
    private Boolean Hail;
    private Boolean Thunder;
    private Boolean Tornado;
    private String WInputTime;*/



    private Double getFlyingConditions(Double visibility,Double windSpeed){
        Double flyingConditions = 0.0;
        flyingConditions = windSpeed / visibility;
        return flyingConditions;

    }

    public FlightsWithFlyingConditions(String flight, String weather) {
        System.out.println("Inside constructor");
        System.out.println("flight:" + flight);
        System.out.println("weather:" + weather);



        if (flight != null) {
            JSONObject flightObject = DatabaseAccessor.convertStringToJson(flight);
            this.icao24 = (String) flightObject.get("icao24");
            this.latitude = (String) flightObject.get("latitude");
            this.longitude = (String) flightObject.get("longitude");
            this.origin = (String) flightObject.get("origin_country");
            this.velocity = (String) flightObject.get("velocity");
            this.track = (String) flightObject.get("true_track");
            this.inputTime = (String) flightObject.get("inputTime");
        }
        if (weather != null) {
            JSONObject weatherObject = DatabaseAccessor.convertStringToJson(weather);
            System.out.println("Station id : " + (String) weatherObject.get("ID"));
            this.stationId = (String) weatherObject.get("ID");
            this.visibility = (Double) weatherObject.get("Mean_Visibility");
            this.windspeed = (Double) weatherObject.get("Mean_Windspeed");
            this.maxTemp = (Double) weatherObject.get("Max_Temp");
            this.minTemp = (Double) weatherObject.get("Min_Temp");
            this.precipitation = (String) weatherObject.get("Precipitation");
            this.flyingConditionsIndex = getFlyingConditions(this.visibility,this.windspeed);
        }



    }

}