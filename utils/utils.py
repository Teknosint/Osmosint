"""
Osmosint utils module

This module deals with the parser for Osmosint.
"""
import argparse
import sys

def exit_prog():
    """
    Function to exit the program and send a message

    args: None

    Return: None
    """
    print("Exiting the program...")
    sys.exit()


def parse_args():
    """
    Parses what the user writes in the command line

    args:
        none

    Returns the args
    """
    parser = argparse.ArgumentParser(
        description="This program processes OpenStreetMap (OSM) data to get the coordinates of specific elements anywhere on earth.",
        epilog="Use the subcommands 'locate', 'radius, or 'convert' for specific actions. For more information on each subcommand, use -h or --help after the subcommand."
    )

    def add_location_arguments(subparser):
        subparser.add_argument("-dec",
                               "--decimal_coords",
                               action='store_true',
                               help="Output coordinates in decimal format")
        subparser.add_argument("-dms",
                               "--dms_coords",
                               action='store_true',
                               help="Output coordinates in degrees, minutes, and seconds (DMS) format")
        subparser.add_argument("-url",
                               "--google_urls",
                               action='store_true',
                               help="Generate Google Maps URLs for the coordinates")
        subparser.add_argument("-w",
                               "--write_file",
                               type=str,
                               choices=['txt', 'csv'],
                               help="Write the output to a file (txt or csv)")

    add_location_arguments(parser)
    
    subparser = parser.add_subparsers(dest='command')
     
    parser_locate = subparser.add_parser('locate',
                                         help="Launch a query to the OSM database and get the location of a specific element")
    add_location_arguments(parser_locate)
        
    parser_radius = subparser.add_parser('radius',
                                         help="Locate OSM tag within a given radius of another tag")
    add_location_arguments(parser_radius)
    
    
    parser_convert = subparser.add_parser('convert',
                                          help="Change the format from coordinates (from DMS to decimal, or the contrary)")
    


    args = parser.parse_args()
    return args
