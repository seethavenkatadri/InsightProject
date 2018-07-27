# Real-time Image classification on scale

Global representation of events that are happening with real-time feedback from publicly posted Social Media images. 

[Link](#) to your presentation.

<hr/>

## How to install and get it up and running


<hr/>

## Introduction
The idea of this project is to build a representation of global events that are happening and will be happening using images available publicly.
## Architecture
For current events

Amazon S3 -> Kafka -> Spark Streaming -> Cassandra -> Spark MLLib -> Mapbox 

For getting historical data to recommend future events

Amazon S3 -> Kafka -> Spark Streaming -> Amazon S3 -> AWS Athena -> Mapbox 

## Dataset
Data to be pulled using Social Media APIs that are source of images with geolocation
## Engineering challenges
The challenge here will be to receive and prepare streaming images for the machine learning models to feed on, and also to deliver the results of the classification on scale

## Trade-offs
