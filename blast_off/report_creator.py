import csv, glob, base64, ntpath, re, shutil, datetime
from os import listdir, path
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import pandas as pd
import time
import numpy as np
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter

class ReportCreator(object):
	'''
	Class allows for downloading, parsing, and reporting of individual factories, as well as portfolio-level
	reporting which includes all factories.

	Assumptions:
	- Individual file naming convention: [Factory Name] - [Month] [Year].csv
	- List of factories will always be provided in FactoryAttributes.csv <--this is the only necesary input besides month/year

	'''
	def __init__(self, factory_attributes_file):
		'''

		:param factory_attributes: a file containing the list of factories
		:param year: 4-digit integer
		:param month: integer from 1-12 inclusive
		'''
		self.factory_attributes_file = factory_attributes_file
		self.raw_data_dir = path.join(path.split(self.factory_attributes_file)[0], 'raw_data')
		self.all_raw_data = [f for f in listdir(self.raw_data_dir) if path.isfile(path.join(self.raw_data_dir, f))]
		self.outputs_dir = path.join(path.split(self.factory_attributes_file)[0], 'outputs')
		self.graphs_dir = path.join(self.outputs_dir, 'graphs')

		self.months = []

		# list of factory attributes dictionaries.
		# Data Definition:
		# List of Dictionaries
		# Dictionaries have 3keys:
		# - Factory
		# - Year Built
		# - SqFootage
		self.factory_attributes = []

		# list of factory names, filled in later
		self.factories = []

		# holds final numbers by factory
		# Keys:
		# - Factory Name [String]
		# Value: Dictionary
		#   Keys:
		#   - Average demand
		#   - Average demand per square foot
		#   - Total demand
		#   - Peak demand
		self.factory_outputs = {}

		# holds portfolio outputs by month
		# Key: Month [String]
		# Value: Dictionary
		#   Keys: same as factory_outputs
		self.portfolio_outputs = {}


	def get_factory_attributes(self):
		'''
		fills in the self.factories from the given file
		:return:
		'''
		with open(self.factory_attributes_file, newline='') as csvfile:
			reader = csv.DictReader(csvfile)

			for row in reader:
				self.factory_attributes.append(row)

		return
		# comment this out, reference only
		for factory in self.factory_attributes:
			print("Factory Name:", factory['Factory'])
			print("Year Built:", factory['Year Built'])
			print("SqFootage:", factory['SqFootage'])

	def create_all_reports(self):
		'''
		1. loops through the list of factories
		2. grabs list of data files for that factory
		3. loop through data files and sends raw data to method to generate monthly reports
		:return:
		'''
		self.raw_data_dir = path.join(path.split(self.factory_attributes_file)[0],'raw_data')
		self.all_raw_data = [f for f in listdir(self.raw_data_dir) if path.isfile(path.join(self.raw_data_dir,f))]

		for factory in [factory['Factory'] for factory in self.factory_attributes]:
			list_of_raw_data = [f for f in self.all_raw_data if factory in f]
			self.create_factory_report(factory,list_of_raw_data)


	def create_factory_report(self, factory, raw_data_files):
		'''

		:param factory: String of the factory name
		:param raw_data_files: a list of raw data file names [String]
		:return:
		'''
		factory_year_built = [x['Year Built'] for x in self.factory_attributes if x['Factory'] == factory][0]
		factory_sq_footage = [x['SqFootage'] for x in self.factory_attributes if x['Factory'] == factory][0].replace(',','')

		self.factory_outputs[factory] = {}

		# create pdf
		filename = path.join(self.outputs_dir, factory + ' Summary.pdf')
		doctitle = factory + 'Summary'
		title = factory
		subtitle = 'Built in ' + str(factory_year_built)

		# Factory level summary page
		pdf = canvas.Canvas(filename)
		pdf.setFont('Helvetica-Bold', 36)
		pdf.setTitle(doctitle)
		pdf.drawCentredString(290, 720, title)
		pdf.setFontSize(24)
		pdf.drawCentredString(290, 690, subtitle)
		pdf.save()

		# accumulators for portfolio-level reporting
		port_total_kwh = 0
		port_total_sq_feet = 0
		port_peak_demand = 0

		for raw_data_file in raw_data_files:
			file_full_path = path.join(self.raw_data_dir, raw_data_file)
			m = re.search('(.*) - (.*) (.*)\.csv',raw_data_file)
			month = m.group(2)
			year = m.group(3)

			self.factory_outputs[factory][year] = {}
			self.factory_outputs[factory][year][month] = {}

			headers = ['Day', 'Electricity Usage (kWh)']
			df = pd.read_csv(file_full_path, header=0, names=headers)

			x = df['Day']
			y = df['Electricity Usage (kWh)']

			self.factory_outputs[factory][year][month]['average demand'] = df['Electricity Usage (kWh)'].mean()
			self.factory_outputs[factory][year][month]['average demand per square foot'] = df['Electricity Usage (kWh)'].mean()/float(factory_sq_footage)
			self.factory_outputs[factory][year][month]['total demand'] = df['Electricity Usage (kWh)'].sum()
			self.factory_outputs[factory][year][month]['peak demand'] = df['Electricity Usage (kWh)'].max()

			plt.title(factory + ' - ' + month + ' ' + year)
			plt.plot(x,y)
			plt.xlabel('Day')
			plt.ylabel('Electricity Usage (kWh)')
			plt.savefig(path.join(self.graphs_dir, factory + " " + month + " " + year + ".pdf"))
			plt.close()

		# after creating the JPGs of the plots, put them into the pdf file
		return

	def create_portfolio_report(self):
		'''
		creates a portfolio-level summary report
		:return:
		'''

		# create list of all files including paths
		all_file_paths = [path.join(self.raw_data_dir, f) for f in self.all_raw_data]
		months = [f for f in self.all_raw_data]

		self.portfolio_outputs[year][month]
		self.portfolio_outputs[year][month]['average demand']
		self.portfolio_outputs[year][month]['average demand per square foot']
		self.portfolio_outputs[year][month]['total demand']
		self.portfolio_outputs[year][month]['peak demand']