import random

# Configuration
revtend = -3 # Value added to the checksum in revision
outskirts = 0 # Value given to locations out of render dimensions
map_min = -16 # Minimum coordinate (map dimensions)
map_max = 16 # Maximum coordinate (map dimensions)
#random.seed(1337) # Seed for rng

mapdata = {}

def show_map(passdata):
	# Characters used for printing map data to the shell
	chars = {'0.0':'  ', '0.1':'░░', '0.2':'░░', '0.3':'▒▒',  '0.4':'▒▒', '0.5':'▒▒', '0.6':'▒▒', '0.7':'▓▓', '0.8':'▓▓', '0.9':'██', '1.0':'██'}

	for y in range(map_min, map_max+1):
		lineout = ''
		for x in range(map_min, map_max+1):
			lineout = lineout+chars[str(abs(round(passdata[str(x)+'|'+str(y*-1)], 1)))]

		print(lineout)

	print('═' * ((abs(map_min) + map_max) * 2 + 2))

def initial_rng():
	return round(random.random(), 3)

def revise(passdata):
	revmap = {}

	for x in range(map_min, map_max+1):
		for y in range(map_min, map_max+1):

			checksum = 0 - passdata[str(x)+'|'+str(y)]
			for x1 in range(x-1, x+2):
				for y1 in range(y-1, y+2):
					try:
						checksum = checksum + passdata[str(x1)+'|'+str(y1)]
					except:
						# 0 emulates water, 1 emulates land around the map
						checksum = checksum + 0

			passvalue = passdata[str(x)+'|'+str(y)]
			revvalue = passvalue * (checksum+revtend)

			# Not happy with solution below, needs improvement
			if revvalue > 1:
				revvalue = 1.0
			elif revvalue < 0:
				revvalue = 0.0

			revmap[str(x)+'|'+str(y)] = revvalue

	return revmap

# Generate the noisemap
for x in range(map_min, map_max+1):
	for y in range(map_min, map_max+1):
		mapdata[str(x)+'|'+str(y)] = initial_rng()

show_map(mapdata)

# Revisions
revision0 = revise(mapdata)
show_map(revision0)

revision1 = revise(revision0)
show_map(revision1)

revision2 = revise(revision1)
show_map(revision2)

#revision3 = revise(revision2)
#show_map(revision3)
