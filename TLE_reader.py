# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 12:38:24 2021

@author: YoSke
"""

from tletools import TLE

tle_string = """
NSS-9
1 33749U 09008A   21309.77806091  .00000079  00000-0  00000-0 0  9992
2 33749   0.0228   1.3579 0002100 218.9799 288.0653  1.00271016 46643
"""

tle_lines = tle_string.strip().splitlines()

tle = TLE.from_lines(*tle_lines)

print(tle)