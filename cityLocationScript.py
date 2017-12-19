#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import re

locationsFile = open("cityLocations.txt", encoding='iso-8859-1')
lines = [line.rstrip('\n') for line in locationsFile]
positions = []
for line in lines:
	positionMatch = re.search("([0-9]+)\t(.+)", line)
	if (positionMatch):
		positions.append(positionMatch.group(1))
locationsFile.close()

for position in positions:
	print(position)

input("Press enter to continue")