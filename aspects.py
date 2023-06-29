
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

def aspect (pos1, pos2):
	""" return the difference in degrees between two ojects on the astral plane
		ARGS:
			- pos1 - List [ sign, degrees, minutes ]
			- pos2 - List [ sign, degrees, minutes ]

		DESCRIPTION:
			Each sign is assigned an offset from 0 degrees Aries.
			Minutes are coverted to decimal values.
			Positions are calculated based on the above.

		RETURN: 
			Decimal difference betwwen the two positions
	"""

	# extract list values
	sign1,deg1,min1 = pos1
	sign2,deg2,min2 = pos2
	
	# calculate the positions = offet + degrees + (decimal) minutes
	position1 = offset[sign1] + deg1 + (round(min1*10/6)/100)
	position2 = offset[sign2] + deg2 + (round(min2*10/6)/100)

	aspect = abs(position2 - position1)

	# Normalize the data (retrn the lesser value if over 180 degrees)
	if aspect > 180:
			aspect = 360 - aspect

	return aspect

# main - sample usage follows

# pos = [ sign, degrees, minutes ]
pos1 = [ 'Ari', 1, 0 ]      # position of first body is 1 deg. Aries
pos2 = [ 'Vir', 21, 48 ]    # position of secod body is 21 deg., 48 min Virgo

angle = aspect(pos1, pos2)
print(f"angle between the two bodies is: {angle}")
