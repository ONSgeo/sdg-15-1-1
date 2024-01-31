## Introduction

## Introduction

The Sustainable Development Goals (SDGs) are part of the UN 2030 Agenda for Sustainable Development. The Office for National Statistics (ONS) reports the UK data for the SDG indicators on the [UK Sustainable Development Goals webpage](https://sdgdata.gov.uk/), contributing to progress towards a sustainable global future. 

Included in the 17 SDGs is Goal 15, which aims to ["Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification and halt and reverse land degredation and halt biodiversity loss"](https://sdgs.un.org/goals/goal15). One indicator that supports this goal is **15.1.1: Forest area as a proportion of total land area**. 

This code aims to provide an automated calculation of SDG indicator 15.1.1 for the timely reporting on progress towards Goal 15. The most recent reporting of this indicator by the UK covers the years [2013-2022](https://sdgdata.gov.uk/15-1-1/).

## Set-up 
Usage
1. Clone this repository into the directory you'd like to work from.

2. In the command-line interface, navigate to the root folder of the project and enter:

    `pip install .`

3. Create a .env file to set the user parameters. To do this, open Notepad and write ROOT_DIR= and the directory you'd like to work from, eg:

    `ROOT_DIR=C:\Users\username\scripts\sdg15_1_1`
    
    Save this notepad as a `.env` file (by simply saving as `.env`) in the main directory you'd like to work from.

4. The **UserParams class (found in `user_params.py`) is where unique parameters are defined for the SDG indicator calculation.**
   
   It will make the assumption that input data will be located in the main directory within a folder named sdg_x_x_x_data, unless you specify a different `data_dir`, eg:
   
   if `self.data_dir: Optional[str] = None`:
   
   data will be stored in: `C:\Users\username\scripts\SDGs\sdg_x_x_x_data`

   else if `self.data_dir: Optional[str] = "C:\Users\username\somewhere_else"`:

   data will be stored in: `C:\Users\username\somewhere_else`

   This is also true for the output directory, where the default directory for output data will be: 'C:\Users\username\scripts\SDGs\sdg_x_x_x_output'

   For this SDG indicator the other user parameters are:
     - `year_start`: The starting year for multiple year exports or the ONLY year for single year exports
     - `year_end`: The ending year for multiple year exports
     - `single_year_test`: Boolean flag to only test a single year or multiple
     - `lad_file_path`: The specific path to the LAD file for the single year
     - `sam_file_path`: The specific path to the SAM file for the single year
     - `nfi_file_path`: The specific path to the NFI file for the single year


## Usage 
?

## Input Data

This SDG indicator requires 2 distinct data types to be input: 

1. **A spatial representation of forest or woodland areas in the country of interest.** A forest or woodland is defined by the UN as being over 0.5 hectare with canopy cover of 10% (or the potential to achieve it), however this defintion is variable between countries. The likely format for this data is .shp. 

2. **A spatial representation of total land cover of the country of interest.** If boundaries for statistical geogrpahies are present, these can provide data for this indicator for these specific areas. Where present, full resolution and extent should be used. The likely format of this data is .shp. 

Data used to calulate this SDG should be sampled from the same year.   

Since the United Kingdom is made up of four countries, each with their own methods of collecting and publishing data, total input data may amount to more than 2 sources. The SDG indicator should only be calulated using this code for countries where a full input dataset is available. 

[Further detail on requirements for SGG 15.1.1 as specified by the UN.](https://unstats.un.org/sdgs/metadata/files/Metadata-15-01-01.pdf) 

### Previously used data sources
    
Great Britain (forest cover): Forest Research Open Data.
(https://www.forestresearch.gov.uk/tools-and-resources/fthr/open-data/)
    
Great Britain (land area): Local Authority Districts (BFE), ONS Open Geography Portal. 
(https://geoportal.statistics.gov.uk/)
        

## Methodology


       

## Outputs

SDG15_1_1_Calculate.ipynb produces outputs for each specified year as a .csv file (forest area as a proportion of total land area for       each specified land division) and a.jpeg (choropleth map of forest area as a proportion of total land area). 
    
  SDG15-1_1_Analysis.ipynb allows plotting of a time series of forest area as a proportion of total land area for each land division         across available years.   
       

### Considerations


### Definitions	

 

**Land area**  is the country area excluding area under inland waters and coastal waters. For this analysis, total land area is calculated using Standard Area Measurements (**SAM**) available on the [ONS Open Geography portal](https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_SAM)). All measurements provided are ‘flat’ as they do not take into account variations in relief e.g. mountains and valleys. Measurements are given in hectares (10,000 square metres) to 2 decimal places. Four types of measurements are included: total extent (AREAEHECT), area to mean high water (coastline) (AREACHECT), area of inland water (AREAIHECT) and area to mean high water excluding area of inland water (land area) (AREALHECT) which is the type used for this analysis.


    
       
