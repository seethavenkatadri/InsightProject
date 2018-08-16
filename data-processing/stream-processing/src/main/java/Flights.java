import org.json.simple.JSONObject;

public class Flights{
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

        public Double getLatitude() {
        return this.Latitude;
        }

        public Double getLongitude() {
        return this.Latitude;
        }

        public Flights(JSONObject jsonObject){
                this.icao24 = (String) jsonObject.get("icao24");
                this.Latitude = (Double) jsonObject.get("Latitude");
                this.Longitude = (Double) jsonObject.get("Latitude");
                this.Longitude = (Double) jsonObject.get("Latitude");
                this.origin_country = (String) jsonObject.get("origin_country");
                this.velocity = (Double) jsonObject.get("velocity");
                this.true_track = (String) jsonObject.get("true_track");

        }
        }