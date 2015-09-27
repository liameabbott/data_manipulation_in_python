# movie_SQL_analysis
In this assignment, a SQLite database and tables are created and manipulated using the sqlite3 module in Python.

Using information from the 'movie_actors_data.txt' file, the 'movie_SQL_data.py' script creates a SQLite database 'movies.db' on disk. 

Three tables are created in the database: a 'movie_genre' table containing the IMDB ID and genre of each movie in the text file, a 'movies' table containing the IMDB ID, title, year, and IMDB rating of each movie, and a 'movie_actor' table containing the IMDB ID and actor for each movie (with 1 table entry per actor per movie).

Using SQL queries, these tables are manipulated and information is extracted to create 4 text files containing the following information:
  1)  The top 10 movie genres ('top10_genres.txt')
  2)  The title, year, and IMDB rating of all fantasy movies ('fantasy_movies.txt')
  3)  The top 10 most productive comedy actors/actresses ('top10_comedy_actors.txt')
  4)  The top 20 most frequent pairs of actors/actresses who co-starred in the same movie ('top20_actor_pairs.txt')
  
The full assignment can be seen in Part 1 of 'SI601_Winter2015_Homework_4.pdf'.
