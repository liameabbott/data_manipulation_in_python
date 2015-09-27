#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import re
import urlparse
import numpy as np


def find_valid_lines(n, access_log_split):
    """Fetches valid lines from formatted access log list 'access_log_split'
       that contains 'n' HTTP requests.

       Returns a one-dimensional array of 1's and 0's with length equal to the
       number of HTTP requests. 1 if the request is valid, 0 if not.

       Also returns a 'domains' list, a list of the domain of each HTTP request
       if it's a valid domain and 'invalid' if it's not a valid domain."""

    urls = [access_log_split[i][6] for i in range(n)]
    parsed_urls = [list(urlparse.urlparse(urls[i])) for i in range(n)]
    url_netlocs = [parsed_urls[i][1] for i in range(n)]

    match_domain = [re.search('^[a-z].*\.([a-z]+)[/:0-9"]*$',
                              url_netlocs[i], re.IGNORECASE) for i in range(n)]
    domains = [match_domain[i].group(1).lower()
               if match_domain[i] else 'invalid' for i in range(n)]
    domain_valid = [1 if domains[i] != 'invalid' else 0 for i in range(n)]

    qs_valid = query_string_check(n, urls)

    verb_valid = verb_check(n, access_log_split)

    access_start_valid = [1 if parsed_urls[i][0] == 'http' or
                          parsed_urls[i][0] == 'https' else 0
                          for i in range(n)]

    status_code_valid = status_code_check(n, access_log_split)

    validity_array = np.array([qs_valid, verb_valid, domain_valid,
                               access_start_valid, status_code_valid])
    valid_line_check = np.cumprod(validity_array, axis=0)[4]

    return valid_line_check, domains


def find_valid_domains(n, valid_line_check, domains):
    """Function is passed the number of HTTP requests 'n', a one-dimensional
       array 'valid_line_check' of length n containing 1 if the request is
       valid and 0 if the request is not valid, and a list of length n
       containing the domain of each request with a valid domain ('invalid' if
       domain of the request is invalid).

       Returns 3 lists:
           - The list of domains for each HTTP request in the
             access log (domain name if request is valid, 'invalid' if request
             is not valid).
           - A list of each unique, valid domain name in the access log.
           - The number of unique, valid domains."""

    valid_domains = [domains[i] if valid_line_check[i] == 1
                     else 'invalid' for i in range(n)]
    uniq_valid_domains = sorted(list(set(valid_domains)))
    uniq_valid_domains.remove('invalid')
    n_valid_domains = len(uniq_valid_domains)

    return valid_domains, uniq_valid_domains, n_valid_domains


def query_string_check(n, urls):
    """Function is passed the number of HTTP requests 'n' and a list
       containing the URL of each request.

       Returns a one-dimensional array of length n with entries of 1
       corresponding to a request with a valid query string in the URL and
       entries of 0 corresponding to a request with an invalid query string in
       the URL."""

    qs = [urlparse.parse_qsl(urls[i]) for i in range(n)]
    qs_max_values = [0] * n
    for i in range(n):
        field_values = [qs[i][k][1] for k in range(len(qs[i]))]
        max_len_value = 0
        for k in range(len(qs[i])):
            if len(field_values[k]) > max_len_value:
                max_len_value = len(field_values[k])
        qs_max_values[i] = max_len_value
    qs_valid = [1 if qs_max_values[i] <= 255 else 0 for i in range(n)]

    return qs_valid


def verb_check(n, access_log_split):
    """Function is passed the formatted access log list and the number of HTTP
       requests in the log.

       Returns a one-dimensional array of length n with entries 1
       corresponding to requests with a valid HTTP verb ('GET' or 'POST') and
       entries 0 corresponding to requests not containing either of these
       verbs."""

    match_verb = [re.search('(GET|POST)', access_log_split[i][5])
                  for i in range(n)]
    verb_valid = [1 if match_verb[i] else 0 for i in range(n)]

    return verb_valid


def status_code_check(n, access_log_split):
    """Function is passed the formatted access log list and the number of HTTP
       requests in the log.

       Returns a one-dimensional array of length n with entries 1
       corresponding to requests with a valid status code ('200') and entries
       0 corresponding to requests without this valid status code."""

    status_codes = [access_log_split[i][7] == '200' or
                    access_log_split[i][8] == '200' for i in range(n)]
    status_code_valid = [1 if status_codes[i] else 0 for i in range(n)]

    return status_code_valid


def find_dates(n, access_log_split):
    """Function is passed the formatted access log list and the number of HTTP
       requests in the log.

       Returns a list of length n containing the date of each HTTP request in
       the access log."""

    match_date = [re.search('\[([^:]+):', access_log_split[i][3])
                  for i in range(n)]
    dates = [match_date[i].group(1) for i in range(n)]

    return dates


def get_domain_counts(n, date, dates, valid_domains, 
                      uniq_valid_domains, n_valid_domains):
    """Takes a given date included in the access log and returns the number of 
       times each valid domain was visited on that date in the log."""
       
    date_domains = [valid_domains[i] for i in range(n)
                    if dates[i] == date
                    if valid_domains[i] != 'invalid']
    date_counts = [str(date_domains.count(uniq_valid_domains[i]))
                   for i in range(n_valid_domains)]
    date_counts.insert(0, date)
    return date_counts


def main():
    """Main function opens file containing access log data, calls functions
       defined above to determine which HTTP requests are valid and to fetch
       the domains of each of those valid requests.

       The function then writes a tab-delimited text file containing the
       unique valid domains and a count of many of the HTTP requests in the
       access log contained that domain. This data is grouped by the date the
       HTTP request was sent.

       The function also writes a tab-delimited text file containing the
       invalid HTTP requests extracted from the original access log."""

    with open('access_log.txt', 'rU') as f:
        access_log = f.readlines()

    n = len(access_log)
    access_log_split = [access_log[i].split() for i in range(n)]

    valid_line_check, domains = find_valid_lines(n, access_log_split)

    dates = find_dates(n, access_log_split)

    valid_domains = find_valid_domains(n, valid_line_check, domains)[0]
    uniq_valid_domains = find_valid_domains(n, valid_line_check, domains)[1]
    n_valid_domains = find_valid_domains(n, valid_line_check, domains)[2]

    invalid_lines = [access_log[i] for i in range(n)
                     if valid_line_check[i] == 0]
                 
    unique_dates = sorted(list(set(dates)))
    date_domain_counts = []
    for date in unique_dates:
        date_counts = get_domain_counts(n, date, dates, valid_domains, 
                                        uniq_valid_domains, n_valid_domains)
        date_domain_counts.append(date_counts)

    uniq_valid_domains.insert(0, 'date')
    header = '\t'.join(uniq_valid_domains)
    date_domain_counts = ['\t'.join(date_domain_counts[i]) 
                          for i in range(len(date_domain_counts))]
    date_domain_counts.insert(0, header)

    with open('valid_log_summary.txt', 'wb') as f:
        f.write('\n'.join(date_domain_counts))

    with open('invalid_access_log.txt', 'wb') as f:
        f.writelines(invalid_lines)

if __name__ == '__main__':
    main()
