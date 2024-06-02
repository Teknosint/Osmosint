#! /usr/bin/env python3
"""
Osmosint: Find anything anywhere.

This module is the main module to access anything anywhere.

"""

from input.input import get_query_details
from convert.conversion import convert_coordinates
from OSMquery.output import check_if_results, output_results, welcome
from OSMquery.query import create_query, query_to_api, extract_data_from_result
from utils.utils import parse_args, exit_prog
import sys

def main():
    args = parse_args()

    if welcome(args) == False :  # Welcomes and makes sure that a command has been entered.
        sys.exit()

    if args.command == 'locate' or args.command == 'radius':
        
        query_details = get_query_details(args.command)
        
        parameters = { # Builds the dictionary with information about the query
            "type_query" : args.command,
            "location" : query_details.get('location'),
            "bbox" : query_details.get('bbox'),
            "tag_1" : query_details.get('tag_1'),
            "tag_2" : query_details.get('tag_2'),
            "radius" : query_details.get('radius'),
            "file_type" : args.write_file,
            "google_urls" : args.google_urls,
            "decimal_coord" : args.decimal_coords,
            "dms_coord" : args.dms_coords,
        }
        query = create_query(parameters)
        query_result = query_to_api(query)
        
        if query_result == False:
            exit_prog()
        else:
            extracted_results = extract_data_from_result(query_result)   

        is_result = check_if_results(extracted_results, parameters)
        if is_result == False:
            exit_prog()

        output_results(extracted_results, parameters)

    elif args.command == 'convert':
        while True:
            lat, lon = convert_coordinates()
            if lat:
                print(f"{lat}, {lon}")


if __name__ == "__main__":
    main()
