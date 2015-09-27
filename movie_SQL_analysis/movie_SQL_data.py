#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import json
import sqlite3 as sqlite

with open('movie_actors_data.txt', 'rU') as f:
    json_data = f.readlines()

movie_genre_list, movies_list, movie_actor_list = [], [], []
for i in range(len(json_data)):
    line_dict = json.loads(json_data[i])
    imdb_id = line_dict['imdb_id']
    genres = line_dict['genres']
    title = line_dict['title']
    year = line_dict['year']
    rating = line_dict['rating']
    actors = line_dict['actors']
    for j in range(len(genres)):
        movie_genre_list.append((imdb_id, genres[j]))
        movies_list.append((imdb_id, title, year, rating))
    for k in range(len(actors)):
        movie_actor_list.append((imdb_id, actors[k]))

with sqlite.connect('movies.db') as con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS movie_genre")
    cur.execute("CREATE TABLE movie_genre(imdb_id TEXT, genre TEXT)")
    cur.executemany("INSERT INTO movie_genre VALUES(?, ?)", movie_genre_list)

    cur.execute("DROP TABLE IF EXISTS movies")
    cur.execute("""CREATE TABLE movies(imdb_id TEXT, title TEXT,
                                       year INT, rating REAL)""")
    cur.executemany("INSERT INTO movies VALUES(?, ?, ?, ?)", movies_list)

    cur.execute("DROP TABLE IF EXISTS movie_actor")
    cur.execute("CREATE TABLE movie_actor(imdb_id TEXT, actor TEXT)")
    cur.executemany("INSERT INTO movie_actor VALUES(?, ?)", movie_actor_list)

    cur.execute("""SELECT genre FROM movie_genre
                   GROUP BY genre ORDER BY COUNT(*) DESC LIMIT 10""")
    rows_1 = cur.fetchall()

    cur.execute("""SELECT title, year, rating
                   FROM movie_genre AS mg JOIN movies AS m
                   ON (mg.imdb_id = m.imdb_id)
                   WHERE genre IS 'Fantasy' ORDER BY rating DESC, year DESC""")
    rows_2 = cur.fetchall()
    rows_2.insert(0, ('Title', 'Year', 'Rating'))

    cur.execute("""SELECT actor, COUNT(*) AS ct
                    FROM movie_actor AS ma JOIN movie_genre AS mg
                    ON (ma.imdb_id = mg.imdb_id)
                    WHERE genre is 'Comedy'
                    GROUP BY actor
                    ORDER BY ct DESC LIMIT 10""")
    rows_3 = cur.fetchall()
    rows_3.insert(0, ('Actor', 'Movies'))

    cur.execute("""SELECT ma1.actor, ma2.actor, COUNT(ma1.actor) AS ct
                    FROM movie_actor AS ma1 JOIN movie_actor AS ma2
                    ON (ma1.imdb_id = ma2.imdb_id)
                    WHERE ma1.actor < ma2.actor
                    GROUP BY ma1.actor, ma2.actor
                    ORDER BY ct DESC LIMIT 20
                    """)
    rows_4 = cur.fetchall()
    rows_4.insert(0, ('Actor A', 'Actor B', 'Co-starred Movies'))

with open('top10_genres.txt', 'wb') as f:
    f.write('Top 10 genres:' + '\n')
    for row in rows_1:
        f.write(row[0]+'\n')

with open('fantasy_movies.txt', 'wb') as f:
    f.write('Fantasy movies:' + '\n')
    for row in rows_2:
        f.write(row[0].encode('utf8') + ', ' + str(row[1]) +
                                        ', ' + str(row[2]) + '\n')

with open('top10_comedy_actors.txt', 'wb') as f:
    f.write('Top 10 most productive comedy actors:' + '\n')
    for row in rows_3:
        f.write(row[0].encode('utf8') + ', ' + str(row[1]) + '\n')

with open('top20_actor_pairs.txt', 'wb') as f:
    f.write("""Top 20 most frequent pairs of actors who co-starred in
                the same movie:""" + '\n')
    for row in rows_4:
        f.write(row[0].encode('utf8') + ', ' + row[1].encode('utf8') +
                                        ', ' + str(row[2]) + '\n')
