# Hurricanes tracking analytics

Author: @azurevolver, @katyyhc, @chienju-chen

* This project aims to answer the following questions.
 1. Compute and output the total distance the storm was tracked in nautical miles.
 2. Calculate the speed in knots that the storm center moved, a.k.a “storm propagation” (from latitudes,
longitudes, and time lags) between data rows, but don’t output these details. Propagation is not derived from wind speed! From this series, compute and output maximum and mean (average) propagation speeds per storm in knots.
 3. Make a function that takes any fixed point (latitude & longitude), supplied by the program user, and lists all storms that directly affected that location with hurricane-level winds (>=64kt). The location might represent a specific city or island or whatever.


* Raw Data format: 

AL152017,              MARIA,     68,\n
20170916, 1200,  , TD, 12.2N,  49.7W,  30, 1006,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,\n
20170916, 1800,  , TS, 12.2N,  51.7W,  40, 1004,   40,    0,    0,   40,    0,    0,    0,    0,    0,    0,    0,    0,\n
20170917, 0000,  , TS, 12.4N,  53.1W,  45, 1002,   40,   30,    0,   40,    0,    0,    0,    0,    0,    0,    0,    0,\n
20170917, 0600,  , TS, 12.8N,  54.4W,  55,  994,   50,   40,    0,   50,   20,   20,    0,   20,    0,    0,    0,    0,\n
20170917, 1200,  , TS, 13.3N,  55.7W,  60,  990,   60,   40,   30,   50,   30,   20,    0,   20,    0,    0,    0,    0,\n


* Data sources (Retrieved from https://www.nhc.noaa.gov/data/)
  1. The Atlantic hurricane database (1851-2018)
  2. Northeast and North Central Pacific hurricane database (HURDAT2) 1949-2018 from National Hurricane Center 


* Work Split: 

All of the members discussed the requirements and wrote pseudo code together.
Based on @azurevolver assignment 1, @azurevolver finished the functions for problem1,
@katyyhc finished the functions for problem2, @chienju-chen and @azurevolver finished the functions for problem3.
All of the members completed "process_storm_data" function together.
