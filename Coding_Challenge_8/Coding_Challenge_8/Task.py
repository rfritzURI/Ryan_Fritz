# Coding Challenge 8
# Our coding challenge this week follows from the last exercise that we did in class during
# Week 8 where we worked with functions.
# Convert some of your earlier code into a function. The only rules are:
# 1) You must do more than one thing to your input to the function, and
# 2) the function must take two arguments or more. You must also, 3) provide a zip file of example data within your repo.
# Plan the task to take an hour or two, so use one of the simpler examples from our past classes.


# I will turn my CC4 Intersect tool into a function
import arcpy, os

arcpy.env.overwriteOutput = True
directory = r"C:\RyanGIS\Class_8\Coding_Challenge_8"
arcpy.env.workspace = directory

# My directory is the argument for the function.
def Coding_Challenge_8(directory):
    roads = os.path.join(directory, "data", "roads_data", "RIDOT_Roads__2016_.shp")
    rivers = os.path.join(directory, "data", "rivers_data",
                          "Rivers_and_Streams__RI_Integrated_Water_Quality_Monitoring_and_Assessment_Report_2012.shp")
    in_features = [roads, rivers]
    out_feature_class = os.path.join(directory, "data", "roads_rivers_intercept.shp")
    join_attributes = "ALL"
    cluster_tolerance = ""
    output_type = "POINT"
    arcpy.Intersect_analysis(in_features, out_feature_class, join_attributes, cluster_tolerance, output_type)
    print('Hooray! We have intercepts!')
    return
Coding_Challenge_8(directory)