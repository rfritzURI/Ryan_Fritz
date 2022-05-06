#                     Python Toolbox for Hydrological Analysis: Pond and Lake Mapping
#                                         Script by Ryan Fritz

# WHAT IS A PYTHON TOOLBOX:
# Python toolboxes are geoprocessing toolboxes that are created entirely in Python and
# are an extremely useful means of sharing geoprocessing tools. While a python file has a .py extension, a
# Python toolbox is a Python file with a .pyt extension that defines a toolbox and its tools. There are two ways to
# create a toolbox in ArcGIS. The first way is directly within the catalog of ArcGIS and the other is through python
# script. This script will generate a toolbox using python script.

# PURPOSE OF THIS SCRIPT:
# Hydrological analyses include identifying water resource areas, analyzing the flow of water over a landscape,
# mapping the area of a watershed, and assessing flood risks. Specifically, this script will use
# four tools to enable anyone in the field of hydrology to map real ponds and lake using an input DEM
# (Digital Elevation Model). A DEM is a raster type where each cell value represents elevation within the cell. Using a
# DEM, one can locate the areas of depressions (sinks) in the ground that retain water a.k.a ponds and lakes!

#                                       TOOLS IN THE TOOLBOX

# The Sink Tool
# PURPOSE: The Sink tool is used to identify real and artificial sinks in the DEM raster. Artificial sinks are not real
# water bodies and are caused from random errors in the DEM.
# WHAT THIS TOOL DOES: Creates a raster identifying all sinks or areas of internal drainage.
# More information on the Sink tool --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/spatial-analyst/sink.htm

# The Region Group Tool
# PURPOSE: Real water bodies are made up of many pixels but artificial sinks are made up of one or two pixels.
# The Region Group tool will filter out artificial sinks by their size. Sinks will become a pixel group with a Object ID
# and count field indicating how many pixels are in the group.
# WHAT THIS TOOL DOES: For each cell in the output, the identity of the connected region to which
# that cell belongs is recorded. A unique number is assigned to each region.
# More information on the Region Group tool --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/spatial-analyst/region-group.htm

# The Set Null Tool
# PURPOSE: To extract real sinks from the DEM. Artificial sinks will be set to a null value and real sinks set to a
# value of one.
# WHAT THIS TOOL DOES: Set Null sets identified cell locations to NoData based on a specified
# criteria. It returns NoData if a conditional evaluation is true, and returns the value specified by
# another raster if it is false.
# More information on the Set Null tool --> https://pro.arcgis.com/en/pro-app/2.8/tool-reference/spatial-analyst/set-null.htm

import arcpy

# The class acts like a folder in code. This section (lines 34-42) will build the toolbox. This section of code is the
# same as right-clicking in ArcGIS Pro and selecting "New Toolbox."

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Pond and Lake Mapping"
        self.alias = ""

        # This is the names of the scrips tools inside the toolbox. List of tool classes associated with this toolbox
        self.tools = [FlowDirection, Sink, RegionGroup, SetNull]


class FlowDirection(object):

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        # Self label will dislay the name of the tool in the geoprocessing toolbox window
        self.label = "Flow Direction Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_DEM = arcpy.Parameter(name="input_DEM",
                                     displayName="Input DEM",
                                     datatype="DERasterDataset",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # input_DEM.value = r"C:\Ryan_GIS\Final_Toolbox\Hydro_Data\dem_RISP.img"  # This is a default value that can be over-ridden in the toolbox
        params.append(input_DEM)
        output_flow = arcpy.Parameter(name="output",
                                 displayName="Output",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        # output_flow.value = r"C:\Ryan_GIS\Final_Toolbox\Flow_Direction_raster.tif"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_flow)
        return params


    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        input_DEM = parameters[0].valueAsText
        output_flow = parameters[1].valueAsText
        outFlowDirection = arcpy.sa.FlowDirection(in_surface_raster=input_DEM,
                               force_flow="NORMAL",
                               out_drop_raster="",
                               flow_direction_type="D8")
        outFlowDirection.save(output_flow)
        arcpy.AddMessage("Flow Direction tool has run")
        return

class Sink(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Sink Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_FlowDirection_raster = arcpy.Parameter(name="input_FlowDirection_raster",
                                     displayName="Input Flow raster",
                                     datatype="DERasterDataset",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # input_FlowDirection_raster.value = r"C:\Ryan_GIS\Final_Toolbox\Flow_Direction_raster.tif"  # This is a default value that can be over-ridden in the toolbox
        params.append(input_FlowDirection_raster)

        output_Sink_raster = arcpy.Parameter(name="output_Sink_raster",
                                 displayName="Output",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        # output_Sink_raster.value = r"C:\Ryan_GIS\Final_Toolbox\Sink_raster.tif"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_Sink_raster)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_FlowDirection_raster = parameters[0].valueAsText
        output_Sink_raster = parameters[1].valueAsText

        outSink = arcpy.sa.Sink(in_flow_direction_raster=input_FlowDirection_raster)
        outSink.save(output_Sink_raster)
        arcpy.AddMessage("Sink tool has run")

        return

class RegionGroup(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Region Group Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_Sink_raster = arcpy.Parameter(name="input_Sink_raster",
                                     displayName="Input Line",
                                     datatype="DERasterDataset",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # input_Sink_raster.value = r"C:\Ryan_GIS\Final_Toolbox\Sink_raster.tif"  # This is a default value that can be over-ridden in the toolbox
        params.append(input_Sink_raster)

        output_RG_raster = arcpy.Parameter(name="output",
                                 displayName="Output",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        # output_RG_raster.value = r"C:\Ryan_GIS\Final_Toolbox\RegionGroup_raster.tif"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_RG_raster)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_Sink_raster = parameters[0].valueAsText
        output_RG_raster = parameters[1].valueAsText

        outRegionGrp = arcpy.sa.RegionGroup(in_raster=input_Sink_raster,
                             number_neighbors="EIGHT",
                             zone_connectivity="WITHIN",
                             add_link="ADD_LINK",
                             excluded_value=None)
        outRegionGrp.save(output_RG_raster)
        arcpy.AddMessage("Region Group tool has run")

        return

class SetNull(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Set Null Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_conditional_raster = arcpy.Parameter(name="input_conditional_raster",
                                     displayName="Input Line",
                                     datatype="DERasterDataset",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # input_conditional_raster.value = r"C:\Ryan_GIS\Final_Toolbox\RegionGroup_raster.tif"  # This is a default value that can be over-ridden in the toolbox
        params.append(input_conditional_raster)

        output_depression_raster = arcpy.Parameter(name="output_depression_raster",
                                 displayName="Output",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        # output_depression_raster.value = r"C:\Ryan_GIS\Final_Toolbox\depression_raster.tif"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_depression_raster)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_conditional_raster = parameters[0].valueAsText
        output_depression_raster = parameters[1].valueAsText

        outSetNull = arcpy.ia.SetNull(in_conditional_raster=input_conditional_raster,
                         in_false_raster_or_constant=1,
                         where_clause="COUNT < 100")
        outSetNull.save(output_depression_raster)

        arcpy.AddMessage("Set Null tool has run")
        return

# This code block allows you to run your code in a test-mode within PyCharm, i.e. you do not have to open the tool in
# ArcMap. This works best for a "single tool" within the Toolbox.
# def main():
#     tool = SetNull()
#     tool.execute(tool.getParameterInfo(), None)
#
# if __name__ == '__main__':
#     main()