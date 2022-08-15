<!--
title: 'AWS Python Example'
description: 'This template demonstrates how to deploy a Python function running on AWS Lambda using the traditional Serverless Framework.'
layout: Doc
framework: v3
platform: AWS
language: python
priority: 2
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->


# Eight
This is a serverless endpoint that follows the exponential moving average of eight weekly, used by Augusto Backes for newbies in Crypto Investment. The endpoint will calculate how far your asset is from the average and decide if you should keep, sell or buy. 

## How the decision is made? 
The algorithm will look at the position of the average and the current value, plus the last movement of the days. It will look for pivots and patterns (e.g. doji), from this data the algorithm will answer you.

## Deployment
We have configured the serverless.yaml, so you can easily deploy to your AWS service.
In order to deploy the example, you need to run the following command:

```
$ serverless deploy
```

# ALERT

> :warning: **This is not a recommendation of buy or sell.**: This repository is for study only, and any decision made from the results of this repository is entirely your responsibility!