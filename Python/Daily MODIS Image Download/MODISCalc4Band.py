import arcpy

rx = (sys.argv[1])
ry = (sys.argv[2])
rz = (sys.argv[3])

inras = rx+";"+ry+"/Band_1"

arcpy.CompositeBands_management(inras,rz)