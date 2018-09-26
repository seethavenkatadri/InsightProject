# SafeJourney
A real-time data pipeline to track where exactly a flight is affected by bad weather

[Link](bit.ly/safejourney-slides) to the presentation



## Introduction

SafeJourney is a real-time data processing application which delivers flight status information along with weather updates to the end users. With this application, the user can find out where exactly a flight is affected by bad weather. The end users of this application are airport ground station officials that monitor flying conditions and also general users looking for flight status updates.


## Architecture

![alt text](images/architecture.png)

## Dataset

NOAA GSOD weather dataset
</br>
OpenSky Flight status dataset

## Engineering challenges

- Joining two real-time streams of data and handling the frequency difference between them
- Finding the closest weather station for a given flight

## Trade-offs

- Using Postgres to store enriched stream data since PostGIS was needed for geo-spatial capabilities

## Future Work

- Predict Weather conditions for future flights based on historical data
- Experiment with alternatives for PostGIS geo-spatial search
