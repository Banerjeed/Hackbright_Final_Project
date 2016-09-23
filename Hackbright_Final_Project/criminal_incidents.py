"""Create map to show criminal incidents in San Francisco from 2003 to 2015
and allow user to focus on specific category of incident"""

#import SFPD incidents API
#open data
#ask for raw input and give choice of neighborhood to look at or crime category
#parse the data to show only incident category (choose certain options) and location
#cull between crime category
#gather the latitude and longitudes of crimes
#pass data into mapbox
#plot the data on map of SF using (mapbox) - longitude/latitude
#user can see map as a whole or type (zoom in on?) specific neighborhood to see in detail? (depends on mapbox)
#user can view map by specific crime categories or choose specific neighborhood to focus on

from urllib2 import urlopen
import json
import os


#load api data into a variable to pass as parameter when creating a dictionary of coordinates
def import_api():
	api_url = 'https://data.sfgov.org/resource/gxxq-x39z.json'
	response = urlopen(api_url)
	json_obj = json.load(response)
	return json_obj 

#plot datapoints for all crimes using mapbox and api
def create_total_crime_map(crimes):

	#Find javascript/mapbox code to display coordinates in a webpage with html
	html = """<!DOCTYPE html>
<html>
<head>
  <meta charset=utf-8 />
  <title></title>
  <script src='https://api.mapbox.com/mapbox.js/v2.4.0/mapbox.js'></script>
  <link href='https://api.mapbox.com/mapbox.js/v2.4.0/mapbox.css' rel='stylesheet' />
  <style>
    body { margin:0; padding:0; }
    .map { position:absolute; top:0; bottom:0; width:100%; }
  </style>
</head>
<body>
<div id='map_geo' class='map'> </div>
<script>
var geojson = """ + json.dumps(crimes) + """;

// call map api using javascript code and load my python code into usable variable (geojson)

L.mapbox.accessToken = 'pk.eyJ1IjoiYmFuZXJqZWVkIiwiYSI6ImNpc3doNzRpYzA1NmQyemtocTh5ZzkxMzYifQ.-w2jfFGPwju-dMjY-3NjMw';
var mapGeo = L.mapbox.map('map_geo', 'mapbox.light').setView([37.76, -122.4], 12);
var myLayer = L.mapbox.featureLayer().setGeoJSON(geojson).addTo(mapGeo);
//mapGeo.scrollWheelZoom.disable();

</script>
</body>
</html>
"""

	#writing the markup to a file which creates the webpage
	with open('maptest3.html', mode = 'w') as my_file:
		my_file.write(html)

	
	os.system('open ' + my_file.name)

#create map using a specific incident category
def create_crime_dictionary(crimes):


	#Find javascript/mapbox code to display coordinates in a webpage with html
	html = """<!DOCTYPE html>
<html>
<head>
  <meta charset=utf-8 />
  <title></title>
  <script src='https://api.mapbox.com/mapbox.js/v2.4.0/mapbox.js'></script>
  <link href='https://api.mapbox.com/mapbox.js/v2.4.0/mapbox.css' rel='stylesheet' />
  <style>
    body { margin:0; padding:0; }
    .map { position:absolute; top:0; bottom:0; width:100%; }
  </style>
</head>
<body>
<div id='map_geo' class='map'> </div>
<script>
var geojson = """ + json.dumps(crimes) + """;

// call map api using javascript code and load my python code into usable variable (geojson)

L.mapbox.accessToken = 'pk.eyJ1IjoiYmFuZXJqZWVkIiwiYSI6ImNpc3doNzRpYzA1NmQyemtocTh5ZzkxMzYifQ.-w2jfFGPwju-dMjY-3NjMw';
var mapGeo = L.mapbox.map('map_geo', 'mapbox.light').setView([37.76, -122.4], 12);
var myLayer = L.mapbox.featureLayer().setGeoJSON(geojson).addTo(mapGeo);
//mapGeo.scrollWheelZoom.disable();

</script>
</body>
</html>
"""


	with open('maptest3.html', mode = 'w') as my_file:
		my_file.write(html)

	os.system('open ' + my_file.name)


def main():

	#Introduce user to map
	print "   "
	print "Welcome to my final project!"
	print "   "
	print "Please open my webpage to view a map of SFPD's criminal incidents from 2003 - 2015"
	print "   "
	#Ask user to view map by crime category or not
	user_choice = (raw_input("Do you want to view a specific category of incidents? (Y or N) ")).upper()
	

	#prompt user to choose which category of criminal incidents to view
	if user_choice == 'Y':
		l = ["ROBBERY", "ARSON", "ASSAULT", "BURGLARY", "PROSTITUTION", "DRUG/NARCOTIC", "LARCENY/THEFT", "VANDALISM"]
		for i in range(len(l)):
			print "Enter ", (i), "to view", l[i], " offenses in San Francisco"

		category = l[int(raw_input())]


		print "Refresh my webpage to see " + category + " incidents in San Francisco"



		#display map based on user input by modifying geojson variable
		#print static map of arrest points using mapbox/geojson - pull all arrests from API and plot points
		crimes = []
		for obj in import_api():
			if category == obj["category"]:
				d = {}
				d['type'] = 'Feature'
				latitude = float(obj['y'])
				longitude = float(obj['x'])
				d['geometry'] = {'type':'Point', 'coordinates': [longitude,latitude]}
				crimes.append(d)

		create_crime_dictionary(crimes)

	#if user does not wish to view specific incident, reload the total crimes map
	elif user_choice == 'N':
		crimes = []

		for incident in import_api():
			d = {}
			d['type'] = 'Feature'
			latitude = float(incident['y'])
			longitude = float(incident['x'])
			d['geometry'] = {'type':'Point', 'coordinates': [longitude,latitude]}
			crimes.append(d)
			
		create_total_crime_map(crimes)

		print "Please open my webpage to view a map of SFPD's criminal incidents from 2003 - 2015"

	#any other option besides yes or no would prompt and error message and bring user back to beginning
	else:
		print "ERROR: Please make valid selection"

		main()

if __name__ == '__main__':
    main()



