

import arcpy
import os
Target_Shapefile=r'C:\Users\npayne\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\Connection to DEFAULT@uggp.agrc.utah.gov.sde\UGGP.UGGPADMIN.UGS_NGWMN_Monitoring_Locations' #Target feature class that needs XY points updated
workspace=os.path.dirname(Target_Shapefile) #workspace path of SDE feature class
Input_Table = r'C:\Projects\MiscTest\update_xy\updated_sites.shp' #shapefile of points with updated locations 

#empty dictionary
loc_dict = {}
#iterate input table
with arcpy.da.SearchCursor(Input_Table, ['AltLocID', 'SHAPE@Y','SHAPE@X'])as Scurs:  #stores id key and location info in dictionary
    for row in Scurs:    #for iden, lat, lon in Scurs
        #update dictionary
        loc_dict[row[0]] = (row[1], row[2])
print loc_dict

edit = arcpy.da.Editor(workspace)
edit.startEditing(False, False) #Set as "False" when working with unversioned data
edit.startOperation
print Target_Shapefile
with arcpy.da.UpdateCursor(Target_Shapefile, ['AltLocationID', 'SHAPE@Y', 'SHAPE@X']) as Tcurs:
    for row in Tcurs:

        cur_Target_ID=row[0]
        if cur_Target_ID in loc_dict:
            row[1]=loc_dict[cur_Target_ID][0]  #index location row[1]=SHAPE@X and row[2]=SHAPE@Y
            row[2] = loc_dict[cur_Target_ID][1]
            print row

            Tcurs.updateRow(row)



edit.stopEditing(True)
