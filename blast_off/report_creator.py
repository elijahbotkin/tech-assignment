import csv, glob, base64, ntpath, re, shutil, os
from configparser import RawConfigParser

class ReportCreator(object):
	'''
	Class allows for downloading, parsing, and reporting of individual factories, as well as portfolio-level
	reporting which includes all factories.

	Assumptions:
	- Individual file naming convention: [Factory Name] - [Month] [Year].csv
	- List of factories will always be provided in FactoryAttributes.csv <--this is the only necesary input besides month/year

	'''
	