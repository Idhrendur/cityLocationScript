#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import re

locationsFile = open("cityLocations.txt", encoding='iso-8859-1')
lines = [line.rstrip('\n') for line in locationsFile]
for line in lines:
	print(line)
locationsFile.close()

input("Press enter to continue")