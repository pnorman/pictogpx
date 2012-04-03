#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	This file is part of pictogpx.

	pictogpx is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	pictogpx is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with pictogpx.  If not, see <http://www.gnu.org/licenses/>.

	Copyright 2012 Paul Norman
'''

import argparse
import sys

import gpxpy
import pyexiv2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A program that makes a gpx track from geotagged images')
    parser.add_argument('-t', '--time', default=15, type=float, help='Start a new track after an interval this long in minutes without images')
    parser.add_argument('gpx', nargs='?', type=argparse.FileType('w'))
    parser.add_argument('images', nargs='+', type=argparse.FileType('r'), metavar='image')
    print parser.parse_args()
    
    