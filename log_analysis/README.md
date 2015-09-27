# log_analysis

Web access log analysis assignment for SI 601, Data Manipulation course with Professor Yuhang Wang at the University of Michigan, Winter 2015.

See 'SI 601_W15_Homework_2.pdf' file for full description of assignment.

'log_analysis.py' Python script reads Web access logs stored in 'access_log.txt', determines valid lines based on criteria in assignment file above, and counts frequency of valid visits to each high-level domain by day.

The script then writes two files:
  - A tab-delimited .txt file summarizing the counts of valid daily visits to the high-level domains
  - A .txt file containing all invalid lines from the original 'access_log.txt' file
