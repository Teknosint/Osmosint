"""
Osmosint conversion module

This module contains functions to convert coordinates from any format to the other
"""
import re

def dms_to_decimal(dms_lat, dms_lon):
    """
    Function that converts coordinates from the dms format to the decimal format

    Args:
        lat (str): latitude of the coordinates in dms format
        lon (str): longitude of the coordinates in dms format

    Returns:
        Coordinates in a tuple in decimal format (float).
    """    
    def convert(dms):
        dms_pattern = re.compile(r'(\d+)[°\s](\d+)\'[\s]?(\d+(?:\.\d+)?)[\"]?[\s]?([NSEW])')
        match = dms_pattern.match(dms)
        
        if not match:
            raise ValueError(f"Invalid DMS format: {dms}")
        
        degrees, minutes, seconds, direction = match.groups()
        decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        
        if direction in ['S', 'W']:
            decimal = -decimal
        
        return decimal
    
    decimal_lat = round(convert(dms_lat), 6)
    decimal_lon = round(convert(dms_lon), 6)
    return decimal_lat, decimal_lon


def decimal_to_dms(lat, lon):
    """
    Function that converts coordinates from the decimal format (API response format) to the DMS format

    Args:
        lat (float): latitude of the coordinates.
        lon (float): longitude of the coordinates.

    Returns:
        Coordinates in a tuple in DMS format.
    """
    def dms(coord):
        # Convert a decimal degree coordinate to degrees, minutes, seconds
        is_positive = coord >= 0
        coord = abs(coord)
        degrees = int(coord)
        minutes_full = (coord - degrees) * 60
        minutes = int(minutes_full)
        seconds = (minutes_full - minutes) * 60
        return degrees, minutes, seconds, is_positive

    lat_dms = dms(lat)
    lon_dms = dms(lon)

    # Determine the hemisphere
    lat_hem = "N" if lat_dms[3] else "S"
    lon_hem = "E" if lon_dms[3] else "W"

    # Return as a formatted string
    lat_str = f"""{lat_dms[0]}°{lat_dms[1]:02d}'{lat_dms[2]:05.2f}\"{lat_hem}"""
    lon_str = f"""{lon_dms[0]}°{lon_dms[1]:02d}'{lon_dms[2]:05.2f}\"{lon_hem}"""
    
    return (lat_str, lon_str)


def convert_coordinates():
    """
    Converts the coordinates. If user inputs coordinates in dms, then output in decimal. Contrary elsewise.

    args:
        None

    Returns a tuple of coordinates in the desired format
    """
    from input.input import get_coordinates

    raw_lat, raw_lon, input_format = get_coordinates()
    if input_format == "decimal":
        dms_lat, dms_lon = decimal_to_dms(raw_lat, raw_lon)
        return dms_lat, dms_lon
    elif input_format == "dms":
        return raw_lat, raw_lon


        



