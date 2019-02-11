#Updates from coordinates of shapefile from existing shapefile, as long at ID match

import arcpy

Target_Shapefile=r'C:\Projects\MiscTest\update_xy\update_xy_copy2.shp' #shapefile of points whose coordnates need to be updated, must contain matching id key field
Input_Shapefile = r'C:\Projects\MiscTest\update_xy\updated_sites.shp'  #Input shapefile containing new coordinates and id key field


loc_dict = {} #empty dictionary
#iterate input table
with arcpy.da.SearchCursor(Input_Shapefile, ['AltLocID', 'SHAPE@Y','SHAPE@X'])as Scurs:
    for row in Scurs:
        loc_dict[row[0]] = (row[1], row[2]) #update dictionary
print loc_dict

#update cursor
with arcpy.da.UpdateCursor(Target_Shapefile, ['AltLocat_1', 'SHAPE@Y', 'SHAPE@X']) as Tcurs:
    for row in Tcurs:
        cur_Target_ID=row[0] #get value from dictionary if value is in dictionary
        if cur_Target_ID in loc_dict:
            row[1]=loc_dict[cur_Target_ID][0]  #index location row[2]=SHAPE@X and row[1]=SHAPE@Y that matches index locations in dictionary
            row[2] = loc_dict[cur_Target_ID][1]
            Tcurs.updateRow(row)
