# Coding Challenge 7
# Our coding challenge this week should make use of temporary folders, output folders and file management.
#
# Convert your Coding Challenge 5 exercise to work with temporary folders, os.path.join and glob.glob.
# Do not take too much time on this and if you do not have a working Challenge 5, talk to the instructor.

import arcpy, os, csv, glob
# Setting my workspace where my files will be stored
arcpy.env.overwriteOutput = True
ryan_directory = r"C:\Ryan_GIS\Class_7\Coding_Challenge_7"
arcpy.env.workspace = ryan_directory
# List all Python files in current directory
print(glob.glob("*.py"))

if not os.path.exists(os.path.join(ryan_directory, "output_files")):
    os.mkdir(os.path.join(ryan_directory, "output_files"))
if not os.path.exists(os.path.join(ryan_directory, "temp_files")):
    os.mkdir(os.path.join(ryan_directory, "temp_files"))

# Splitting the csv file to separate the species
with open('Fish_Species_updated.csv') as species_csv:
    csv_reader = csv.reader(species_csv, delimiter=',')
    species_list = []
    header = next(csv_reader)
    for row in csv_reader:

        if row[0] not in species_list:
            species_list.append(row[0])
    print(species_list)

for species in species_list:
    print(species)
    csv_file_species = os.path.join(ryan_directory,"temp_files", species.replace(" ", "_") + ".csv")
    file = open(csv_file_species, "w")
    # Extract that species from the cvs file
    with open('Fish_Species_updated.csv') as species_csv:
        csv_reader = csv.reader(species_csv, delimiter=',')
        species_list = []
        header = next(csv_reader)
        file.write(", ".join(header))
        file.write("\n")
        for row in csv_reader:
            if row[0] == species:
                file.write(", ".join(row))
                file.write("\n")
        file.close()

    # Converting the csv file into a shapefile before generating the heatmap
    shp_file_species = os.path.join(ryan_directory, "temp_files", species.replace(" ", "_") + ".shp")

    in_Table = "Fish_Species_updated.csv"
    x_coords = "longitude"
    y_coords = "latitude"
    z_coords = ""
    out_Layer = "fish"

    # Set the spatial reference
    spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
    arcpy.CopyFeatures_management(lyr, shp_file_species)

    #Creating the fishnet
    shp_fishnet_file_species = os.path.join(ryan_directory, "temp_files", species.replace(" ", "_") + "_fishnet.shp")
    # But first, we must extract the Extent
    desc = arcpy.Describe(shp_file_species)
    XMin = desc.extent.XMin
    XMax = desc.extent.XMax
    YMin = desc.extent.YMin
    YMax = desc.extent.YMax

    # Generate fishnet
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

    print("Cool, we made a Fishnet shapefile")
    # Set the origin of the fishnet
    originCoordinate = str(XMin) + " " + str(YMin)
    yAxisCoordinate = str(XMin) + " " + str(YMin + 1)
    cellSizeHeight = "1"
    cellSizeWidth = "1"
    numRows = ""
    numColumns = ""
    oppositeCorner = str(XMax) + " " + str(YMax)
    labels = "NO_LABELS"
    templateExtent = "#"
    geometryType = "POLYGON"

    arcpy.CreateFishnet_management(shp_fishnet_file_species, originCoordinate, yAxisCoordinate,
                                   cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                   oppositeCorner, labels, templateExtent, geometryType)
    print("Fishnet origin created successfully")
    if arcpy.Exists(shp_fishnet_file_species):
        print("Created Fishnet file successfully!")

    # Spatial join the fishnet to the observed points
    shp_heatmap_file_species = os.path.join(ryan_directory, "temp_files",
                                                species.replace(" ", "_") + "_heatmap.shp")
    target_features = shp_fishnet_file_species
    join_features = shp_file_species
    out_feature_class = shp_heatmap_file_species
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_ALL"
    field_mapping = ""
    match_option = "INTERSECT"
    search_radius = ""
    distance_field_name = ""

    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                               join_operation, join_type, field_mapping, match_option,
                               search_radius, distance_field_name)

    if arcpy.Exists(shp_heatmap_file_species):
        print("Created Heatmap file successfully!")


