# Predicting Taxi Out time

## Use Case
Provide an accurate Actual Take-Off Time (ATOT) prediction based on an Actual Off-Block Time (AOBT) and an algorithm-based taxi-out time prediction considering factors such as airport configuration, AC type, weather, etc.

The taxi-time is the time an airplane spends “driving” on the ground: \
• Taxi-in is the time window between the moment the airplane’s wheels touch the ground i.e. the Actual Landing Time (ALDT) and the moment it arrives at its assigned dock i.e. Actual In-Block Time (AIBT). \
• Taxi-out is the time window between the moment the airplane starts moving from its dock i.e. Actual Off-Block Time (AOBT) to the moment its wheels leave the ground i.e. Actual Take-Off Time (ATOT).

## Status Quo
Currently almost every airport around the world is using a moving average approach to predict TOT: the airport assumes that the taxi-out time for a given day will be equal to the average of taxi-outs during the past two months.

## Key Benefits
• Know more accurately when an aircraft will be airborne. \
• Reduce GHG emissions resulting from airplanes’ idle time at the runway entrance. \
• Optimize ground movement and airport flow.