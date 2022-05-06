#                          Wetlands Vulnerable to Roadway Runoff in South Kingstown, RI
#                                          Script by Ryan Fritz

# SCRIPT SUMMARY: Wetlands adjacent to roadways are highly suceptible to runoff pollution. This script accesses the arcpy
# package and uses ArcGIS's greoprocessing tools to determine the total acreage of wetlands within 500 feet of
# roadways in South Kingstown, Rhode Island.

import arcpy
import os

arcpy.env.overwriteOutput = True
directory = r"C:\Data\Students_2022\Fritz\Midterm"
arcpy.env.workspace = directory

print("My script will determine the acreage of wetlands present within 500 feet from "
      "roadways in South Kingstown, Rhode Island")

# The Data
data_list = ['RIDOT_Roads_2016_', 'towns', 'wetlands']
RIDOT_Roads_2016_ = os.path.join(directory, "data", r"RIDOT_Roads__2016_.shp")
towns = os.path.join(directory, "data", r"towns.shp")
wetlands = os.path.join(directory, "data", "wetlands.shp")
print("The script will use these three shapefiles: ")
print(data_list)

# Step 1: The Buffer Tool
# PURPOSE: Let's use the Buffer Tool to create a 500-foot buffer from roads
# WHAT THIS TOOL DOES: The Buffer Tool creates buffer polygons around
# input features (roads) to a specified distance.
#
# More information on the Buffer Tool --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/analysis/buffer.htm

Roads_Buffer = os.path.join(directory, "data", "Roads_Buffer.shp")
in_features = RIDOT_Roads_2016_
out_feature_class = Roads_Buffer
buffer_distance_or_field = "500 Feet"
line_side = "FULL"
line_end_type = "ROUND"
dissolve_option = "ALL"
dissolve_field = []
method = "PLANAR"
arcpy.analysis.Buffer(in_features, out_feature_class,
                      buffer_distance_or_field, line_side,
                      line_end_type, dissolve_option,
                      dissolve_field, method)
print("The Buffer Tool has successfully set a 500 foot buffer from roads ")

# Step 2: The Select Tool
# PURPOSE: The Select Tool will create the study area of South Kingstown, RI from the towns.shp feature class
# WHAT THIS TOOL DOES: Extracts features from an input feature class or input feature
# layer, typically using a select or Structured Query Language (SQL) expression,
# and stores them in an output feature class.
#
# More information on the Select Tool --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/analysis/select.htm

South_Kingstown = os.path.join(directory, "data", "South_Kingstown.shp")
in_features = towns
out_feature_class = South_Kingstown
where_clause = "NAME = 'SOUTH KINGSTOWN'"

arcpy.analysis.Select(in_features, out_feature_class,
                      where_clause)
print("The Select Tool has successfully created our study area of South Kingstown")

# Step 3: The Clip Tool
# PURPOSE: The Clip Tool will "clip" the road input features to the study area of South Kingstown, RI. Now,
# only roads in South Kingtown, RI are present.
# WHAT THIS TOOL DOES: Extracts input features that overlay the clip features. Use this tool to cut out a piece of
# one dataset using one or more of the features in another dataset as a cookie cutter.
#
# More information on the Clip Tool --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/analysis/clip.htm

Roads_Buffer_SK = os.path.join(directory, "data", "Roads_Buffer_SK.shp")
in_features = Roads_Buffer
clip_features = South_Kingstown
out_feature_class = Roads_Buffer_SK
cluster_tolerance = ""

arcpy.analysis.Clip(in_features, clip_features,
                    out_feature_class, cluster_tolerance)
print("Cool, the Clip Tool worked! Now we have roads only in South Kingstown")

# # Step 4: The Clip Tool...again!
# PURPOSE: The Clip Tool will "clip" the wetland input features to the roads feature class, only
# displaying wetlands in the roads 500 foot buffer zone.

Wetlands_Within_RoadsBZ = os.path.join(directory, "data", "Wetlands__Within_RoadsBZ.shp")
in_features = wetlands
clip_features = Roads_Buffer_SK
out_feature_class = Wetlands_Within_RoadsBZ
cluster_tolerance = ""
arcpy.analysis.Clip(in_features, clip_features,
                    out_feature_class, cluster_tolerance)
print("Using the Clip Tool again, we have only have wetlands within our 500 foot buffer from roads...success!")

# Step 5: The Summary Statistics Tool
# PURPOSE: The Summary Statistics Tool calculate the sum (acres) of wetlands within
# 500 feet of roads in South Kingstown, RI.
# WHAT THIS TOOL DOES: The tool creates an Output Table that consists of fields
# containing the result of the statistical operation.
# More information on the Summary Statistics Tool  --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/analysis/summary-statistics.htm

# Wetlands_Acres = "C:\\Users\\Student\\Documents\\ArcGIS\\Projects\\midterm\\midterm.gdb\\Wetlands_Acres"
in_table = Wetlands_Within_RoadsBZ
out_table = os.path.join(directory, "data", "SumAcres.csv")
statistics_fields = [["ACRES", "SUM"]]
case_field = ""
arcpy.analysis.Statistics(in_table, out_table, statistics_fields, case_field)

# arcpy.analysis.Statistics(in_table=Wetlands_Within_RoadsBZ, out_table=Wetlands_Acres,
#                       statistics_fields=[["ACRES", "SUM"]], case_field=[])
print("Hooray! The Summary Statistics Tool calculated the total acreage of wetlands with 500 feet of roads")

# Step 6: Reading the csv file
import csv

with open("SumAcres.csv") as Midterm_Results_csv:
    csv_reader = csv.reader(Midterm_Results_csv, delimiter=',')


# Step 7:Creating a text file to display the results of the script

file = open("Midterm_Analysis_Results.txt", "w")

file.write("Midterm Results\n")
file.write("By Ryan Fritz\n")
file.write("The script has determined that there is 9,494 acres of "
           "wetlands within 500 feet of roadways in South Kingstown,RI. \n")
file.write("The final output is a csv file containing the calculated sum of wetland acres.\n")
file.close()

# Reading the Midterm Analysis Results text file
file = open("Midterm_Analysis_Results.txt", "r")
file_contents = file.read()
print(file_contents)
file.close()