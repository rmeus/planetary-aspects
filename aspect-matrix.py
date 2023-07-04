""" for each planetary body, caculate the angular aspect between it
   and all other bodies in the DataFrame.
"""
import copy
import pandas as pd

# map the zodiac signs as offsets from a meridian defined as 0 deg. Aries
offset = {
	'Ari': 0,
	'Psc': 30,
	'Aqr': 60,
	'Cap': 90,
	'Sgr': 120,
	'Sco': 150,
	'Lib': 180,
	'Vir': 210,
	'Leo': 240,
	'Cnc': 270,
	'Gem': 300,
	'Tau': 330
}

def calc_aspect (pos1, pos2):
	""" return the difference in degrees between two ojects on the astral plane
		ARGS:
			- pos1 - List [ sign, degrees, minutes ]
			- pos2 - List [ sign, degrees, minutes ]

		DESCRIPTION:
			Each sign is assigned an offset from 0 degrees Aries.
			Minutes are coverted to decimal values.
			Positions are calculated based on the above.

		RETURN: 
			Decimal difference between the two positions
	"""

	# extract list values
	sign1,deg1,min1 = pos1
	sign2,deg2,min2 = pos2
	
	# calculate the positions = offet + degrees + (decimal) minutes
	position1 = offset[sign1] + int(deg1) + (round((int(min1))*10/6)/100)
	position2 = offset[sign2] + int(deg1) + (round((int(min2))*10/6)/100)
	aspect = abs(position2 - position1)

	# Normalize the data (retrn the lesser value if over 180 degrees)
	if aspect > 180:
			aspect = 360 - aspect

	# return aspect
	return round(aspect,2)

def parse_ephemeris (data):
	"""
	data is taken from the ephermeris here: http://ephemeris.com/ephemeris.php
	parse each line of the data and load it into the 'input' dataframe

	ARGS:
	- input = a panda DataFrame of ephemeris data for a given day
	- datafil - raw planetary data includes sign, degrees, minutes (see below)

	RETURN:
	- DataFrame representing the 'matrix' of all planetary aspects possible
	  for the given input.
	
	For example, if the input contains the planetary data for Mars, Jupiter, Saturn,
	the returned data will be a 3x3 matrix of the planetary aspects:
		- Mars-Mars (set to None)
		- Mars-Jupiter (aspect angle between the two planetary bodies)
		- Mars-Saturn (aspect angle between the two planetary bodies)
	"""
	datafile = open(data, 'r')
	Lines = datafile.readlines()

	# parse and store [the first 24 char of] each line into planetary positions
	input = pd.DataFrame()
	for line in Lines:
		if len(line[:24].split()) == 4:
			body, degrees, sign, minutes = line[:24].split()

			# Pandas expects that each value of a dictionary to be a list
			data = dict(body=body, sign=sign, degrees=degrees, minutes=minutes)
			new_row = pd.DataFrame([data])

		# handle Moon's Node - len = 5
		else:
			body, _, degrees, sign, minutes = line[:24].split()

			# convert each row from List to Dict, then a DataFrame
			data = dict(body="MoonsNode", sign=sign, degrees=degrees, minutes=minutes)

			# error - need to force an index
			# see https://stackoverflow.com/questions/57631895/dictionary-to-dataframe-error-if-using-all-scalar-values-you-must-pass-an-ind
			new_row = pd.DataFrame([data])

		# collect all rows
		input = pd.concat([input, new_row], ignore_index=True)

	# get list of 'keys' or planetary bodies from the input
	input.set_index('body', inplace=True)
	matrix = pd.DataFrame()

	# for each body fetch the aspect between it and the remaining bodies (targets)
	bodies = list(input.index.values)
	for body in bodies:
		targets = copy.deepcopy(bodies)
		# targets.remove(body)
		row = {'body': body}

		source_pos = list(input.loc[body][["sign", "degrees", "minutes"]])
		for target in targets:
			target_pos = list(input.loc[target][["sign", "degrees", "minutes"]])

			# give unique name to each aspect
			# label = body.lower() + '_' + target.lower()
			aspect = calc_aspect(source_pos, target_pos)

			if body != target:
				row[target] = aspect
			else:
				row[target] = "NULL"

		# Pandas expects that each value of a dictionary to be a list
		# Convert dictionary to a dictionary of lists
		dict_data = {k: [v] for k, v in row.items()}

		new_row = pd.DataFrame(dict_data)

		# collect all rows
		matrix = pd.concat([matrix, new_row], ignore_index=True)

	matrix.set_index('body', inplace=True)
	return matrix

# main

# TODO - pass datafile as ARGV
matrix = parse_ephemeris("ephemeris-20230627.dat")
print(matrix)
