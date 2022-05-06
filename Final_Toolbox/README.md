# Python Toolbox for Hydrological Analysis: Pond and Lake Mapping
## Script by Ryan Fritz

## PURPOSE OF THIS SCRIPT:
##### Hydrological analyses include identifying water resource areas, analyzing the flow of water over a landscape,
### mapping the area of a watershed, and assessing flood risks. Specifically, this script will use
### four tools to enable anyone in the field of hydrology to map real ponds and lake using an input DEM
### (Digital Elevation Model). A DEM is a raster type where each cell value represents elevation within the cell. Using a
### DEM, one can locate the areas of depressions (sinks) in the ground that retain water a.k.a ponds and lakes!

##                                       TOOLS IN THE TOOLBOX

## The Flow Direction Tool
### PURPOSE: The Flow Direction tool will determine direction of flow by the direction of
### steepest descent, or maximum drop, from each cell in the DEM raster.
### WHAT THIS TOOL DOES: Creates a raster of flow direction from each cell to its downslope neighbor or neighbors.
### More information on the Flow Direction tool -->https://pro.arcgis.com/en/pro-app/2.8/tool-reference/spatial-analyst/flow-direction.htm

## The Sink Tool
### PURPOSE: The Sink tool is used to identify real and artificial sinks in the DEM raster. Artificial sinks are not real
### water bodies and are caused from random errors in the DEM.
### WHAT THIS TOOL DOES: Creates a raster identifying all sinks or areas of internal drainage.
### More information on the Sink tool --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/spatial-analyst/sink.htm

## The Region Group Tool
### PURPOSE: Real water bodies are made up of many pixels but artificial sinks are made up of one or two pixels.
### The Region Group tool will filter out artificial sinks by their size. Sinks will become a pixel group with a Object ID
### and count field indicating how many pixels are in the group.
### WHAT THIS TOOL DOES: For each cell in the output, the identity of the connected region to which
### that cell belongs is recorded. A unique number is assigned to each region.
### More information on the Region Group tool --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/spatial-analyst/region-group.htm

## The Set Null Tool
### PURPOSE: To extract real sinks from the DEM. Artificial sinks will be set to a null value and real sinks set to a
### value of one.
### WHAT THIS TOOL DOES: Set Null sets identified cell locations to NoData based on a specified
### criteria. It returns NoData if a conditional evaluation is true, and returns the value specified by
### another raster if it is false.
### More information on the Set Null tool --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/spatial-analyst/set-null.htm

![lake](https://upload.wikimedia.org/wikipedia/commons/8/80/Rhode_Island_Rams_logo.svg)
:droplet: :fishing_pole_and_fish:
