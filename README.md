# planetary-aspects

Supply a function 'aspects' which  can be used to calculate angular aspects between
two celestial bodies on the the equator.

The positions are anticipated to be taken from a standard ephemeris.

ARGS:
```
	- pos1 - List [ sign, degrees, minutes ]
	- pos2 - List [ sign, degrees, minutes ]
```

DESCRIPTION:
	Each sign is assigned an offset from 0 degrees Aries.
	Minutes are coverted to decimal values.
	Positions are calculated based on the above.

RETURN: 
	Decimal difference between the two positions		

FILES:
```
	LICENSE - standard MIT license suggested by Github
	README.md - this file
	aspects.py - function as well as sample usage
```

