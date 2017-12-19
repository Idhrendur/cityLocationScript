#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import re

#read the city positions
locationsFile = open("cityLocations.txt", encoding='iso-8859-1')
lines = [line.rstrip('\n') for line in locationsFile]
positionsList = []
positionsMap = dict()
for line in lines:
	positionMatch = re.search("([0-9]+)\t(.+)", line)
	if (positionMatch):
		positionsList.append(positionMatch.group(1))
		positionsMap[positionMatch.group(1)] = positionMatch.group(2)
locationsFile.close()

# read in the province mappings
provinceMappingsFile = open('province_mappings.txt', encoding='iso-8859-1')
lines = [line.rstrip('\n') for line in provinceMappingsFile]
provinceMappings = dict()
provinceNames = dict()
for line in lines:
	if len(line) == 0: continue
	if line[0] == '#': continue
	Vic2Match = re.search("(vic2 = )([0-9]+)", line)
	if (Vic2Match):
		HoI4Matches = re.finditer("(hoi4 = )([0-9]+)", line)
		if (HoI4Matches):
			HoI4Name = re.search("# (.+)( ->)", line)
			HoI4Provinces = []
			for HoI4Match in HoI4Matches:
				HoI4Provinces.append(HoI4Match.group(2))
			for HoI4Province in HoI4Provinces:
				provinceMappings[HoI4Province] = HoI4Provinces
				provinceNames[HoI4Province] = HoI4Name.group(1)
provinceMappingsFile.close()

# Check city positions against mappings, report mismatches
outputFile = open('output.txt', "w+", encoding='iso-8859-1');
for position in positionsList:
	mapping = provinceMappings.get(position)
	if mapping[0] != position:
		outputString = "HoI4 province " + position + " was not first in its mapping! Locations name: " + positionsMap.get(position) + "\tMapping name: " + provinceNames.get(position) + "\n"
		outputFile.write(outputString)
outputFile.close();