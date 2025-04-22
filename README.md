# <code style="color : red">This repo has been archived April 2025</code>

## Introduction

The Sustainable Development Goals (SDGs) are part of the UN 2030 Agenda for Sustainable Development. The Office for National Statistics (ONS) reports some of the UK data for the SDG indicators on the [UK SDG data website](https://sdgdata.gov.uk/).


Included in the 17 SDGs is Goal 15, which aims to ‘Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss’. One of the goal 15 indicators that, until recently, remained unreported for the UK, is **15.1.1: ‘Forest area as a proportion of total land area’**. 

### Definitions	

According to the FAO, Forest is defined as: “land spanning more than 0.5 hectares with trees higher than 5 meters and a canopy cover of more than 10 percent, or trees able to reach these thresholds in situ. It does not include land that is predominantly under agricultural or urban land use”. In the United Kingdom, forest is defined as below:

**Forest/woodland** all forest and woodland area over 0.5 hectare with a minimum of 20% canopy cover (25% in Northern Ireland) (or the potential to achieve it) and a minimum width of 20 metres, including areas of new planting, clearfell, windblow and restocked areas. This differs from the UN definition for which the minimum canopy cover is 10% (or the potential to achieve it)

**Land area**  is the country area excluding area under inland waters and coastal waters. For this analysis, total land area is calculated using Standard Area Measurements (**SAM**) available on the [ONS Open Geography portal](https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_SAM)). All measurements provided are ‘flat’ as they do not take into account variations in relief e.g. mountains and valleys. Measurements are given in hectares (10,000 square metres) to 2 decimal places. Four types of measurements are included: total extent (AREAEHECT), area to mean high water (coastline) (AREACHECT), area of inland water (AREAIHECT) and area to mean high water excluding area of inland water (land area) (AREALHECT) which is the type used for this analysis.

### Data
       Forest/Woodland data - Forest Services (GB) and DAERA (NI)
       Land area - Local authority districts (LADs) boundaries from ONS Open Geography portal
       SAM for LADs from ONS Open Geography portal


### Methodology
       Forest area as a proportion of total land area (PFATLA) = Forest area (reference year)/Land area (reference year)*100           

### Analysis
       function to call forest layer
       function to call land area/boundary layer
       intersection analysis to spatially join and attribute forest parcels to LAD boundaries
       join intersect output to SAM
       calculate Forest area as a proportion of total land area (PFATLA)
       
       
### Outputs
       table with LAD codes and forest area, SAM and PFATLA and geometry for plotting
       



