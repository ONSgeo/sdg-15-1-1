## Introduction

The Sustainable Development Goals (SDGs) are part of the UN 2030 Agenda for Sustainable Development. The Office for National Statistics (ONS) reports the UK data for the SDG indicators on the [UK SDG data website](https://sdgdata.gov.uk/).


Included in the 17 SDGs is Goal 15, which aims to ‘Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss’. One of the goal 15 indicators that, until recently, remained unreported for the UK, is **15.1.1: ‘Forest area as a proportion of total land area’**. 

This code aims to provide a means to report on the status of SDG 15.1.1 in the UK from available open data. It is hoped that the base class included will also provide a starting point to analyse additional SDGs.  

### Definitions	

According to the Food and Agriculture Organization of the United Nations (FAO), Forest is defined as: “land spanning more than 0.5 hectares with trees higher than 5 meters and a canopy cover of more than 10 percent, or trees able to reach these thresholds in situ. It does not include land that is predominantly under agricultural or urban land use”. In the United Kingdom, forest is defined as below:

**Forest/woodland** all forest and woodland area over 0.5 hectare with a minimum of 20% canopy cover (25% in Northern Ireland) (or the potential to achieve it) and a minimum width of 20 metres, including areas of new planting, clearfell, windblow and restocked areas. This differs from the UN definition for which the minimum canopy cover is 10% (or the potential to achieve it)

**Land area**  is the country area excluding area under inland waters and coastal waters. For this analysis, total land area is calculated using Standard Area Measurements (**SAM**) available on the [ONS Open Geography portal](https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_SAM)). All measurements provided are ‘flat’ as they do not take into account variations in relief e.g. mountains and valleys. Measurements are given in hectares (10,000 square metres) to 2 decimal places. Four types of measurements are included: total extent (AREAEHECT), area to mean high water (coastline) (AREACHECT), area of inland water (AREAIHECT) and area to mean high water excluding area of inland water (land area) (AREALHECT) which is the type used for this analysis.

### Useage
    
    Before using SDG15_1_1_Calulate.ipynb and SDG15_1_1_Analysis.ipynb, a .env file should be made to set the user parameters. To do this,
    open Notepad and write ROOT_DIR= and the main directory you'd like to work from,  eg. ROOT_DR=C:\Users\Your_username\Scripts\sdg15_1_1.     Save this notepad as an ENV file (by simply saving as .env) in the main directory you'd like to work from.

    In order for this to be recognised, python-dotenv must be installed. To do this, go to CMD.exe Prompt in the Anaconda Navigator
    and enter: 
    pip install python-dotenv 
    
    

### Data

       Forest/Woodland data - Forestry Commission Open Data (GB) and DAERA (NI).  
       Land area - Local authority districts (LADs) boundaries from ONS Open Geography portal.
       SAM for LADs from ONS Open Geography portal.

### Methodology
    SDGBase was designed to present a resusable base class applicable to the analysis of multiple SDGs.   

    SDG15_1_1 is a child class of SDGBase and performs functions relevant to the analysis of SDG15_1_1. It is potentially applicable to the
    analysis of further SDGs with input data of a similar structure. 
    
    UserParams class was built to enable the individual user to set the directories from which they will input and output data. 
    
    Once UserParams have been specified, SDG_15_1_1_Calculate.ipynb allows the user to calculate SDG_15_1_1 for multiple years and 
    outputs results for each year  as both a data frame and a choropleth map.   
    
    SDG_15-1_1_Analysis.ipynb offers the user further insight into the data, allowing SDG metrics to be explored by individual land             divisions across time. 
       
### Calculation
    
    Forest area as a proportion of total land area (PFATLA) = Forest area (reference year)/Land area (reference year)*100 

### Analysis

    SDGBase presents an abstract base class enabling the defintion of input and output directories for data analysis, use of relevant
    read methods based on the file extension of inputs, and the joining of dataframes; applicable to 
    analysis of additional SDGs.  
    
    SDG15_1_1 is a child class of SDGBase and allows for the automatic pairing of data input files published in the same year, 
    analysis across multiple years, calculation of SDG15_1_1 and plotting and saving of results.     
    
    SDG_15_1_1_Calculate.ipynb allows the user to calculate SDG_15_1_1 from the file directories specified in UserParams class and produces
    and saves outputs (forest area as a proportion of total land area for each specified land division) for each available year as both a       .csv file and as a choropleth map (.jpeg), with the added option of a .shp file.
    
    SDG_15-1_1_Analysis.ipynb allows plotting of a time series of forest area as a proportion of total land area for each land division         across available years.   
              
### Outputs

    SDG_15_1_1_Calculate.ipynb produces outputs for each specified year as a .csv file (forest area as a proportion of total land area for       each specified land division) and a.jpeg (choropleth map of forest area as a proportion of total land area), with the option to 
    save results as a .shp file. 
    
    SDG_15-1_1_Analysis.ipynb allows plotting of a time series of forest area as a proportion of total land area for each land division         across available years.   
       
       