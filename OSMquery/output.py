"""
Osmosint output module

This module deals with every output within Osmosint.
"""
import os
import csv
import sys
import datetime
from utils.utils import exit_prog


def create_google_links(decimal_coordinates):
    """
    Function that takes a list of coordinates and turns them into Google Maps links.

    Args:
        decimal_coordinates (list): List that contains tuples of the coordinates in decimal format.

    Returns: A list that contains all the google maps links associated to the coordinates
    """
    urls = []
    for lat, lon in decimal_coordinates:
        url = f"https://www.google.com/maps?q=loc:{lat},{lon}&hl=en&z=18"
        urls.append(url)
    return urls


def establish_file_header(parameters):
    """
    Builds the header of the file (description of what the results are for) based on the parameters of the query

    args:
        parameters (dict): dictionnary of all the query parameters, to write details about the query

    Returns:
        header (str): description of what the file will include
    """
    if parameters["location"]:
        location = parameters["location"][0]

    if parameters["bbox"]:
        location = parameters["location"]

    match parameters["type_query"]:
        case "locate":
            header = f"Results for all {parameters['tag_1']} in {location}\n\n"
        case "radius":
            header = f"Results for all {parameters['tag_1']} in a {parameters['radius']}m radius of {parameters['tag_2']} in {location}\n\n"

    return header
    

def write_results_file(data, parameters, file_name, format='txt', data_types=[]):
    """
    Function that writes data in a specific file
    First goes through the format to chose for the file.
    Then goes through the data_types list (either "decimal", "dms" or "urls")
    For each data_type, goes through the dictionary's associated list and write every element in the file

    args:
        data (dict): dict of the data to write. Format is {output_format:[list of coordinates/url]}
        parameters (dict): dictionnary of all the query parameters, to write the header about the query
        file_name (str) : name of the file
        format='text' (callable) : by default it writes a txt file, unless csv specifically mentioned
        data_types (str) : by default the program writes coordinates, unless url is specifically mentioned

    Returns nothing, but writes data in the file.
    """
    
    mode = 'a' if os.path.exists(file_name) else 'w'
    current_time = datetime.datetime.now().strftime("%d/%m at %H:%M")

    header = establish_file_header(parameters)
    
    if format == 'csv':
        # For DMS coords, file writing is harder because of special characters ° and ".
        # To handle °, added utf-16 and the Byte Order Mark
        # Harder to find something for ", so the file writing is done with '\', and the the user has to
        # manually replace all \ with nothing to make the coordinates readable.
        try:
            with open(file_name, mode, newline='', encoding='utf-16') as file:
                file.write('\ufeff') # Adding a Byte Order Mark to handle filewriting of special characters (DMS coords)
                writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
                
                writer.writerow([header])
                        
                for data_type in data_types:
                    
                    if data_type == 'decimal':
                        writer.writerow(['Coordinates in Decimal Format:'])
                        for lat, lon in data.get(data_type, []):
                            writer.writerow([lat, lon])
                            
                    elif data_type == 'dms':
                        writer.writerow(['Coordinates in DMS Format:'])
                        for lat, lon in data.get(data_type, []):
                            writer.writerow([lat, lon])
                            
                    elif data_type == 'urls':
                        writer.writerow(['Google Maps URLs'])
                        for url in data.get('urls', []):
                            writer.writerow([url])
        except PermissionError:
            print("Permission to write in the Result.csv file was denied. Close the file and try again.")
            exit_prog()
    
    else:  # By default --> text format
        with open(file_name, mode, encoding='utf-8') as file:
            file.write(f"Query from the {current_time}\n")
            file.write(header)

            for data_type in data_types:
                
                if data_type == 'decimal':
                    file.write("Coordinates in Decimal Format:\n")
                    for lat, lon in data.get(data_type, []):
                        file.write(f"{lat}, {lon}\n")
                        
                elif data_type == 'dms':
                    file.write("Coordinates in DMS Format:\n")
                    for lat, lon in data.get(data_type, []):
                        file.write(f"{lat}, {lon}\n")
                        
                elif data_type == 'urls':
                    file.write("Google Maps URLs:\n")
                    for url in data.get('urls', []):
                        file.write(f"{url}\n")
                file.write("\n\n")

    print("\nFile writing completed!")
    print(f"You can access your results in the 'Results.{format}' file.")


def check_if_results(query_result, parameters):
    """
    Function that checks whether the OSM query found results.
    Prints custom return message if not.

    args:
        query_result (list): results from the query (list of coordinates)
        parameters (dict): dictionary with all the parameters, used to send custom message if no found

    Returns:
        True if result, False if not
    """
    if len(query_result) == 0:
        match parameters["type_query"]:
            case 'locate':
                if parameters["location"]:
                    print(f"\nThe query found 0 {parameters['tag_1']} in {parameters['location'][0]}.")
                elif parameters["bbox"]:
                    print(f"\nThe query found 0 {parameters['tag_1']} in the following bbox {parameters['bbox']}.")
            case 'radius':
                if parameters["location"]:
                    print(f"\nThe query found 0 {parameters['tag_1']} within a {parameters['radius']}m radius of a "
                            f"{parameters['tag_2']} in {parameters['location'][0]}.")
                elif parameters["bbox"]:
                    print(f"\nThe query found 0 {parameters['tag_1']} within a {parameters['radius']}m radius of a "
                            f"{parameters['tag_2']} in this bbox : {parameters['bbox']}.")
        print("\nMake sure that the parameters you entered are correct: ")
        for key, value in parameters.items():
            if value != None and value != False:
                print(f"    {key} : {value}")
        print("If you are certain that the query should yield result and the parameters are correct, visit the documentation to troubleshoot what could be wrong.")
        sys.exit()
        return False
            
    else:
        return True


def check_len_results(results, threshold):
    """
    Function that checks whether the query returned more results than the limit allowed

    args:
        results (list): result from the api in decimal format
        threshold (int): maximal number of result

    Returns:
        False if the query did not return more than the limit
        True if the query returned more than the limit and the user decided to get the results in a file.
        Exits the program if the query returned more than then limit and the user decided to leave.
    """
    from input.input import get_input
    len_results = len(results)

    if len_results <= threshold:
        return False
    elif len_results > threshold:
        while True:
            print(f"\nThe query returned {len_results} results. This is over the maximum threshold for printing ({threshold}).")
            print("\nOptions:")
            print("1. Print all results in a file")
            print("2. Cancel (all unsaved data will be lost)")
            choice = get_input(">> Enter your choice: ", int, [1, 2])
            match choice:
                case 1:
                    return True
                case 2:
                    exit_prog()
            

def output_results(raw_results, parameters):
    """
    Output the result based on user's decisions
    Can print and file_write, and can display either decimal coordinates, dms coordinates or google maps urls
    args:
        raw_results (list): list of tuples [(latitude1, longitude1), (latitude2, longitude2)]
        parameters (dict): dictionary with all the parameters.
    
    """
    from convert.conversion import decimal_to_dms

       
    def print_results(results): # Basic print function for printing and prevent redundancy
        try: # If decimal format
            for lat, lon in results:
                print(f"{lat}, {lon}")
        except: # If url format
            for result in results:
                print(result)
            
            print(result)

    def format_results(results, format_type): 
        if format_type == "decimal":
            return [(lat, lon) for lat, lon in results]
        elif format_type == "dms":
            return [decimal_to_dms(lat, lon) for lat, lon in results]
        elif format_type == "urls":
            return create_google_links(results)

    # Handle the format(s) that the user decided for the output
    output_formats = ["decimal", "dms", "urls"]
    selected_formats = []
    for formats in output_formats:
        if parameters.get(f"{formats}_coord") or (formats == "urls" and parameters["google_urls"]):
            selected_formats.append(formats)

    if check_len_results(raw_results, 100) == True:
        # Forces the file writing if the results are too big.
        parameters["file_type"] = "txt"
        
    data_to_output = {}
    for formats in selected_formats:
        formatted_results = format_results(raw_results, formats)
        data_to_output[formats] = formatted_results
        if not parameters["file_type"]:
            print(f"\n\nResults in {formats} format:\n")
            print_results(formatted_results)


    if parameters["file_type"]:
        if not data_to_output: # default choice is decimal
            data_to_output["decimal"] = format_results(raw_results, "decimal")
        if not selected_formats:
            selected_formats.append("decimal")
        write_results_file(
            data_to_output,
            parameters,
            f"Results.{parameters['file_type']}",
            parameters['file_type'],
            selected_formats,
            )

    if not selected_formats and not parameters["file_type"]:
        print("\nYou did not specify an output format (-dec, -dms, or -u).\nOutput by default is in decimal format:\n")
        print_results(format_results(raw_results, "decimal"))

    return data_to_output

def welcome(args):
    """
    Function that launches at the start of the program and explains to the user what the query is about to do

    args:
        args: arguments from the parser

    Returns:
        none
    """
    osmosint_ascii = """
   ____                                 _         __ 
  / __ \ _____ ____ ___   ____   _____ (_)____   / /_
 / / / // ___// __ `__ \ / __ \ / ___// // __ \ / __/
/ /_/ /(__  )/ / / / / // /_/ /(__  )/ // / / // /_  
\____//____//_/ /_/ /_/ \____//____//_//_/ /_/ \__/  
                                                     
"""

    welcome_message = "Welcome to Osmosint!\n"
    welcome_message += f"Command: {args.command}\n"
    
    output_format = []

    if not args.command:
        print("Welcome to Osmosint!")
        print("To get an overview of what you can do, enter 'Osmosint.py -h'")
        print("To try a command out, enter 'Osmosint.py locate'")
        return False
    elif args.command == 'convert':
        print(osmosint_ascii)
        print("Welcome to the Osmosint Coordinate Converter!")
        print("""Allowed coordinate formats for conversion: DMS (e.g. 21°07'24.35"N), Decimal (e.g. 21.123431)""")
        print("Input format: latitude, longitude")
        print("Enter exit to leave the program.\n")
        return 'Convert'
 
    if args.google_urls:
        output_format.append("Google Maps URL")
    if args.dms_coords:
        output_format.append("Coordinates in DMS format")
    if args.decimal_coords:
        output_format.append("Coordinates in decimal format")

    if output_format:
        welcome_message += "Output Format: " + ", ".join(output_format) + "\n"
    else:
        welcome_message += "Output Format: None selected, decimal coordinates by default\n"

    print(osmosint_ascii)
    print(welcome_message)
