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
import datetime
from operator import itemgetter
import gpxpy
import pyexiv2

'''
Each point is a (latitude, longitude, date, name) pair
e.g. (49.5, -123, datetime(), 'IMG_123.JPG')


sort with sorted(points, key=itemgetter(2, 3))
'''

points = []
def latitude(XmpLatitude):
    '''
    Converts a latitude pyexiv2.utils.GPSCoordinate to a decimal representation
    
    The builtin conversion looses decimal places
    '''
    
    degrees,minutes = XmpLatitude[0:-1].split(',')
    degrees = int(degrees)
    minutes = float(minutes)
    direction = (1 if XmpLatitude[-1] == 'N' else -1)
    
    return direction * (float(degrees) + float(minutes)/60.)
           

def longitude(XmpLongitude):
    degrees,minutes = XmpLongitude[0:-1].split(',')
    degrees = int(degrees)
    minutes = float(minutes)
    direction = (1 if XmpLongitude[-1] == 'E' else -1)
    
    return direction * (float(degrees) + float(minutes)/60.)
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A program that makes a gpx track from geotagged images')
    parser.add_argument('-t', '--time', default=15, type=float, help='Start a new track after an interval this long in minutes without images')
    parser.add_argument('gpx', nargs='?', type=argparse.FileType('w'))
    parser.add_argument('images', nargs='+', type=argparse.FileType('r'), metavar='image')
    opts=parser.parse_args()
    
    for image in opts.images:
        metadata = pyexiv2.ImageMetadata(image.name)
        metadata.read()
        
        
        if 'Xmp.exif.GPSLatitude' in metadata and 'Xmp.exif.GPSLongitude' in metadata:
        
            if 'Xmp.exif.GPSMapDatum' in metadata and metadata['Xmp.exif.GPSMapDatum'].value != u'WGS-84':
                print 'Unknown GPSMapDatum found in %s:%s' % (image.name, metadata['Xmp.exif.GPSMapDatum'])
            
            if 'Xmp.exif.DateTimeOriginal' not in metadata:
                print 'No timestamp found for %s.' % image.name
                # do what with these?


            points.append(
                    (latitude(metadata['Xmp.exif.GPSLatitude'].raw_value), longitude(metadata['Xmp.exif.GPSLongitude'].raw_value), 
                    metadata['Xmp.exif.DateTimeOriginal'].value, image.name))
    
    
    '''
    GPXTrack made of GPXTrackSegments
    
    '''
    trackpoints = []
    lasttime = None
    gpx_track=gpxpy.gpx.GPXTrack('foo','bar')
    
    for point in sorted(points, key=itemgetter(2, 3)):
    
        if len(trackpoints) > 0 and (point[2] - lasttime) > datetime.timedelta(minutes=opts.time):
            print 'found segment...'
            gpx_track.segments.append(gpxpy.gpx.GPXTrackSegment(trackpoints))
            trackpoints = []
            
        trackpoints.append(gpxpy.gpx.GPXTrackPoint(point[0], point[1], None, point[2], point[3]))
        lasttime = point[2]
        
    if len(trackpoints) > 0:
        print 'cleaning up...'
        gpx_track.segments.append(gpxpy.gpx.GPXTrackSegment(trackpoints))
        trackpoints = []
    gpx = gpxpy.gpx.GPX(tracks=[gpx_track])
    opts.gpx.write(gpx.to_xml())
    opts.gpx.close()