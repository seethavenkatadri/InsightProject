

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.JoinWindows;
import org.apache.kafka.streams.kstream.Joined;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KTable;
import org.apache.kafka.streams.kstream.Reducer;
import org.apache.kafka.streams.kstream.ValueJoiner;
import org.apache.kafka.streams.kstream.KGroupedStream;
import org.apache.kafka.streams.KeyValue;
import src.main.java.db.FlightsWithFlyingConditions;
import java.io.IOException;

import org.codehaus.jackson.map.ObjectMapper;




import java.util.Properties;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import org.apache.kafka.streams.kstream.Printed;
import org.json.simple.JSONObject;
import src.main.java.db.DatabaseAccessor;

public class StreamProcessor {




        public static String convertObjectToJSON(FlightsWithFlyingConditions flyingConditions){

            ObjectMapper mapperObj = new ObjectMapper();
            String jsonStr = null;

            try {
                jsonStr = mapperObj.writeValueAsString(flyingConditions);
            } catch (IOException e) {
                e.printStackTrace();
                System.exit(1);
            }
            return jsonStr;
        }


    public static void main(String[] args)  {
        String flightTopic = "topic-flight";
        String weatherTopic = "topic-weather";
        String targetTopic = "topic-flying-conditions";
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "stream-processor");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "ec2-35-160-138-85.us-west-2.compute.amazonaws.com:9092," +
                                                            "ec2-34-218-19-12.us-west-2.compute.amazonaws.com:9092," +
                                                            "ec2-54-148-69-162.us-west-2.compute.amazonaws.com:9092," +
                                                            "ec2-54-149-61-226.us-west-2.compute.amazonaws.com:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

       /* Double latitude = -77.0092;
        Double longitude = 38.889588;


        String nearestStationId = DatabaseAccessor.getNearestStation(latitude, longitude);
        System.out.println("nearest id :" + nearestStationId);*/



        final StreamsBuilder builder = new StreamsBuilder();
        KStream<String, String> flightLines = builder.stream(flightTopic);
        KStream<String, String> weatherLines = builder.stream(weatherTopic);

        KGroupedStream<String, String> weatherGroupedWithStationId = weatherLines.groupByKey();

        KTable<String, String> weatherTable = weatherGroupedWithStationId.reduce(
                new Reducer<String>() {
                    @Override
                    public String apply(String aggValue, String newValue) {
                        return newValue;
                    }
                });


        flightLines.print(Printed.toSysOut());
        weatherLines.print(Printed.toSysOut());


        KStream<String, String> flightsWithNearestStationId = flightLines.map((key, value) -> KeyValue.pair(DatabaseAccessor.getNearestStation(value), value));
        flightsWithNearestStationId.print(Printed.toSysOut());


        KStream<String, FlightsWithFlyingConditions> flightsWithFlyingConditions = flightsWithNearestStationId.leftJoin(weatherTable,
                 new ValueJoiner<String, String, FlightsWithFlyingConditions>() {
                    @Override
                    public FlightsWithFlyingConditions apply(String leftValue, String rightValue) {
                        System.out.println("Inside value joiner:" + leftValue);
                        return new FlightsWithFlyingConditions(leftValue,rightValue);
                    }
                }
        );
        flightsWithFlyingConditions.print(Printed.toSysOut());


        KStream<String, String> flightsWithFlyingConditionsJSON = flightsWithFlyingConditions.mapValues(value -> convertObjectToJSON(value));

        flightsWithFlyingConditionsJSON.print(Printed.toSysOut());

        flightsWithFlyingConditionsJSON.to("topic-flying-conditions");



        final Topology topology = builder.build();

        final KafkaStreams streams = new KafkaStreams(topology, props);
        final CountDownLatch latch = new CountDownLatch(1);

        // attach shutdown handler to catch control-c
        Runtime.getRuntime().addShutdownHook(new Thread("streams-shutdown-hook") {
            @Override
            public void run() {
                streams.close();
                latch.countDown();
            }
        });

        try {
            streams.start();
            latch.await();
        } catch (Throwable e) {
            System.exit(1);
        }
        System.exit(0);
    }
}