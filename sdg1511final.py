# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 11:36:12 2022

@author: shavar
"""
#project: SDG indicator 15.1.1: Forest area as a proportion of total land area

#import libraries
from pathlib import Path
import geopandas as gpd
import pandas as pd
from pandas import DataFrame, merge
import numpy as np
import matplotlib.pyplot as plt
import shapely
import csv


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
    # import forst and lad boundaries as geodataframes and SAM as csv
    nfi19ni = open_geodataframe(r'D:\SDGs\SDG_15_1_1\data\NIforest\draftNIWoodlandBasemapAtApril2019.shp')
    print(nfi19ni.head())
    sam19lad = open_dataframe_csv(r'D:\SDGs\SDG_15_1_1\data\SAM_AdministrativeAreas_2019\SAM_LAD_DEC_2019_UK.csv',cols=['LAD19CD','LAD19NM','AREALHECT'],index='LAD19CD')
    print(sam19lad.head())
    lad19bfe = open_geodataframe(r'D:\SDGs\SDG_15_1_1\data\LAD\Local_Authority_Districts__December_2019__Boundaries_UK_BFE.shp')
    print(lad19bfe.head())
    
    # do spatial join between forest layer and lad boundaries layer
    gdf_join_ni = gpd.sjoin(nfi19ni, lad19bfe, how='left')
    print(gdf_join_ni.head())
    
    # group by LAD19CD
    gdf_join_ni_groupbylad = gdf_join_ni.groupby(['LAD19CD'])
    print(gdf_join_ni_groupbylad.head())
    
    # merge gdf_join_ni and SAM csv to add lad area column to gdf_join_ni and calculate area
    gdf_join_ni_merge_sam19lad = gdf_join_ni.merge(sam19lad, on='LAD19CD')
    print(gdf_join_ni_merge_sam19lad.head())
    
    
