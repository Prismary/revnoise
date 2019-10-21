import random
from PIL import Image, ImageDraw

# Configuration
checkradius = 1 # Radius for calculating the checksum
revtend = 3 # Value added to the checksum in revision
outskirts = 0 # Value given to locations out of render dimensions
map_min = -16 # Minimum coordinate (map dimensions)
map_max = 16 # Maximum coordinate (map dimensions)
random.seed(1337) # Seed for rng

def rng():
	return round(random.random(), 3)

def noise():
	gendata = {}
	for x in range(map_min, map_max+1):
		for y in range(map_min, map_max+1):
			gendata[str(x)+'|'+str(y)] = rng()
	return gendata

def revise(passdata):
	revmap = {}

	for x in range(map_min, map_max+1):
		for y in range(map_min, map_max+1):

			checksum = 0 - passdata[str(x)+'|'+str(y)]
			for x1 in range(x-checkradius, x+checkradius+1):
				for y1 in range(y-checkradius, y+checkradius+1):
					try:
						checksum = checksum + passdata[str(x1)+'|'+str(y1)]
					except:
						# 0 emulates water, 1 emulates land around the map
						checksum = checksum + 0

			revvalue = passdata[str(x)+'|'+str(y)] * (checksum - revtend)

			# Not happy with solution below, needs improvement
			if revvalue > 1:
				revvalue = 1.0
			elif revvalue < 0:
				revvalue = 0.0

			revmap[str(x)+'|'+str(y)] = revvalue

	return revmap

def show_map(passdata):
	# Characters used for printing map data to the shell
	chars = {'0.0':'  ', '0.1':'░░', '0.2':'░░', '0.3':'▒▒',  '0.4':'▒▒', '0.5':'▒▒', '0.6':'▒▒', '0.7':'▓▓', '0.8':'▓▓', '0.9':'██', '1.0':'██'}

	for y in range(map_min, map_max+1):
		lineout = ''
		for x in range(map_min, map_max+1):
			lineout = lineout+chars[str(abs(round(passdata[str(x)+'|'+str(y*-1)], 1)))]

		print(lineout)

	print('═' * ((abs(map_min) + map_max) * 2 + 2))

def export_map(passdata):
	color = {'blue':(50, 123, 240), 'yellow':(222, 210, 33), 'green':(40, 165, 40), 'grey':(148, 148, 148)}
	img_dim = abs(map_min)+map_max+1
	img = Image.new('RGB', (img_dim, img_dim))
	px = img.load()

	for item in passdata:
		if passdata[item] <= 0.2: # Water
			px[int(item.split('|')[0]) + map_max, int(item.split('|')[1]) * -1 + map_max] = color['blue']
		elif passdata[item] <= 0.5: # Beach
			px[int(item.split('|')[0]) + map_max, int(item.split('|')[1]) * -1 + map_max] = color['yellow']
		elif passdata[item] <= 0.9: # Grass
			px[int(item.split('|')[0]) + map_max, int(item.split('|')[1]) * -1 + map_max] = color['green']
		elif passdata[item] <= 1.0: # Mountain
			px[int(item.split('|')[0]) + map_max, int(item.split('|')[1]) * -1 + map_max] = color['grey']

	img.save('map.png')

mapdata = noise()
show_map(mapdata)

# Revisions
revision0 = revise(mapdata)
show_map(revision0)

revision1 = revise(revision0)
show_map(revision1)

#revision2 = revise(revision1)
#show_map(revision2)

export_map(revision1)
