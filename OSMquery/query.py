"""
Osmosint query module

This module deals with the creation and sending of the OSM query to the API

"""

import overpy
import sys

def create_query(parameters):
    """
    Takes in all the parameters and creates the query

    args:
        parameters (dict): dict of all the parameters
    returns:
        query (str) to send to API
    """
    match parameters["type_query"]:
        case "locate":
            if parameters["location"]:
                query = f"""
area["name"="{parameters["location"][0]}"]->.boundaryarea;
(node(area.boundaryarea)[{parameters["tag_1"]}];)->.A;
out body;
"""
            else: # Going for Bbox
                query = f"""
[bbox:{parameters["bbox"][0]},{parameters["bbox"][1]},{parameters["bbox"][2]},{parameters["bbox"][3]}];
node[{parameters["tag_1"]}];)->.A;
out body;
"""

        case "radius":
            if not parameters["location"] == None:
                query = f"""
area["name"={parameters["location"][0]}]->.boundaryarea;
(node(area.boundaryarea)[{parameters["tag_1"]}];)->.A;
(node(area.boundaryarea)[{parameters["tag_2"]}];)->.B;
nwr.A(around.B:{parameters["radius"]});
out body;
                """
            else: # Going for Bbox
                query = f"""
[bbox:{parameters["bbox"][0]},{parameters["bbox"][1]},{parameters["bbox"][2]},{parameters["bbox"][3]}];
(node[{parameters["tag_1"]}];)->.A;
(node[{parameters["tag_2"]}];)->.B;
nwr.A(around.B:{parameters["radius"]});
out body;
                """
    return query


def query_to_api(query):
    """
    Sends the query to the api and manages errors

    args:
        query (str) : the query to send to the api, from create_query()

    Returns
        results (list) if the query happens without error
        False if there was an error
    """
    api = overpy.Overpass()
    try:
        result = api.query(query)
        return result
                
    except overpy.exception.OverpassBadRequest:
        print("There was a syntax error in the query.")
        print("Please check that your input matches the documentation's example, or that it does not contain any special characters or quotes (\", \')")
    except overpy.exception.OverpassTooManyRequests:
        print("Too many requests have been sent to the Overpass API. Please try again later.")
    except overpy.exception.OverpassGatewayTimeout:
        print("The Overpass API server is too busy to handle the request. Please try again later.")
    except overpy.exception.OverpassRuntimeError:
        print("A runtime error occurred on the Overpass API server.")
    except overpy.exception.OverpassRuntimeRemark:
        print("A runtime remark was returned by the Overpass API server.")
    except overpy.exception.OverpassUnknownContentType:
        print("The Overpass API returned an unknown content type.")
    except overpy.exception.OverpassUnknownHTTPStatusCode:
        print("The Overpass API returned an unknown HTTP status code.")
    except overpy.exception.DataIncomplete:
        print("The data returned by the Overpass API is incomplete.")
    except overpy.exception.ElementDataWrongType:
        print("The data type of an element returned by the Overpass API is incorrect.")
    except overpy.exception.MaxRetriesReached:
        print("The maximum number of retries to the Overpass API was reached.")
    except overpy.exception.OverpassError:
        print("An error occurred with the Overpass API.")
    except overpy.exception.OverPyException:
        print("An OverPy exception occurred.")
    except Exception:
        print("An unexpected error occurred.")
    return False

def extract_data_from_result(result):
    """
    Extract the coordinates from the raw api result

    args:
        result: the raw result given by the API query

    returns:
        coordinates (list): list of coordinates in tuples
    """
    raw_data_nodes = result.get_nodes()
    coordinates = [(float(node.lat), float(node.lon)) for node in raw_data_nodes]
    return coordinates
