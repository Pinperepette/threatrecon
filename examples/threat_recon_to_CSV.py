#!/usr/bin/env python

"""
Copyright (C) 2014 by Wapack Labs Corporation
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import threatrecon as tr
import argparse

import csv
import datetime
import time

timestring = time.time()
formatted_timestring = datetime.datetime.fromtimestamp(timestring).strftime('%Y_%m_%d')

search_default = 'serval.essanavy.com'
api_key_default = tr.api.get_api_key() or 'my API key'
output_default = 'TR_search_%s.csv' % formatted_timestring

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Query the ThreatRecon database and write to CSV'
    )
    parser.add_argument(
        'search_indicator',
        default=search_default,
        nargs="?",
        help="indicator to search on"
    )

    parser.add_argument(
        '-f', '--file', '--output-file',
        dest="output_file",
        default=output_default,
        help="File to output to (default %s)" % output_default
    )
    parser.add_argument(
        '-k', '--api-key', '--key',
        dest="api_key",
        default=api_key_default,
        help="your API key (overrides ~/%s)" % (tr.api.API_FILENAME)
    )

    args = parser.parse_args()
    api_key = args.api_key
    search = args.search_indicator
    csvfn = args.output_file

    results = tr.query.raw_query_threat_recon(search, api_key)
    if not results:
        print("There were no results for submission {0}".format(search))
        exit(1)

    with open(csvfn, 'w') as csvfile:
        dw = csv.DictWriter(
            csvfile,
            fieldnames=tr.api.API_FIELDS,
            extrasaction="ignore",
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )

        dw.writeheader()
        dw.writerows(results)

    print '%d records added to %s' % (len(results), csvfn)
    exit(0)
