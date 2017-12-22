#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import re

#read the city positions
locationsFile = open("cityLocations.txt", encoding='iso-8859-1')
lines = [line.rstrip('\n') for line in locationsFile]
positionsList = []
positionsMap = dict()
namedPositions = dict()
for line in lines:
	positionMatch = re.search("([0-9]+)\t(.+)", line)
	if (positionMatch):
		positionsList.append(positionMatch.group(1))
		positionsMap[positionMatch.group(1)] = positionMatch.group(2)
		namedPositions[positionMatch.group(2)] = positionMatch.group(1)
locationsFile.close()

# read in the province mappings
provinceMappingsFile = open('province_mappings.txt', encoding='iso-8859-1')
lines = [line.rstrip('\n') for line in provinceMappingsFile]
provinceMappings = dict()
namedMappings = dict()
mappingsByName = dict()
for line in lines:
	if len(line) == 0: continue
	if line[0] == '#': continue
	if line[0] == '}': break
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
				namedMappings[HoI4Province] = HoI4Name.group(1)
			mappingsByName[HoI4Name.group(1)] = HoI4Provinces
provinceMappingsFile.close()

# Check city positions against mappings, report positional mismatches
outputFile = open('badpositions.txt', "w+", encoding='iso-8859-1');
for position in positionsList:
	mapping = provinceMappings.get(position)
	if (mapping[0] != position) and (positionsMap.get(position) == namedMappings.get(position)):
		outputString = "HoI4 province " + position + " was not first in its mapping! Locations name: " + positionsMap.get(position) + "\tMapping name: " + namedMappings.get(position) + "\n"
		outputFile.write(outputString)
outputFile.close();

# Check city positions against mappings, report mapping mismatches
outputFile = open('badmappings.txt', "w+", encoding='iso-8859-1');
for namedPosition, position in namedPositions.items():
	if namedPosition in mappingsByName:
		mapping = mappingsByName[namedPosition]
		mappingMatched = False
		for provNum in mapping:
			if provNum == position:
				mappingMatched = True
				break
		if not mappingMatched:
			outputString = "The city " + namedPosition + " at position " + position + " was not in the correct mapping!\n"
			outputFile.write(outputString)
outputFile.close();

# Check for names that don't match
outputFile = open('unmatched names.txt', "w+", encoding='iso-8859-1');
for namedPosition, position in namedPositions.items():
	if namedPosition not in mappingsByName:
		outputFile.write("\"" + namedPosition + "\" (" + position + ") did not match any province mappings. The mapping at that position was \"" + namedMappings[position] + "\"\n")
outputFile.close()