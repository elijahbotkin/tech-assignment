from blast_off.report_creator import ReportCreator
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

if __name__ == "__main__":
	'''
	Purpose: Parse through the data files for the given list of factories. Generates a PDF report for each factory for
	each month, and one additional PDF of a portfolio-level report summarizing all given factories.
	'''

	Tk().withdraw()  # prevent Tk root window from appearing
	factory_attributes_file = askopenfilename()  # ask user to provide attributes file

	'''
	ASSUMPTION: factory-level data files will be stored in the "raw_data" directory within the directory that the current
	FactoryAttributes.csv file. This means the only inputs needed for the tool are the current FactoryAttributes file. 
	Assumed that the user wants to generate a report for each factory that includes all raw data for that factory in the
	"raw_data" directory.
	'''
	rc = ReportCreator(factory_attributes_file=factory_attributes_file)

	rc.get_factory_attributes()
	rc.create_all_reports()

	rc.create_portfolio_report()
