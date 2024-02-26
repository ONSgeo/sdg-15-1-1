## Introduction


The Sustainable Development Goals (SDGs) are part of the UN 2030 Agenda for Sustainable Development. The Office for National Statistics (ONS) reports some of the UK data for the SDG indicators on the [UK Sustainable Development Goals webpage](https://sdgdata.gov.uk/), contributing to progress towards a sustainable global future. 

Included in the 17 SDGs is Goal 15, which aims to ["Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification and halt and reverse land degradation and halt biodiversity loss"](https://sdgs.un.org/goals/goal15). One indicator that supports this goal is **15.1.1: Forest area as a proportion of total land area**. 

This code aims to provide an automated calculation of SDG indicator 15.1.1 for the timely reporting on progress towards Goal 15. The most recent reporting of this indicator by the UK covers the years [2013-2022](https://sdgdata.gov.uk/15-1-1/).


## Set-up


1. **Clone this repository** into the root directory you'd like to work from. 

2. **Install the SDG base class:** Open git BASH in the cloned repository and run the following two commands:

    ```git submodule init```

    ```git submodule update```

   The SDG base class handles methods common to all SDG indicator calculations and can be found in [this repository](https://github.com/ONSgeo/sdg_base).

3. **Create an environment variable** to set the address of the root directory. Using environment variables negates the need to enter personal information into the script. Open Notepad and write:

    `ROOT_DIR=C:\root\directory\address`
    
    Save this as the extension ".env" in the root directory. 

4. **Specify user parameters:** `user_params.py` requires user input:

- `root directory`: will be taken from the environment variable.
- `data_dir`: refers to the location of input data. If none is provided, it will assume the data is located within the root directory, in a folder named "sdg_x_x_x_data".
- `output_dir`: refers to the location in which outputs should be stored. If none is provided, data will be output to the root directory as "sdg_x_x_x_output".
- `single_year_test`: set to True if only calculating for a single year.
- `year_start`: expects the starting year for multiple exports. If calculating for a single year, this will be the date of that year.
- `year_end`: expects the ending year for multiple year exports. If calculating for a single year, this will take None.
- `lad_file_path`: takes the specific path to the LAD file for the single year.
- `sam_file_path`: takes the specific path to the SAM file for the single year.
- `nfi_file_path`: takes the specific path to the NFI file for the single year.
- `save_shp_file`: will save results as shapefiles if set to True. This will impact performance speed. 


## Usage


`SDG15_1_1_Calculate.ipynb` calculates SDG 15.1.1 for each specified year.
    
`SDG15-1_1_Analysis.ipynb` allows for the plotting of a time series of SDG 15.1.1 across available years.   
       
### Input Data

This SDG indicator requires 2 distinct data types to be input: 

1. **A spatial representation of forest or woodland areas in the country of interest.** The assumed format for this data is .shp. 

3. **Standard Area Measurements for the land of interest**. This provides the total land area to divide land area covered by forest by. The higher the granularity of these areas, the more detailed the output. The assumed format of this data set is .csv. 

2. **Boundaries of administrative areas.** These provide spatial context for the standard area measurements and as such should match the granularity of areas with available standard area measurements. Where present, full resolution and extent should be used. The assumed format of this data is .shp.

Each data source used to calculate this SDG should be sampled from the same year(s).   

Since the United Kingdom is made up of four countries, each with their own methods of collecting and publishing data, total input data may amount to more than 2 sources. The SDG indicator should only be calculated for countries where a full input dataset is available. 

[Further detail on requirements for SGG 15.1.1 as specified by the UN.](https://unstats.un.org/sdgs/metadata/files/Metadata-15-01-01.pdf) 

### Methodology

1. A new geo-dataframe is created from the "Woodland" column of forest geo-dataframe. 

2. Standard area measurements (dataframe) are merged with administrative boundaries (geo-dataframe) on a shared column, creating a new geo-dataframe with spatial context to standard area measurements. The shared column is calculated automatically based upon similarity and is likely to be area name or code. 

3. A spatial join is conducted between this new geo-dataframe and woodland geo-dataframe. The resultant geo-dataframe contains information on how much total land there is within an administrative boundary, and how much forest cover there is within that same boundary. It also retains its geometry column and can be plotted.

4. ((area covered by woodland / total land area) *100) yields the forest area as a percentage of total land area.

Full programmatic calculation and methodology is found within `in sdg_15_1_1_src/sdg_15_1_1.py`. 

### Outputs

Currently available outputs include:

- Forest area as a proportion of total land area for each specified land division (csv).
- Choropleth map of forest area as a proportion of total land area (jpeg).
- Optional shapefile for further geospatial analysis. 

    
## Notes


### Previously used data sources
    
Great Britain (forest cover): Forest Research Open Data.
(https://www.forestresearch.gov.uk/tools-and-resources/fthr/open-data/)

Great Britain (land area): Standard Area Measurements (SAM), ONS Open Geography Portal. 
(https://geoportal.statistics.gov.uk/)

Great Britain (administrative areas): Local Authority Districts (BFE), ONS Open Geography Portal. 
(https://geoportal.statistics.gov.uk/)

### Considerations 

- The methodology of this indicator calculation is based upon assumed input data formats (see methodology). If better input data is found in an alternative format, methodology may need to be adjusted accordingly.
- The definition of what constitutes a forest is variable across countries and may cause discrepancies in this calculation. 
- Standard Area Measurements and other land cover estimates do not usually account for land relief and therefore come with an inherent degree of inaccuracy.
- Please consult the [UN indicator requirements](https://unstats.un.org/sdgs/metadata/files/Metadata-15-01-01.pdf) for further considerations.

### Future work

- The input data and methodology should be comprehensively compared against [UN specified requirements](https://unstats.un.org/sdgs/metadata/files/Metadata-15-01-01.pdf) when considering improvements.
-  As you might be able to tell, this was our first go at a reproducible calculation for an SDG indicator and there are a couple of rookie mistakes. The most annoying is perhaps that the column containing the land cover of interest is specified in the script as "woodland" and this is not set to be modifiable within the user parameters. If the land cover of interest is not "Woodland" (perhaps it's recorded instead as "Forest") this will need to be modified within `sdg_15_1_1_src/sdg_15_1_1.py`. Please consider using a similar structure to that found in SDG-11-3-1 where these problems have been accounted for.
-  The methodology of this calculator takes input data saved locally. The ability to directly stream input data, through an API or otherwise, is desirable but dependent on the data source. 
   

#### Authors

Ed Cuss (EdCussONS) & Lucy Astley-Jones (LucyAstleyJonesONS).
