# Osmosint
## Description
Osmosint is an open-source analysis tool designed to help you find anything, anywhere. Through queries to [OpenStreetMap](https://www.openstreetmap.org) (OSM) data, performed with the [Overpy](https://pypi.org/project/overpy/) library, it allows you to get the exact coordinates of any elements, anywhere on earth.

Examples of what you can do with Osmosint in less than 1 minute:
- Get the exact coordinates of all pharmacies in London
- Get the exact coordinates of any bench within a 10m radius of a bakery in Berlin
- Get the Google Maps url of all bakeries in Paris.
- Create a file with the Google Maps url of all the bookshops within a 50m radius of a restaurant in New York City.

I'm sure you can imagine countless examples where this would help you during an open-source research. The only limit is your imagination (and existing OSM tags)!
## Table of Contents
- [Installation]
- [Usage]
	- [Basic usage]
	- [Commands functionality]
		- [Locate]
		- [Radius]
		- [Convert]
	- [Choose output format for locate and radius]
- [Surface-level presentation of OSM (important to understand Osmosint)]
- [Examples]
	- [Troubleshooting an absence of results]
- [License]
- 
## Installation
Follow the instructions below to install Osmosint on your system (works for both Linux and Windows).
1. **Clone the repository**
Open a terminal or Command Prompt and run:
```bash
git clone https://github.com/teknosint/osmosint.git
cd osmosint
```

2. **Set-up a virtual environment (optional)**
Setting up a virtual environment can be useful to prevent version conflicts between packages.
- **For Windows**
```bash
python -m venv venv
venv\Scripts\activate
```
- **For Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install the dependencies**
```bash
pip install -r requirements.txt
```
## Usage
### Basic usage
**Windows**
```
python osmosint.py -h
```
**Unix/Linux**
```
osmosint.py locate
```
### Commands functionality
###### Locate
To locate the instances of a single element within a given location (for example, to get the coordinates of all bakeries in Vienna), you can use:
```
osmosint.py locate
```

###### Radius
To locate the instances of a single tag within a given radius of another tag (for example, to get the coordinates of all the bakeries within a 10m radius of a pharmacy in Vienna) , you can use:
```
osmosint.py radius
```

###### Convert
To change the format of a coordinate (either from dms to decimal, or from decimal to dms), you can use:
```
osmosint.py convert
```
### Output format for *locate* and *radius*

| Parameter | Effect                                          |
| --------- | ----------------------------------------------- |
| -dec      | Output coordinates in decimal format            |
| -dms      | Output coordinates in DMS format                |
| -url      | Output results in Google Maps URL format        |
| -w txt    | Write results in a txt file instead of printing |
| -w csv    | Write results in a csv file instead of printing |

**Default output format**: coordinates in decimal format printed in the terminal. Printing is the rule, file-writing is the exception.

When choosing to output **DMS-formatted coordinates in a csv file**, it is a bit harder to handle because of special characters '°', ,' " ' inherent to the coordinates. Therefore, the coordinates are written with a '\\' character in front of every double quote to ensure no error in the importing of data. To then have readable coordinates, you can replace all \\ with nothing (ctrl + h).

Example of coordinates in decimal format: 1.123123, -12.123123
Example of coordinates in DMS format: 1°07'23.24"N, 12°07'23.24"W

See [[#Examples]] to get a better idea of how to choose the output format.
## Surface-level presentation of OSM (important to understand Osmosint)
Some of you might skip this part but I truly recommend you don't. This part won't go into deep details about the functionning of OverpassQL and OpenStreetMap, it is just a basic rundown to ensure that you know how to make the best use of the program.

For the program to send a correct query and get the answers you are looking for, you will need to input some data. Overpass asks for the data to take a particular format. Below are the things you will have to input.
#### Location
To input a location, the program will ask you this question
![[Pasted image 20240529161619.png]]
Those are the two types of location that Overpass handles. Here is a quick explanation of each of them.
1. **Geographical Area**
The Geographical Area is the most straightforward way to input a location. Essentially, if you want the query to look in London, enter 'London'.

OSM data is, however, not like google maps. If you enter "Paris", looking for the French capital, it might fetch the data from Paris in Texas. It might also fetch the data from Greater Paris, and not limit to the strict boundaries of the city of Paris, France. 

Here are some methods to ensure that the data you enter is the closest to the location you are looking for:
- https://taginfo.openstreetmap.org/keys/name#values --> List of all the possible values of the 'name' attribute for OSM. Before trying a value, you can make sure that it is included in the database. This can especially be useful when looking for a city that has special characters in its name.
- https://osmnames.org/ (recommended)--> Open-source project that gathers all OSM place names on a nice, easily-accessible website. When you enter a location on osmnames, check out the square on the bottom-right corner, and look for the "name" variable. If the square that you see appear on the screen matches the location where you want the query to be, you can enter the value of "name" in the Osmosint.

2. **Bounding Box** 
Bounding Boxes (bbox) are less straightforward, but significantly more precise than Geographical Areas. 

A bbox is a square on the map. Each corner of the square represents a coordinate. Instead of having OSM draw a bbox based on the location you entered, you can specify the coordinates so that the query only looks within the bbox that you defined. Here is an example of a bbox, taken from https://osmnames.org/ (where you can see how imprecise Geographical Areas are; here is the area that would be queried if you entered "London"):

*Figure 1 - Screenshot of the query 'London' on https://osmnames.org/. The red "A" and "B" were added to illustrate the corners of the bbox.*

**Bbox guidelines**
- When entering the bbox, you only need to enter the coordinates from the bottom-left (A) and top-right corners (B). 
- You can enter the coordinates under any format (48.875799 or 48°51'20.8"N), as long as you provide them following this structure: latitude, longitude.
- To get the coordinates, the easier option is to use Google Maps and click on the map to get the coordinates of a specific place. Any alternative that works as well can also be used.

#### Tags
Tags are names given to the elements you are looking for. Again, OSM data is not as straightforward as GoogleMaps. If you enter "bakery", you will not get all bakeries. Tags follow a specific format (key=value). 

- **Format key=value**
This section is an extract from the OSM wiki. Consult [here](https://wiki.openstreetmap.org/wiki/Tags) for more information.

Tags follow the format key=value. The key describes a topic, category or feature (example: amenity, healthcare, shop). The value provides detail for the topic (example: bakery, pharmacy, name of a specific street).

Here are examples of basic tags to help understand the way they work:
- shop=bakery --> Find all bakeries
- healthcare=pharmacy --> Find all pharmacies
- incline=steps --> Find all steps

You need to pay attention to the fact that values can have several keys. For example, some pharmacies might be found using 'healthcare=pharmacy'. But you can also get pharmacies using 'amenity=pharmacy'.

- **Where to find tags?**
The best way to find tags is to look at the [taginfo website](https://taginfo.openstreetmap.org/tags), which lists all existing tags within OSM. There, you can search for tags on the upper-right searchbar.

- **The program**
OSM data is categorised under three types: nodes, ways, relations. This program only fetches nodes results. Ways and relations are harder to handle considering that they are made up of several nodes (so several coordinates).

Once you find adequate tag (or tags) for a query, you will need to enter them in Osmosint using the key=value format. Example: natural=tree.

## Examples
```
Osmosint.py locate -dec -url
```
Launch the locate functionality of the program, and print the results in decimal format and as Google Maps url in the terminal.

```
Osmosint.py radius --dms_coords -w txt
```
Launch the radius functionality of the program, and print the results in DMS format in a .txt file.
#### Example use of radius

Here, I used "Osmosint.py radius -url", meaning I want the program to perform a radius search, and print the results in clickable -url format.

First, the program asks whether I want to input the location in Geographical Area or Bounding Box. I chose, 1, and entered 'Barcelona'. This means that the program will only check results in the bounding box defined for the place 'Barcelona'. I 
### Troubleshooting an absence of results
If you get a message from Osmosint saying that there was no response to your query, it means that the query fetched 0 instances from the specified tag within the location. Here are the steps to follow:
- Check the syntax of the tag(s) you entered. Make sure that they closely match what you see on https://taginfo.openstreetmap.org/tags
- On taginfo, also check that the key/value combination do exist. For example, pharmacies exist under amenity=pharmacy but not under shop=pharmacy.
- If you entered a Geographical area as location, check on https://osmnames.org/ that it exists, that the syntax is correct, and that the covered area corresponds to the location where you want to do your query.
- If you entered a bbox, double-check that the coordinates you entered are correct. The API only accepts coordinates in decimal format (12.123123). You can enter the coordinates in dms format (48°51'20.8"N), which are then converted by the program. If you want, you can try to convert the coordinates using the *convert* command of Osmosint to check that the decimal version matches what you intended to enter. If they do correspond to your bbox, you can try the *locate* or *radius* commands again with the new coordinates.
- If you are doing a radius check, try increasing the radius to check whether the problem comes from a radius that is too narrow. For example, if you tried to get all the pharmacies within a 1m radius of a bakery, it is likely that you won't get a response. However, if you tried all the pharmacies within a 100m radius in Paris and did not get anything, there is likely a problem with how you entered your parameters.
## License
This project is licensed under the MIT License. See the [LICENSE](LISENSE) file for details.

### Acknowledgements
This project uses the [OverPy library](https://pypi.org/project/overpy/), which is licensed under the MIT License. 

Data used by this project is retrieved from the Overpass API, which operates under the Open Database License (ODbL) by OpenStreetMap. Please see the [OSM legal FAQ](https://wiki.osmfoundation.org/wiki/Licence) for more details.
