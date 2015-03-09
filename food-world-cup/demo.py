"""This program will determine the most popular ethnic food based on demographics."""

import csv
import numpy as np
import string
import matplotlib
import matplotlib.pyplot as plt
import operator
import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pprint import pprint
import pylab as plt2
from pylab import *
from mpl_toolkits.basemap import Basemap
from matplotlib.widgets import Slider, Button, RadioButtons
plt.close('all')


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"




def get_numpy_array(csv_file):                                                                                                                                             
	"""returns a numpy array built from the csv file. To stop numpy from crapping itself, uneven rows and columns are padded with empty strings so that all rows and            columns have the same number of elements"""                                                                                                                                 
	data = []                                                                                                                                                               
	f = open(csv_file, "rU")                                                                                                                                                     
	for row in csv.reader(f):                                                                                                                                              
		data.append(row)                                                                                                                                                    
	length = len(sorted(data,key=len, reverse=True)[0])
	#print np.array([x+[]*(length-len(x)) for x in data])  
	return np.array([x+[]*(length-len(x)) for x in data])  

def fix_data(filename):
	a = get_numpy_array(filename)
	remove = ["N/A"]
	for element in a:
		for index in range(len(element)):
			if element[index] in remove:
				element[index] = 0
	return a

def sum_by_age(filename,age_range):
	data = fix_data(filename)
	final = []
	fn = []
	for n in range(3,43):
		column_country_sum = []
		column_country = data[1:,n]
		for index in range(1,len(column_country)):
			if data[index, 44] == age_range:
				try:
					column_country_sum.append(int(data[index,n]))
				except:
					pass
		final.append(sum(column_country_sum))
	return final

def sum_countries2(filename):
	data = fix_data(filename)
	final = []
	fn = []
	for n in range(3,43):
		new2 = []
		new = data[1:,n]
		for ele in new:
			try:
				new2.append(int(ele))
			except:
				pass
		final.append(sum(new2))
	return final

def country_rank_age(filename,age_range):
	countries = ['Algeria','Argentina','Australia','Belgium','Bosnia and Herzegovia','Brazil','Cameroon','Chile','Colombia','Costa Rica','Croatia','Ecuador','England','France','Germany','Ghana','Greece','Honduras','Iran','Italy','Ivory Coast','Japan','Mexico','Netherlands','Nigeria','Portugal','Russia','South Korea','Spain','Switzerland','United States','Uruguay','China','India','Thailand','Turkey','Cuba','Ethiopia','Vietnam','Ireland']
	country_sum = sum_by_age(filename, age_range)
	country_rank = dict(zip(countries,country_sum))
	return country_rank

def country_rank(filename):
	countries = ['Algeria','Argentina','Australia','Belgium','Bosnia and Herzegovia','Brazil','Cameroon','Chile','Colombia','Costa Rica','Croatia','Ecuador','England','France','Germany','Ghana','Greece','Honduras','Iran','Italy','Ivory Coast','Japan','Mexico','Netherlands','Nigeria','Portugal','Russia','South Korea','Spain','Switzerland','United States','Uruguay','China','India','Thailand','Turkey','Cuba','Ethiopia','Vietnam','Ireland']
	country_sum = sum_countries2(filename)
	country_rank = dict(zip(countries,country_sum))
	return country_rank

def make_barplot(filename):
	"""Using a dictionary, plots a book's relative happiness in reference to the year it was published.
	Input is a list of txt files generated by the get_file function.
	file_list = list of string that correspond to .txt files"""
	D = country_rank(filename)
	#this for loop plots the publishing year and first sentiment (polarity) of each book
	#in the dictionary
	for country in D:
		plt.bar(range(len(D)), D.values())
	plt.xticks(range(len(D)),D.keys(),rotation = 'vertical')
	plt.xlabel('country')
	plt.ylabel('sum of survey data')
	plt.title('Popularity of Ethnic Foods', fontsize=12)
	plt.show()


def make_interactive_plot(filename):
	fig, ax = plt.subplots()
	plt.subplots_adjust(left=0.3)

	axcolor = 'lightgoldenrodyellow'
	rax = plt.axes([0.05, 0.7, 0.15, 0.15], axisbg=axcolor)
	radio = RadioButtons(rax, ('18-29', '30-44', '44-60'))
	def hzfunc(filename,label):
		D = country_rank_age(filename,label)
		hzdict = {'18-29':s0, '30-44':s1, '44-60':s2}
		ydata = hzdict[label]
		l.set_ydata(ydata)
		for country in D:
		plt.bar(range(len(D)), D.values())
		plt.xticks(range(len(D)),D.keys(),rotation = 'vertical')
		plt.xlabel('country')
		plt.ylabel('sum of survey data')
		plt.title('Popularity of Ethnic Foods', fontsize=12)
		plt.show()
		plt.draw()
	radio.on_clicked(hzfunc)

make_interactive_plot("food-world-cup-data.csv")


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    new_place = place_name.replace(' ', "+")
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + new_place + "&key=AIzaSyAqswAJZEulRtIHPvMpyCEYMT8XpU8uCM4" 
    json = get_json(url)
    results = json["results"][0]['geometry']['bounds']['northeast']    
    lat_long = results['lat'],results['lng']
    return lat_long #tuple

def lat_long_countries(filename):
	D = country_rank(filename) 
	for country in D:
		latlong = get_lat_long(country)
		D[country] = [D[country] , latlong[0] , latlong[1]]
	return D

def plot_on_map(filename):
	D = lat_long_countries(filename)
	m = Basemap(llcrnrlon=-360,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=90,
		  resolution='c')
	m.drawcoastlines()
	m.drawcountries()
	max_size=280
	for city in D.keys():
	        x, y = m(D[city][1],D[city][2]) 
	        m.scatter(x,y,max_size*D[city][0]/D["Italy"][0],marker='o',color='r')

	axcolor = 'lightgoldenrodyellow'
	rax = axes([-10.0, 10.0, 10.0, -10.0], axisbg=axcolor)
	radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)
	def colorfunc(label):
	    D.set_color(label)
	    draw()
	radio.on_clicked(colorfunc)
	plt.show()


