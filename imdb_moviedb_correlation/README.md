# imdb_moviedb
IMDB and The Movie Database movie analysis assignment for SI 601, Data Manipulation course with Professor Yuhang Wang at the University of Michigan.

The 'movie_analysis.py' script first fetches the top 250 IMDB movies from http://www.imdb.com/chart/top and saves the movies in an HTML file ('imdb_top250.html').

The script then uses the BeautifulSoup module to parse the HTML page, extracting the IMDB_ID, Title, and IMDB Rating for the top 100 movies and writes this information to a tab-delimited text file ('imdb_top100.txt').

Using themoviedb.org API, the script fetches the JSON string of The Movie Database information for each of the top 100 IMDB movies and saves the IMDB ID and the Movie Database JSON string for the top 100 to a text file ('imdb_moviedb_top100.txt'). This step takes some time, as the script pauses for 10 seconds after every HTTP request to themoviedb.org.

Finally, the script opens the 'imdb_moviedb_top100.txt' file, loads the JSON string of each movie, extracts the 'vote_average' numbers from the JSON string, and then joins it with the IMDB rating data based on IMDB IDs. The IMDB ID, Title, IMDB rating, and Movie Database rating are saved to a CSV file ('imdb_moviedb_ratings.csv').

The 'imdb_moviedb_plot.pdf' chart shows the correlation between IMDB and The Movie Database ratings.

The full assignment can be read in Part 2 of the 'SI601_Winter2015_Homework_3.pdf' file.
