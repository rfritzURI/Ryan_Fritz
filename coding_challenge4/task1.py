# For this coding challenge, I want you to find a particular tool that you like in arcpy.
# It could be a tool that you have used in GIS before or something new. Try browsing the full tool list to get
# some insight here (click Tool Reference on the menu list to the left).
#
# Set up the tool to run in Python, add some useful comments, and importantly, provide
# some example data in your repository (try to make it open source, such as Open Streetmap, or RI GIS.
# You can add it as a zip file to your repository.
#
# My only requirements are:
#
# Comment your code well.
# Ensure that the code will run on my machine with only a single change to a
# single variable (i.e. a base folder location)


# The Intercept tool
# More information on the Intercept tool is found here: https://desktop.arcgis.com/en/arcmap/10.3/tools/analysis-toolbox/intersect.htm

# Summary of Intercept tool:
# Computes a geometric intersection of the input features. Features or portions of features
# which overlap in all layers and/or feature classes will be written to the output feature class.

# The syntax: Intersect_analysis (in_features, out_feature_class, {join_attributes}, {cluster_tolerance}, {output_type})
# Using raods and rivers feature class data from RIGIS, I used the intercept tool to

# import arcypy gives you access to nearly all ArcGIS functions
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\RyanGIS\Class_4\coding_challenge4"
arcpy.AddMessage("The new current workspace is: %s" % arcpy.env.workspace)

roads = r"C:\RyanGIS\Class_4\coding_challenge4\data\roads_data\RIDOT_Roads__2016_.shp"
rivers = r"C:\RyanGIS\Class_4\coding_challenge4\data\rivers_data\Rivers_and_Streams__RI_Integrated_Water_Quality_Monitoring_and_Assessment_Report_2012.shp"
in_features = ["roads", "rivers"]
out_feature_class = r"C:\RyanGIS\Class_4\coding_challenge4\data\roads_rivers_intercept"
join_attributes = "ALL"
cluster_tolerance = 1.5
output_type = "POINT"
arcpy.Intersect_analysis(in_features, out_feature_class, {join_attributes}, {cluster_tolerance}, {output_type})
