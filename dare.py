'''
Created on 18 Mar 2017

@author: ash
'''
import matplotlib as mpl
import re
from itertools import product
#mpl.use('Agg')
import matplotlib.mlab as mlab
from matplotlib import ticker
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
from matplotlib.patches import Polygon as MplPolygon
import seaborn as sns
sns.set(style="white")
import operator
import argparse
import sys
from scipy.spatial import ConvexHull
import os
import pdb
import random
import numpy as np
import sys
from os import path
import scipy as sp
import shutil
import logging
import json
import codecs
import pickle
import gzip
from collections import OrderedDict, Counter
from sklearn.preprocessing import normalize
from haversine import haversine
from _collections import defaultdict
from scipy import stats
from mpl_toolkits.basemap import Basemap, cm, maskoceans
from scipy.interpolate import griddata as gd
from shapely.geometry import MultiPoint, Point, Polygon, MultiPolygon
from shapely.ops import cascaded_union, unary_union
import shapefile
from sklearn.cluster import KMeans, MiniBatchKMeans
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

lllat = 24.396308
lllon = -124.848974
urlat =  49.384358
urlon = -66.885444

def union_polygons(list_of_polygons):
    #accept few polygons and return their union, visualize them to make sure it's correct
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, axisbg='w', frame_on=False)
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False) 
    for spine in ax.spines.itervalues(): 
        spine.set_visible(False) 
    m = Basemap(llcrnrlat=lllat,
    urcrnrlat=urlat,
    llcrnrlon=lllon,
    urcrnrlon=urlon,
    resolution='i', projection='cyl')

    m.drawmapboundary(fill_color = 'white')
    #m.drawcoastlines(linewidth=0.2)
    m.drawcountries(linewidth=0.2)
    shp_info = m.readshapefile('../localism/data/us_states_st99/st99_d00','states',drawbounds=False, zorder=0)
    regions = []
    for shapedict,state in zip(m.states_info, m.states):
        if shapedict['NAME'] in set(['California', 'Washington']):
            regions.append(state)
    polies = []
    for r in regions:
        poly = Polygon(r)
        polies.append(poly)
    poly = MultiPolygon(polies)
    poly = unary_union(poly).convex_hull
    lons, lats = poly.exterior.coords.xy
    coords = np.array(zip(lons, lats))

    poly = MplPolygon(coords,facecolor='gray',edgecolor='gray')
    ax.add_patch(poly)
    plt.show()
    result = None
    return result

def read_dare(filename='./geodare.cleansed.filtered.json'):
    records = []
    with open(filename, 'r') as fin:
        for line in fin:
            line = line.strip()
            record = json.loads(line)
            records.append(record)
    dialect_regions = set([records[i]['dialect'] for i in range(len(records))])
    m = Basemap(llcrnrlat=lllat,
        urcrnrlat=urlat,
        llcrnrlon=lllon,
        urcrnrlon=urlon,
        resolution='i', projection='cyl')

    shp_info = m.readshapefile('../localism/data/us_states_st99/st99_d00','states',drawbounds=False, zorder=0)
    dialectregion_coords = {}
    for dialect_region in dialect_regions:
        regions = []
        for shapedict,state in zip(m.states_info, m.states):
            if shapedict['NAME'].lower()==dialect_region:
                regions.append(state)
        if regions:
            '''
            polies = []
            for r in regions:
                poly = Polygon(r)
                polies.append(poly)
            poly = MultiPolygon(polies)
            poly = unary_union(poly).convex_hull
            lons, lats = poly.exterior.coords.xy
            coords = np.array(zip(lons, lats))
            '''
            dialectregion_coords[dialect_region] = regions
    with open('dare_polygon.json', 'w') as fout:
        for dialect, regions in dialectregion_coords.iteritems():
            json.dump({'dialect':dialect, 'polygons':regions}, fout)
             
    pdb.set_trace()
if __name__ == '__main__':
    #union_polygons(list_of_polygons=None)
    read_dare()