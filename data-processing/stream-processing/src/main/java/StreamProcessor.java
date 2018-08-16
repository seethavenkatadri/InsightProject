

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.JoinWindows;
import org.apache.kafka.streams.kstream.Joined;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.KeyValue;


import java.util.Dictionary;
import java.util.Properties;
import org.json.JSONObject;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import org.apache.kafka.streams.kstream.Printed;
import src.main.java.db.DatabaseAccessor;

public class StreamProcessor {

    public static void main(String[] args) throws Exception {
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
        Double latitude = -77.0092;
        Double longitude = 38.889588;
        String nearestStationId = DatabaseAccessor.getNearestStation(latitude, longitude);

        System.out.println("nearest id :" + nearestStationId);

        final StreamsBuilder builder = new StreamsBuilder();
        KStream<String, JSONObject> flightLines = builder.stream(flightTopic);
        KStream<String, JSONObject> weatherLines = builder.stream(weatherTopic);
        flightLines.print(Printed.toSysOut());
        weatherLines.print(Printed.toSysOut());

        KStream<String, JSONObject> flightsWithNearestStationId = flightLines.map((key,value) -> KeyValue.pair(DatabaseAccessor.getNearestStation(value.getDouble("latitude"),value.getDouble("longitude")),value));
        flightsWithNearestStationId.print(Printed.toSysOut());






    /*   KStream<String, String> joined = flightLines.join(weatherLines,
                (leftValue, rightValue) -> "left=" + leftValue + ", right=" + rightValue,
                JoinWindows.of(TimeUnit.MINUTES.toMillis(5)),
                Joined.with(
                        Serdes.String(), /* key
                        Serdes.Long(),   /* left value
                        Serdes.Double())  /* right value
        );
*/


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