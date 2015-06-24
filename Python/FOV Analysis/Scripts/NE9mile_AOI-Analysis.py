
"""============  FOR AMERICA-VIEW/PHENOCAM INTERNAL USE ONLY!  =============="""
#===============================================================================
#===============================================================================

    # Name:          NE9mile_AOI-Analysis

    # Version:       Beta

    # Purpose:       Produce polygon areas of visible land surfaces via.
    #                optical/installation field camera specs. and
    #                USGS provided LIDAR data.

    # Locality:      Site specific system implementation for:
    #                                9-mile Prarie, Nebraska

    # Orginization:  USGS / NAGT Office
    #                North Central Climate Science Center
    #                Colorado State University

    # Copyright:     (c) June-6th-2015
    #                Joseph M. Krienert
    #                jkrienert@siu.edu


#===============================================================================

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    For a copy of the GNU General Public License, please refer to:
#                                    <http://www.gnu.org/licenses/>

#===============================================================================
#===============================================================================

# Import arcpy processing directory
import arcpy

# Main -area of interest(AOI)- processing function
def AOIanalysis():
    # Establish fundamental extent
    arcpy.CheckOutExtension("spatial")
    # Rerunning script auto-overwrites output AOI shapefile
    arcpy.env.overwriteOutput = True
    # Maintains processing chain outputs in memory ONLY
    arcpy.env.addOutputsToMap = False

    """===========vvv FUNDAMENTAL PARAMETERS BELOW vvv==========="""

    # Locations of workspace, data-soucres, and data-outputs
    arcpy.env.workspace = "C:\\...\\your-project.mxd"
    DEM_raster_layer = "C:\\...\\your-directory\\...\\NE-LIDARxDEM-Clip.tif"
    Camera_point_layer = "C:\\...\\your-directory\\...\\NE-PHENOCAM.shp"
    AOI_output = "C:\\...\\your-directoy\\...\\your-output-filename.shp"

    # Primary varriable : cleanup of polygon borders
    Smoothing_Tolerance = "1 Meters"

    """===========^^^ FUNDAMENTAL PARAMETERS ABOVE ^^^============"""

    # Chain processing of the point sources FOV-footprint dataset
    roughAOI = estabFOVfootprint(DEM_raster_layer,Camera_point_layer,Smoothing_Tolerance)

    # Sort roughAOI output based on proximity to camera (with respect to North centered azimuth)
    sortToCameraRange(roughAOI,AOI_output)

    # Add relative polygon areas to attribute table
    addAreas(AOI_output)

    # Cleanup unecessary fields from AOI_output
    cleanupFields(AOI_output)

# AOI footprint processing function with annomolous geometry cleanup
def estabFOVfootprint(DEM_raster_layer,Camera_point_layer,Smoothing_Tolerance):
    # Spatial Analyst Tools > Surface > Visibility
    arcpy.gp.Visibility_sa(DEM_raster_layer,Camera_point_layer,"in_memory\\rawVisRast",\
                           "","FREQUENCY","NODATA","0.00001201","FLAT_EARTH","0.13","","",\
                           "OFFSETA","","","AZIMUTH1","AZIMUTH2","VERT1","VERT2")

    # Spatial Analyst Tools > Generalization > Boundary Clean
    arcpy.gp.BoundaryClean_sa("in_memory\\rawVisRast","in_memory\\clnVisRast","ASCEND","TWO_WAY")
    arcpy.Delete_management("in_memory\\rawVisRast")

    # Conversion Tools > From Raster > Raster to Polygon
    arcpy.RasterToPolygon_conversion("in_memory\\clnVisRast","in_memory\\visPoly","NO_SIMPLIFY","")
    arcpy.Delete_management("in_memory\\clnVisRast")

    # Cartographic Tools > Generalization > Smooth Polygon
    arcpy.SmoothPolygon_cartography("in_memory\\visPoly","in_memory\\smthVisPoly","PAEK",\
                                     Smoothing_Tolerance,"NO_FIXED","NO_CHECK")
    arcpy.Delete_management("in_memory\\visPoly")

    # Analysis Tools > Overlay > Union
    arcpy.Union_analysis("in_memory\\smthVisPoly","in_memory\\uniVisPoly","ALL","","NO_GAPS")
    arcpy.Delete_management("in_memory\\smthVisPoly")

    # Data Management Tools > Generalization > Dissolve
    footprintFOVout = "in_memory\\whlVisPoly"
    arcpy.Dissolve_management("in_memory\\uniVisPoly",footprintFOVout,"","",\
                              "SINGLE_PART","DISSOLVE_LINES")
    arcpy.Delete_management("in_memory\\uniVisPoly")
    return footprintFOVout

# Designate AOI footprint index based on proximity to North-Azimuth Phenocam
def sortToCameraRange(roughAOI,AOI_output):
    # establish new sorting, numbering, and area fields
    arcpy.AddField_management(roughAOI, "YMin", "DOUBLE", "20","12")
    arcpy.AddField_management(roughAOI, "AOI", "SHORT")
    arcpy.AddField_management(roughAOI,"SqrMeters","Double")

    # compile list of minimum Y bounds of each polygon (proximal to PHENOCAM-North)
    yMinExtents = []
    readFeatures = arcpy.SearchCursor(roughAOI)
    changeFeatures = arcpy.UpdateCursor(roughAOI)
    featureNames = arcpy.Describe(roughAOI).shapeFieldName
    for readFeat in readFeatures:
        yMinExtents.append(readFeat.getValue('Shape').extent.YMin)

    # apply respective minimum Y bounds to each features new attribute field
    for idx, changeFeat in enumerate(changeFeatures):
        changeFeat.setValue("yMin",yMinExtents[idx])
        changeFeatures.updateRow(changeFeat)

    # resort the attribute table based on the newly filled YMin attribute field
    arcpy.env.addOutputsToMap = True
    arcpy.Sort_management(roughAOI, AOI_output, [["YMin","ASCENDING"]], "")
    arcpy.Delete_management(roughAOI)

    # create top-down AOI numerical index (thnx to YMin-sort), and update AOI field
    changeFeatures = arcpy.UpdateCursor(AOI_output)
    for idx, changeFeat in enumerate(changeFeatures):
        aoiIdx = idx+1
        changeFeat.setValue("AOI",aoiIdx)
        changeFeatures.updateRow(changeFeat)

# Calculate respective AOI polygonal areas
def addAreas(AOI_output):
    # publish respective polygonal map areas to attribute table via calculated expression
    areaExpress = "{0}".format("!SHAPE.area@SQUAREMETERS!")
    arcpy.CalculateField_management(AOI_output, "SqrMeters", areaExpress, "PYTHON")

# Remove erronious fields from AOI attribute table generated durning processing
def cleanupFields(AOI_output):
    # cleanup and garbage any extrenuous fields generated through the analysis process
    keepFields = ["FID","OBJECTID","Shape","AOI","SqrMeters"]
    aoiFields = arcpy.ListFields(AOI_output)
    for field in aoiFields:
        if field.name in keepFields: continue
        else: arcpy.DeleteField_management(AOI_output,field.name)

if __name__ == '__main__':
    AOIanalysis()



