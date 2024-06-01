"""
Osmosint input module

This module deals with all inputs from the user.
"""
import sys
import re
from convert.conversion import dms_to_decimal
from utils.utils import exit_prog

def get_input(input_prompt, type_func=str, valid_values=None):
    """
    Function to get input from the user, with the option to exit the program by typing 'exit'.

    Args:
        input_prompt (str): The prompt displayed to the user.
        type_func (type): A function to convert the input to a specified type.
        valid_values (list): Optional list of valid values.

    Returns:
        Converted user input, if valid and not an exit command.
    """
    while True:            
        try: # Make sure that the input is under the correct format

            user_input = input(input_prompt)

            if user_input.strip().lower() == "exit":
                exit_prog()

            user_input = type_func(user_input) # If not of the correct type, it will stop the "try" and go to "except"
            
            if valid_values and user_input not in valid_values:
                print(f"Invalid input. Please enter one of the valid input : {valid_values}.")
            else:
                return user_input

        except ValueError:
            print("Invalid input. Please try again.")

        except KeyboardInterrupt:
            exit_prog()


def get_coordinates(bbox = None, corner = "South West"):
    """
    Function that uses regex to manage the user's input of coordinates, when the prefered choice of location is bbox.
    If in decimal format, then separate and return
    If in Dms format, then separate, turn into decimal and return
    If none, try again.

    Args:
        bbox: if prompting coordinates to get the bbox, then add something, else, nothing.
        corner_name (str): the name of the corner that the program will input to the user.

    Returns:
        The decimal coordinates in a tuple.
    
    """
    decimal_pattern = re.compile(r'^-?\d+\.\d+\s*,\s*-?\d+\.\d+$')
    dms_pattern = re.compile(r'(\d+)[°\s](\d+)\'[\s]?(\d+(?:\.\d+)?)[\"]?[\s]?[NSEW],\s*(\d+)[°\s](\d+)\'[\s]?(\d+(?:\.\d+)?)[\"]?[\s]?[NSEW]')
    input_pattern = ""

    while True:
        if bbox:
            user_input = get_input(f">> Enter the coordinates of the {corner} corner of the bbox: ")
        else:
            user_input = get_input(f">> Enter the coordinates : ")

        user_input = f"""{user_input}""" # Triple quotes to deal with the special characters if the user inputs a dms-formated coordinate

        # Checks whether the user input matches either dms or decimal. if not, then ask to prompt again.
        if decimal_pattern.match(user_input):
            coordinates = map(float, user_input.replace(" ", "").split(","))
            coordinates = list(coordinates)
            input_pattern = "decimal"
            return coordinates[0], coordinates[1], input_pattern
        if dms_pattern.match(user_input):
            dms_lat, dms_lon = user_input.split(", ")
            decimal_lat, decimal_lon = dms_to_decimal(dms_lat.strip(), dms_lon.strip())
            input_pattern = "dms"
            return decimal_lat, decimal_lon, input_pattern
        else:
            print("The value you entered does not match the desired format (latitude, longitude)")
            print("""Example of valid format : 48°50'41.5"N, 2°19'48.7"E [OR] 48.855208, 2.345775""")

def get_location():
    """
    Function that asks the user for its prefered choice of location: specific location or bbox
    
    Args: None

    Returns:
        If user choses location, the format is : ['name_location']
        If the user choses bbox, the format is : [longitude_SW, latitude_SW, longitude_NE, latitude_NE], coordinates in float.
    """
    location_name = []
    print("Please select the format for entering the location of your query:\n"
          "   1. Geographical Area (e.g. name of city, country). \n"
          "   2. Bounding Box (square of coordinates)")
    type_research = get_input(">> Enter your choice (1 or 2) : ", int, valid_values=[1, 2])
    match type_research:
        case 1:
            location_name.append(get_input(">> Enter the name of the city/area : ", str))
        case 2:
            print("\nYou have chosen 'Bounding Box' (bbox)")
            print("If you are unsure of what a bbox is, please refer to the documentation")
            print("Input format: latitude, longitude")
            southwest_bbox = get_coordinates(True, "Lower-Left (South-West)")
            northeast_bbox = get_coordinates(True, "Upper-Right (North-East)")
            location_name = list(southwest_bbox) + list(northeast_bbox) # Need to turn into a list because each element is a 'map' -> No concatenation
            location_name.pop(2) # Removing the "input pattern" from get_coordinates that we don't need here
            location_name.pop(4) # same
    return location_name


def get_query_details(query_type):
    """
    Get the additional detail for the query from the user

    args:
        query_type (str): whether the query is only to locate a single element or a combination of two in a radius

    Returns:
        details (dict), including all details needed for the query
    """
    details = {
        'location' : None,
        'bbox' : None,
        'tag_1' : None,
        'tag_2' : None,
        'radius' : None,
    }

    location_input = get_location()
    if len(location_input) == 1:
        details["location"] = location_input
    elif len(location_input) == 4:
        details["bbox"] = location_input
    
    match query_type:
        case "locate":
            details['tag_1'] = get_input(">> Enter the tag (format: 'key=value', e.g. 'shop=bakery') : ", str)
        case "radius":
            details['tag_1'] = get_input(">> Enter the first tag (format: 'key=value', e.g. 'shop=bakery') : ", str)
            details['tag_2'] = get_input(">> Enter the second tag : ", str)
            details['radius'] = get_input(">> Enter the radius (in meters) : ", int)
    return details
