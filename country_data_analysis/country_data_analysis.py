#!/usr/bin/env python

import csv
import math
import itertools


def find_avg(all_years_of_indicator_for_single_country):

    non_missing_entries = [x for x in all_years_of_indicator_for_single_country
                           if not math.isnan(x)]
    if len(non_missing_entries) != 0:
        avg = sum(non_missing_entries)/len(non_missing_entries)
    else:
        avg = 0

    return avg


def create_step1_list(n, indices, wbi_countries, wbi_total_pop,
                      wbi_urban_pop, wbi_birth_rate):

    wbi_countries_unique = [wbi_countries[i] for i in indices]

    wbi_avg_total_pop = [find_avg(wbi_total_pop[i:i+n]) for i in indices]

    wbi_avg_urban_pop = [find_avg(wbi_urban_pop[i:i+n]) for i in indices]

    wbi_avg_birth_rate = [find_avg(wbi_birth_rate[i:i+n]) for i in indices]

    avg_urban_pop_ratio = [wbi_avg_urban_pop[i]/wbi_avg_total_pop[i]
                           if wbi_avg_total_pop != 0 else 0
                           for i in range(len(indices))]

    neg_log_avg_birth_rate = [-math.log(wbi_avg_birth_rate[i])
                              if wbi_avg_birth_rate[i] > 0 else 0
                              for i in range(len(indices))]

    full_list = zip(wbi_countries_unique, wbi_avg_total_pop,
                    wbi_avg_urban_pop, wbi_avg_birth_rate,
                    avg_urban_pop_ratio, neg_log_avg_birth_rate)
    full_list_del_missing_data = [row[:3] + row[4:] for row in full_list
                                  if row[1] != 0 if row[2] != 0 if row[3] != 0]

    country_data_step1 = sorted(full_list_del_missing_data,
                                key=lambda x: (-x[3], -x[4]))

    return country_data_step1


def create_step2_list(country_data_step1, wbr_regions, wbr_countries):

    step2_countries_of_interest = [row[0] for row in country_data_step1]

    step2_regions_list = [wbr_regions[wbr_countries.index(country)]
                          if country in wbr_countries else 'No region'
                          for country in step2_countries_of_interest]

    step2_avg_total_pop = [row[1] for row in country_data_step1]

    step2_avg_urban_pop = [row[2] for row in country_data_step1]

    step2_avg_pop_ratio = [row[3] for row in country_data_step1]

    step2_neg_log_birth_rate = [row[4] for row in country_data_step1]

    country_data_step2 = zip(step2_countries_of_interest, step2_regions_list,
                             step2_avg_total_pop, step2_avg_urban_pop,
                             step2_avg_pop_ratio, step2_neg_log_birth_rate)

    return country_data_step2


def create_step3_list(country_data_step2):

    step3_sorted_region = sorted(country_data_step2, key=lambda x: x[1])

    step3_remove_no_region = [row for row in step3_sorted_region
                              if row[1] != 'No region']

    country_data_step3 = []
    for key, region in itertools.groupby(step3_remove_no_region,
                                         lambda x: x[1]):
        current_region, max_country, pop = '', '', 0
        for country in region:
            if country[2] > pop:
                current_region = country[1]
                max_country = country[0]
                pop = country[2]
        country_data_step3.append((current_region, max_country))

    return country_data_step3


def parse_wbi_data(wbi_all_cols):

    for row in wbi_all_cols:
        if row[9] == "":
            row[9] = 'NaN'
        if row[10] == "":
            row[10] = 'NaN'
        if row[11] == "":
            row[11] = 'NaN'

    wbi_countries = [row[0] for row in wbi_all_cols]
    wbi_total_pop = [float(row[9].replace(',', '')) for row in wbi_all_cols]
    wbi_urban_pop = [float(row[10].replace(',', '')) for row in wbi_all_cols]
    wbi_birth_rate = [float(row[11])/1000.0 for row in wbi_all_cols]

    return wbi_countries, wbi_total_pop, wbi_urban_pop, wbi_birth_rate


def parse_wbr_data(wbr_all_cols):

    wbr_regions = [row[0] for row in wbr_all_cols]
    wbr_sub_regions = [row[1] for row in wbr_all_cols]
    wbr_countries = [row[2] for row in wbr_all_cols]

    return wbr_regions, wbr_sub_regions, wbr_countries


def main():

    with open('world_bank_indicators.txt', 'rU') as f:
        next(f)
        wbi_all_cols = [line for line in csv.reader(f, delimiter='\t')]

    with open('world_bank_regions.txt', 'rU') as f:
        next(f)
        wbr_all_cols = [line for line in csv.reader(f, delimiter='\t')]

    wbi_countries = parse_wbi_data(wbi_all_cols)[0]
    wbi_total_pop = parse_wbi_data(wbi_all_cols)[1]
    wbi_urban_pop = parse_wbi_data(wbi_all_cols)[2]
    wbi_birth_rate = parse_wbi_data(wbi_all_cols)[3]

    start_year, end_year = 2000, 2010
    n = end_year - start_year + 1
    indices = range(0, len(wbi_countries), n)

    country_data_step1 = create_step1_list(n, indices, wbi_countries,
                                           wbi_total_pop, wbi_urban_pop,
                                           wbi_birth_rate)

    wbr_regions, wbr_sub_regions, wbr_countries = parse_wbr_data(wbr_all_cols)

    country_data_step2 = create_step2_list(country_data_step1,
                                           wbr_regions, wbr_countries)

    country_data_step3 = create_step3_list(country_data_step2)

    with open('country_data_step1.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['country name', 'average population',
                         'average urban population',
                         'average urban population ratio',
                         'average birth rate'])
        for row in country_data_step1:
            writer.writerow(row)

    with open('country_data_step2.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['country name', 'region', 'average population',
                         'average urban population',
                         'average urban population ratio',
                         'average birth rate'])
        for row in country_data_step2:
            writer.writerow(row)

    with open('country_data_step3.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['region', 'country with highest average population'])
        for row in country_data_step3:
            writer.writerow(row)


if __name__ == '__main__':
    main()
