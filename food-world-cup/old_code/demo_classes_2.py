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
import matplotlib.ticker as ticker



class Data(object):
	def __init__(self, filename):
		self.filename = filename

	def get_age_range(self,age_range):
		self.age_range = age_range
		return age_range
	
	def get_numpy_array(self):                                                                                                                                             
		"""returns a numpy array built from the csv file. To stop numpy from crapping itself, uneven rows and columns are padded with empty strings so that all rows and            columns have the same number of elements"""                                                                                                                                 
		data = []      
		csv_file = self.filename                                                                                                                                                         
		f = open(csv_file, "rU")                                                                                                                                                     
		for row in csv.reader(f):                                                                                                                                              
			data.append(row)                                                                                                                                                    
		length = len(sorted(data,key=len, reverse=True)[0])
		#print np.array([x+[]*(length-len(x)) for x in data])  
		return np.array([x+[]*(length-len(x)) for x in data])  

	def fix_data(self):
		a = self.get_numpy_array()
		remove = ["N/A"]
		for element in a:
			for index in range(len(element)):
				if element[index] in remove:
					element[index] = 0
		return a

	def get_sum_by_age(self):
		data = self.fix_data()
		final = []
		fn = []
		for n in range(3,43):
			column_country_sum = []
			column_country = data[1:,n]
			for index in range(1,len(column_country)):
				if data[index, 44] == self.age_range:
					try:
						column_country_sum.append(int(data[index,n]))
					except:
						pass
			final.append(sum(column_country_sum))
		return final


	def get_country_rank_age(self):
		countries = ['Algeria','Argentina','Australia','Belgium','Bosnia and Herzegovia','Brazil','Cameroon','Chile','Colombia','Costa Rica','Croatia','Ecuador','England','France','Germany','Ghana','Greece','Honduras','Iran','Italy','Ivory Coast','Japan','Mexico','Netherlands','Nigeria','Portugal','Russia','South Korea','Spain','Switzerland','United States','Uruguay','China','India','Thailand','Turkey','Cuba','Ethiopia','Vietnam','Ireland']
		country_sum = self.get_sum_by_age()
		country_rank = dict(zip(countries,country_sum))
		return country_rank


data = Data("food-world-cup-data.csv")
data.get_age_range('30-44')

print data.get_country_rank_age()

class Plot(object):
	def __init__(self, filename):
		self.filemame = Data(self.filename)

	def add_age(self,age_range):
		self.age_range = age_range
		return age_range

	def using_Data(self):
		filename = Data(self.filename)
		filename.add_age(self.age_range)
		return filename

	def make_barplot(self):
		"""Using a dictionary, plots a book's relative happiness in reference to the year it was published.
		Input is a list of txt files generated by the get_file function.
		file_list = list of string that correspond to .txt files"""
		filename = Plot(self.filename)
		#filename.add_age('18-29')
		plot_data = filename.using_Data(filename)
		D = Data.country_rank_age(plot_data)

		for country in D:
			plt.bar(range(len(D)), D.values())
		plt.xticks(range(len(D)),D.keys(),rotation = 'vertical')
		plt.xlabel('country')
		plt.ylabel('sum of survey data')
		plt.title('Popularity of Ethnic Foods', fontsize=12)
		plt.show()


	def make_interactive_plot(self):
		filename = self.filename
		young = country_rank_age("food-world-cup-data.csv",'18-29')
		medium = country_rank_age("food-world-cup-data.csv",'30-44')
		old = country_rank_age("food-world-cup-data.csv",'45-60')
		older = country_rank_age("food-world-cup-data.csv",'> 60')
		fig, ax = plt.subplots()
		D = country_rank_age(filename, '18-29')
		for country in D:
			ax.bar(range(len(D)), D.values())
		plt.xticks(range(len(D)),D.keys(),rotation = 'vertical')
		plt.xlabel('country')
		plt.ylabel('sum of survey data')
		plt.title('Popularity of Ethnic Foods', fontsize=12)
		axcolor = 'lightgoldenrodyellow'
		plt.subplots_adjust(left=0.3)
		rax = plt.axes([0.05, 0.7, 0.15, 0.15], axisbg=axcolor)
		radio = RadioButtons(rax, ('18-29', '30-44', '45-60'))

		def hzfunc(label):
			fig, ax = plt.subplots()
			plt.clf()
			hzdict = {'18-29':young, '30-44':medium, '45-60':old}
	   		D = hzdict[label]
			for country in D:
				ax.bar(range(len(D)), D.values())
			plt.xticks(range(len(D)),D.keys(),rotation = 'vertical')
			plt.xlabel('country')
			plt.ylabel('sum of survey data')
			plt.title('Popularity of Ethnic Foods', fontsize=12)
			axcolor = 'lightgoldenrodyellow'
			plt.subplots_adjust(left=0.3)
			rax = plt.axes([0.05, 0.7, 0.15, 0.15], axisbg=axcolor)
			plt.show()

		radio.on_clicked(hzfunc)
		plt.show()

