# Coding Challenge 10
# Our coding challenge this week follows from the last exercise that we did in class during
# Week 6 and improve our practice with rasters from Week 10.
#
# Task 1 - Use what you have learned to process the Landsat files provided, this time, you
# know you are interested in the NVDI index which will use Bands 4 (red, aka vis) and 5 (near-infrared, aka nir)
# from the Landsat 8 imagery, see here for more info about the bands: https://www.usgs.gov/faqs/what-are-band-designations-landsat-satellites. Data provided are monthly (a couple are missing due to cloud coverage) during the year 2015 for the State of RI, and stored in the file Landsat_data_lfs.zip.
#
# Before you start, here is a suggested workflow:
#
# Extract the Landsat_data_lfs.zip file into a known location.
# For each month provided, you want to calculate the NVDI,
# using the equation: nvdi = (nir - vis) / (nir + vis)
# https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index.
# using the Raster Calculator Tool in ArcMap and using "Copy as Python Snippet" for the first calculation.
# The only rule is, you should run your script once, and generate the NVDI for ALL MONTHS provided.
# As part of your code submission, you should also provide a visualization document
# (e.g. an ArcMap layout in PDF format), showing the patterns for an area of RI that you find interesting.

import arcpy, os
directory = r"C:\Ryan_GIS\Class_10\Coding_Challenge_10\Data"
arcpy.env.workspace = os.path.join(directory)
arcpy.env.overwriteOutput = True

# Listing the landsat data folders containing the raster files
directory_contents = os.listdir(directory)
print("The landsat files are contained in the following subfolders: ")
print(directory_contents)

# Now that the subfolders have been identified as a variable, I can use a loop to extract
# Bands 4 and 5 within the subfolders and connecting the subfolders to the directory

for landsat_folder in directory_contents:
    arcpy.env.workspace = os.path.join(directory, landsat_folder)

    raster_list_B4 = arcpy.ListRasters("*B4.tif")
    raster_list_B5 = arcpy.ListRasters("*B5.tif")
    print('The Band 4 raster file is:' + str(raster_list_B4))
    print('The Band 5 raster file is:' + str(raster_list_B5))

    # To calculate NVDI index, we can use the equation nvdi = (nir - vis) / (nir + vis) and setting
    # the B4 and B5 rasters as variables
    band_4 = arcpy.Raster(raster_list_B4)
    band_5 = arcpy.Raster(raster_list_B5)
    vis = band_4
    nir = band_5
    # The Raster Calculator tool will run equation nvdi = (nir - vis) / (nir + vis)
    # WHAT TOOL DOES: Builds and executes a single Map Algebra expression using Python syntax.
    # Helpful link on how to perform a raster calculation using arcpy --> https://support.esri.com/en/technical-article/000022418
    print("Running raster calculation...")
    nvdi = (nir - vis) / (nir + vis)
    print('The raster calculation ran successfully. nvdi is : '+ str(nvdi))

    # I'll rename the nvdi file to tif format


    # To save nvdi to Output_rasters folder, I'll use:  outraster.save(r"<location_path>\<name>.gdb" + "\\" + filename)
    raster_output_directory = os.path.join(directory, "Output_rasters")
    if not os.path.exists(raster_output_directory):
        os.mkdir(raster_output_directory)



    nvdi.save(os.path.join(raster_output_directory, str(raster_output_directory) + '_nvdi.tif'))
    print('nvdi.tif file saved sucessfully')
print('Coding Challenge 10 complete!')
