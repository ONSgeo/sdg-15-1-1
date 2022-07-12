# -*- coding: utf-8 -*-
"""
#author: robert shava
#project: SDG indicator 15.1.1: Forest area as a proportion of total land area
"""
#import libraries
from pathlib import Path
import geopandas as gpd
import pandas as pd
from pandas import DataFrame, merge
import numpy as np
import matplotlib.pyplot as plt
import shapely
import csv

"""
forests = [r'R:\SDGs\SDG_15_1_1\data\gb_nfi\nfi_gb_2017.shp',r'R:\SDGs\SDG_15_1_1\data\gb_nfi\nfi_gb_2018.shp',r'R:\SDGs\SDG_15_1_1\data\gb_nfi\nfi_gb_2019.shp']
lad19BFE = gpd.read_file(r'R:\SDGs\SDG_15_1_1\data\LAD\Local_Authority_Districts__December_2019__Boundaries_UK_BFE.shp')
display(lad19BFE.head())

for forest in forests:
    nfi = gpd.read_file(forest)
    nfi.columns = nfi.columns.str.upper() #capitalise column names
    filt_cat=(nfi['CATEGORY']=='Woodland') # filter olny Woodland from non-woodland
    nfi_wood=nfi.loc[filt_cat]
    nfi_wood_bng = nfi_wood.to_crs(27700) # convert crs to british national grid 
    display(nfi_wood_bng.head()) # check if code has run successfully

"""
# function to open geodataframe of shapefiles with specified parameters
def open_geodataframe(shapefile_path, cols=None, index=None, epsg=27700):
    
    """
    Returns gdf of shapefile. If cols is None, all cols will be returned, else only cols in a list. If index is None, no index will be set

    Parameters:
    -----------
    shapefile_path (str):
        Path to shapefile

    cols (None/list):
        Columns to select. If left as default (None), all columns will be selected (Default=None)

    index (None/str):
        Column to set as index. If left as default (None), no index will be set (Default=None)

    epsg (int):
        EPSG Code for gdf coordinate reference system

    Returns:
    --------
    gdf (gpd.GeoDataFrame):
        Geodataframe of shapefile opened with columns and index set as selected

    """
    shp = Path(str(shapefile_path)).resolve()
    gdf = gpd.read_file(shp)
    if cols:
        gdf = gdf[cols]
    if index:
        gdf = gdf.set_index(index)
    if not gdf.crs.to_epsg() == epsg:  # Set the projection to that defined in epsg in the arguments
        gdf = gdf.to_crs(epsg)
    return gdf



#function to open csv file as a pandas dataframe with specified parameters

def open_dataframe_csv(csv_filepath,cols=None,index=None):
    
    """
    Returns df of csv. If cols is None, all cols will be returned, else only cols in a list. If index is None, no index will be set

    Parameters:
    -----------
    csv_path (str):
        Path to csv

    cols (None/list):
        Columns to select. If left as default (None), all columns will be selected (Default=None)

    index (None/str):
        Column to set as index. If left as default (None), no index will be set (Default=None)

    
    Returns:
    --------
    df (pd.DataFrame):
        pandas Dataframe of csv opened with columns and index set as selected
        
    """
    csv = Path(str(csv_filepath)).resolve()
    df=pd.read_csv(csv)
    if cols:
        df = df[cols]
    if index:
        df = df.set_index(index)
    return df


if __name__ == '__main__':
    nfi19ni = open_geodataframe(r'D:\SDGs\SDG_15_1_1\data\NIforest\draftNIWoodlandBasemapAtApril2019.shp')
    print(nfi19ni.head())
    sam19lad = open_dataframe_csv(r'D:\SDGs\SDG_15_1_1\data\SAM_AdministrativeAreas_2019\SAM_LAD_DEC_2019_UK.csv',cols=['LAD19CD','LAD19NM','AREALHECT'],index='LAD19CD')
    print(sam19lad.head())
    lad19bfe = open_geodataframe(r'D:\SDGs\SDG_15_1_1\data\LAD\Local_Authority_Districts__December_2019__Boundaries_UK_BFE.shp')
    print(lad19bfe.head())
    
#intersect lad boundaries with forest layer to create a spatial join

def do_spatial_join(nfi19ni, lad19bfe):
    """
    Returns spatial join of LAs with forests

    Parameters:
    -----------
    gdf_LA (gpd.GeoDataFrame):
        Geodataframe of Local Authorities

    gdf_forest (gpd.GeoDataFrame):
        Geodataframe of forests

    Returns:
    --------
    gdf_join (gpd.GeoDataFrame):
        GeodataFrame of forests joined to LAS
-
    """
    print("WRITE CODE TO DO JOIN AND RETURN JOINED GDF")
    # CODE
    # return gdf_join
    
    
    
lad19bfe_sam = lad19bfe.merge(sam19lad, on='LAD19CD')    
lad19bfe_sam.head()
lad19bfe_sam.to_file(r'D:\SDGs\SDG_15_1_1\intermediate\lad19bfe_sam.shp')

lad19bfe_samgpd = gpd.read_file(r'D:\SDGs\SDG_15_1_1\intermediate\lad19bfe_sam.shp')
nfi19ni_lad19 = gpd.overlay(nfi19ni, lad19bfe_samgpd, how='intersection')
nfi19ni_lad19.head()
nfi19ni_lad19.to_file(r'D:\SDGs\SDG_15_1_1\intermediate\nfi19ni_lad19.shp')