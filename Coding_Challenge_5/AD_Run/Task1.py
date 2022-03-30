# For this coding challenge, I want you to practice the heatmap
# generation that we went through in class, but this time obtain your own input data, and I
# want you to generate heatmaps for TWO species.

# You can obtain species data from a vast array of different sources, for example:

# obis - Note: You should delete many columns (keep species name, lat/lon) as OBIS adds
# some really long strings that don't fit the Shapefile specification.
# GBIF
# Maybe something on RI GIS
# Or just Google species distribution data
# My requirements are:

# The two input species data must be in a SINGLE CSV file, you must process the input data to
# separate out the species (Hint: You can a slightly edited version of our CSV code from a
# previous session to do this), I recommend downloading the species data from the same source so the columns match.
# Only a single line of code needs to be altered (workspace environment) to ensure code runs
# on my computer, and you provide the species data along with your Python code.
# The heatmaps are set to the right size and extent for your species input data, i.e. appropriate fishnet cellSize.
# You leave no trace of execution, except the resulting heatmap files.
# You provide print statements that explain what the code is doing, e.g. Fishnet file generated

import arcpy
# Setting my workspace where my files will be stored
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\Data\Students_2022\Fritz\Coding_Challenge_5\AD_Run"
# Converting the Bonefish and Tarpons csv file into a shapefile before generating the heatmap
in_Table = r"BONEFISH_TARPONS_points.csv"
x_coords = "longitude"
y_coords = "latitude"
z_coords = ""
out_Layer = "Bonefish_Tarpons"
saved_Layer = r"Step_1_Bonefish_Tarpons_Species_Output.shp"

# Set the spatial reference
spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

#  see if the output exists in the file
arcpy.CopyFeatures_management(lyr, saved_Layer)
if arcpy.Exists(saved_Layer):
    print("Created file successfully!")

# Extract the Extent
desc = arcpy.Describe(saved_Layer)
XMin = desc.extent.XMin
XMax = desc.extent.XMax
YMin = desc.extent.YMin
YMax = desc.extent.YMax

# Generate fishnet
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)
# Name output fishnet
outFeatureClass = "Fishnet_bonefish_tarpon.shp"

# Set the origin of the fishnet
originCoordinate = str(XMin) + " " + str(YMin)
yAxisCoordinate = str(XMin) + " " + str(YMin + 1)
cellSizeHeight = "0.25"
cellSizeWidth = "0.25"
numRows = ""
numColumns = ""
oppositeCorner = str(XMax) + " " + str(YMax)
labels = "NO_LABELS"
templateExtent = "#"
geometryType = "POLYGON"

arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                               cellSizeWidth, cellSizeHeight, numRows, numColumns,
                               oppositeCorner, labels, templateExtent, geometryType)

if arcpy.Exists(outFeatureClass):
    print("Created Fishnet file successfully!")

# Spatial join the fishnet to the observed points
target_features = "Fishnet_bonefish_tarpon.shp"
join_features = "Step_1_Bonefish_Tarpons_Species_Output.shp"
out_feature_class = "HeatMap_Bonefish_Tarpons.shp"
join_operation = "JOIN_ONE_TO_ONE"
join_type = "KEEP_ALL"
field_mapping = ""
match_option = "INTERSECT"
search_radius = ""
distance_field_name = ""

arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                           join_operation, join_type, field_mapping, match_option,
                           search_radius, distance_field_name)

# 5. Check that the heatmap is created and delete the intermediate files (e.g. species shapefile and fishnet). Hint:
# arcpy.Delete_management()..

if arcpy.Exists(out_feature_class):
    print("Created Heatmap file successfully!")
    print("Deleting intermediate files")
    # arcpy.Delete_management(target_features)
    # arcpy.Delete_management(join_features)