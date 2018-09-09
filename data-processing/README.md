# Stream Processing

Stream Processing is implemented using Kafka Streams API

- The flight data is processed as a KStream
- The weather data is aggregated into a Changelog Stream, i.e. KTable
- Flight Stream and Weather Table are joined using a LeftJoin to get all flight data
- The enriched flight stream and latest weather updates are written into output topics

