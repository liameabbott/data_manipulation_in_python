# MapReduce_bigrams
A Hadoop MapReduce Python script written using the mrjob Python module to count and analyze bigrams.

The 'bigram_counts_analysis.py' is a MapReduce job containg two steps. 

The first step includes a mapper and a reducer. It takes a text file as input and returns each unique bigram (two-word phrase) in that file and the number of times that bigram occurred in the text file.

The second step also includes both a mapper and a reducer. It takes the bigrams and their counts generated in the first step as input and returns a list containing each unique bigram, and returns the first word of each bigram, coupled with the second word of a bigram beginning with that first word, the number of times that second word occurred after the given first word, and the probability of that second word occurring after the first word (calculated as the number of occurrences of that first word + second word combo, divided by the total number of bigrams beginning with the first word).

As an example to illustrate the process, the 'pg1268.txt' file is parsed using this MapReduce script, resulting in the output 'bigrams_analyzed.txt'.
