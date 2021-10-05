library("dplyr")
library("sf")
library("tmap")
library("lwgeom")

setwd("D:\\Research\\QA_15_1_1")

#Import data
lad <- st_read("Data\\NI_LADs_BNG\\LADs_December_2016_BFE_NI_BNG.shp")
forest <- st_read("Data\\ForestServiceDatasetsForONS_NIForest\\draftNIWoodlanBasemapAtApril2015.shp")
sam <- read.csv("Data\\SAM_for_Administrative_Areas_2015\\SAM_LAD_DEC_2015_UK.csv", colClasses = c("LAD15CD" = "character", "LAD15NM" = "character"))

#British National Grid
bng <- "+init=epsg:27700 +proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +datum=OSGB36 +units=m +no_defs +ellps=airy +towgs84=446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894"

#Convert layers to BNG
lad <- st_transform_proj(lad, bng)
forest <- st_transform_proj(forest, bng)

### Check if geometries are valid
if(any(st_is_valid(lad) == FALSE) == TRUE){
  message("Geometry issues detected - running st_make_valid to correct ")
  lad <- st_make_valid(lad)
}

if(any(st_is_valid(forest) == FALSE) == TRUE){
  message("Geometry issues detected - running st_make_valid to correct ")
  forest <- st_make_valid(forest)
}


#Select forest features wholely within lads to remove them from forest and speed up intersection of lad boundary straddling forests (next step)
contained_forest_list <- st_contains(lad, forest)
contained_forest <- forest[unlist(contained_forest_list), ]

#Select forest polygons which straddle lad boundaries.
straddling_forest <- forest[-unlist(contained_forest_list), ]

#Intersect lad and straddling_forest to split forest polygons and assign containing LAD code 
straddling_intersection <- st_intersection(lad, straddling_forest)

#Assign lad code to contained_forest polygons by joining contained_forest and lad
contained_forest <- st_join(contained_forest, lad)

#Combine contained_forest and straddling_intersection dataframes
intersection <- rbind(contained_forest, straddling_intersection)

#Calculate forest area for each LAD
intersection$forest_area_ha <- as.numeric(units::set_units(st_area(intersection), ha))

#Group features by LAD and summarise by summing total area
#Need to drop geometry otherwise process trys to run spatially and takes ages
summary <- intersection %>% 
  st_set_geometry(NULL) %>% 
  group_by(lad15cd) %>% 
  summarise(forest_area_ha = sum(forest_area_ha))

#Join SAM to summary for later 15.1.1 calculation
summary <- left_join(summary, sam, by = c("lad15cd" = "LAD15CD"))

#Calculate 15.1.1: forest area as percentage of total land area
summary$SDG_15_1_1 <- (summary$forest_area_ha / summary$AREALHECT)*100

#Produce dataframe for output
output <- summary[ , c("lad15cd", "LAD15NM", "forest_area_ha", "AREALHECT", "SDG_15_1_1")]

#Rename columns for output
output <- output %>% rename(lad_area_ha = AREALHECT)

#Output spreadsheet of areas and results
write.csv(output, "Output/QA_15_1_1.csv", row.names = FALSE)
