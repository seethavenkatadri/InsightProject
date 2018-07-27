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
                                            
                                         Amazon S3 -> AWS Athena -> Mapbox 
                                        (Classified Images - Historical data)
## Dataset
Images from Social Media APIs with geolocation

## Engineering challenges
The challenge here will be to receive and prepare streaming images for the machine learning models to feed on, and also to deliver the results of the classification on scale

## Current issues  

- Processing images on a stream applying classification introduces a bottleneck based on algorithmic complexity - handling this is not be a data-engineering problem

- Social media API call restrictions limit the amount of data that can be obtained

## What to do further

- Non-image source of events can be used for the classification algorithm

- Other data sources can be joined with the event data 

## Trade-offs
