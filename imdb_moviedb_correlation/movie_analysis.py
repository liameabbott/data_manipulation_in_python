#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import json
import time
import csv


def find_imdb_top250_html(url):

    response = urllib2.urlopen(url)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc)
    html_str = soup.prettify()
    html_utf8_str = html_str.encode('utf8')

    return html_utf8_str, soup


def find_top100_id_title_rating(soup):

    id_list, title_list, rating_list = [], [], []

    a_tags = soup.find_all('a')
    for i in range(1, len(a_tags), 2):
        if a_tags[i].get('href').startswith('/title/'):
            id_list.append(a_tags[i].get('href')[7:16])
            title_list.append(a_tags[i].string.encode('utf8'))

    strong_tags = soup.find_all('strong')
    for i in range(1, len(strong_tags)):
        rating_list.append(strong_tags[i].string.encode('utf8'))

    top100_ids = id_list[0:100]
    top100_titles = title_list[0:100]
    top100_ratings = rating_list[0:100]

    return zip(top100_ids, top100_titles, top100_ratings)


def find_moviedb_json_str(top100_id_title_rating):

    api_key = 'b969c3e2e3aaad3281ca834f0cc9e504'
    root = 'http://api.themoviedb.org/3/find/'
    end = '&external_source=imdb_id'

    id_moviedb_json_str = []
    for i in range(100):
        moviedb_url = root + top100_id_title_rating[i][0] + '?api_key=' + \
                      api_key + end
        response = urllib2.urlopen(moviedb_url)
        id_moviedb_json_str.append([top100_id_title_rating[i][0],
                                    response.read()])
        time.sleep(10)

    return id_moviedb_json_str


def find_moviedb_rating(id_moviedb_json_str):

    moviedb_ratings = []
    for i in range(100):
        dict_response = json.loads(id_moviedb_json_str[i][1])
        vote_avg = dict_response['movie_results'][0]['vote_average']
        moviedb_ratings.append(vote_avg)

    return moviedb_ratings


def main():

    url = 'http://www.imdb.com/chart/top'
    imdb_top250_html, soup = find_imdb_top250_html(url)

    top100_id_title_rating = find_top100_id_title_rating(soup)

    id_moviedb_json_str = find_moviedb_json_str(top100_id_title_rating)

    moviedb_rating = find_moviedb_rating(id_moviedb_json_str)

    top100_with_moviedb_rating = [[top100_id_title_rating[i][0],
                                   top100_id_title_rating[i][1],
                                   top100_id_title_rating[i][2],
                                   moviedb_rating[i]] for i in range(100)]

    with open('si601_hw3_part2_step1_leabbott.html', 'wb') as f:
        f.write(imdb_top250_html)

    with open('si601_hw3_part2_step2_leabbott.txt', 'wb') as f:
        for line in top100_id_title_rating:
            f.write('\t'.join(line) + '\n')

    with open('si601_hw3_part2_step3_leabbott.txt', 'wb') as f:
        for line in id_moviedb_json_str:
            f.write('\t'.join(line) + '\n')

    with open('si601_hw3_part2_step4_leabbott.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['IMDB ID', 'title', 'IMDB rating',
                         'themoviedb rating'])
        for row in top100_with_moviedb_rating:
            writer.writerow(row)

if __name__ == '__main__':
    main()
