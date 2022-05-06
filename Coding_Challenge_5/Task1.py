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

import arcpy, os, csv
# Setting my workspace where my files will be stored
arcpy.env.overwriteOutput = True
ryan_directory = r"C:\Ryan_GIS\Class_5\Coding_Challenge_5"
arcpy.env.workspace = ryan_directory

if not os.path.exists(os.path.join(ryan_directory, "output_files")):
    os.mkdir(os.path.join(ryan_directory, "output_files"))
if not os.path.exists(os.path.join(ryan_directory, "temp_files")):
    os.mkdir(os.path.join(ryan_directory, "temp_files"))

# Splitting the csv file to separate thespecies
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


