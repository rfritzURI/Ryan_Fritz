# Coding Challenge 9
# In this coding challenge, your objective is to utilize the arcpy.da module to undertake some
# basic partitioning of your dataset. In this coding challenge, I want you to work with the
# Forest Health Works dataset from RI GIS (I have provided this as a downloadable ZIP file in this repository).
#
# Using the arcpy.da module (yes, there are other ways and better tools to do this),
# I want you to extract all sites that have a photo of the invasive species (Field: PHOTO) into a new Shapefile,
# and do some basic counts of the dataset. In summary, please addressing the following:
#
# Count how many individual records have photos, and how many do not (2 numbers), print the results.
#
# Count how many unique species there are in the dataset, print the result.
#
# Generate two shapefiles, one with photos and the other without


import arcpy
import os

arcpy.env.overwriteOutput = True
directory = r"C:\RyanGIS\Class_9\Coding_Challenge_9"
arcpy.env.workspace = directory
arcpy.AddMessage("The new current workspace is: %s" % arcpy.env.workspace)

# Count how many individual records have photos, and how many do not (2 numbers), print the results.
Forest_shp = os.path.join(directory, "Data", "RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp")

fields = ['FID', 'Species', 'photo']
print('The fields are: ')
print(fields)

expression = arcpy.AddFieldDelimiters(Forest_shp, "photo") + " = 'y'"

line_count_da = 0
with arcpy.da.SearchCursor(Forest_shp, fields, expression) as cursor:
    for row in cursor:
        line_count_da += 1
print(line_count_da)
print('Success!' + str(line_count_da) + ' records of photos have been determined')
#
expression = arcpy.AddFieldDelimiters(Forest_shp, "photo") + " <> 'y'"
line_count_da = 0
with arcpy.da.SearchCursor(Forest_shp, fields, expression) as cursor:
    for row in cursor:
        line_count_da += 1
print(line_count_da)
print('Success!' + str(line_count_da) + ' records that do not have photos have been determined')


# Count how many unique species there are in the dataset, print the result.
fields = ['Species']

species_list = []
with arcpy.da.SearchCursor(Forest_shp, fields) as cursor:
    for row in cursor:
        if row[0] not in species_list:
            species_list.append(row[0])
print(len(species_list))
print('Success!' + str(len(species_list)) + ' records of unique species have been determined')


# Generate two shapefiles, one with photos and the other without

# To create the two shapefiles, I'll use the Copy Features tool
# WHAT TOOL DOES: Copies features from the input feature class or layer to a new feature class.
# More information on the tool can be found here --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/data-management/copy-features.htm

# However, first I can use the Select by Attribute tool to select the records with photos and without
# WHAT TOOL DOES: Adds, updates, or removes a selection based on an attribute query.
# More information on the tool can be found here --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/data-management/select-layer-by-attribute.htm

# Creating the shapefile with photos

expression = arcpy.AddFieldDelimiters(Forest_shp, "photo") + " = 'y'"

select = arcpy.SelectLayerByAttribute_management(Forest_shp, "NEW_SELECTION", expression)

out_feature_class = 'records_with_photos.shp'

arcpy.CopyFeatures_management(select, out_feature_class)
print("The shapefile with photos has been created")
# # Creating the shapefile without photos

expression = arcpy.AddFieldDelimiters(Forest_shp, "photo") + " <> 'y'"

select = arcpy.SelectLayerByAttribute_management(Forest_shp, "NEW_SELECTION", expression)

out_feature_class = 'records_without_photos.shp'

arcpy.CopyFeatures_management(select, out_feature_class)
print("The shapefile without photos has been created")
