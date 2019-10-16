import random
#random.seed(1337)

mapdata = {}

# Map dimensions
map_min = -16
map_max = 16

# Generate a fitting spacer
spacer_len = (map_min * -1 + map_max) * 2
spacer = ''
for i in range(0, spacer_len+2):
	spacer = spacer + '═'


def show_map(passdata):
	# Characters used for printing the map to the shell
	chars = {'0':'  ', '1':'██'}

	for y in range(map_min, map_max+1):
		lineout = ''
		for x in range(map_min, map_max+1):
			lineout = lineout+chars[str(passdata[str(x)+'|'+str(y*-1)])]

		print(lineout)

	print(spacer)

def initial_rng():
	return random.randrange(0, 2)

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

			if checksum < 4:
				revmap[str(x)+'|'+str(y)] = 0
			elif checksum > 4:
				revmap[str(x)+'|'+str(y)] = 1
			else:
				revmap[str(x)+'|'+str(y)] = passdata[str(x)+'|'+str(y)]
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

revision3 = revise(revision2)
show_map(revision3)
