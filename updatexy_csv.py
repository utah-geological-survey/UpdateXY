#Takes coordinates from CSV and updates matching records in shapefile, as long as ID fields match
import arcpy
Target_Shapefile=r'C:\Projects\MiscTest\update_xy\update_xy_copy1.shp'
Input_Table = r'C:\Projects\MiscTest\update_xy\SV_GPS2.csv'

#empty dictionary
loc_dict = {}
#iterate input table
with arcpy.da.SearchCursor(Input_Table, ['AltID', 'Northing','Easting'])as Scurs:
    for row in Scurs:    #for iden, lat, lon in Scurs
        #update dictionary
        loc_dict[row[0]] = (row[1], row[2])
print loc_dict

#update
with arcpy.da.UpdateCursor(Target_Shapefile, ['AltLocat_1', 'SHAPE@Y', 'SHAPE@X']) as Tcurs:
    for row in Tcurs:
        print Tcurs
        #get value from dictionary if value is in dictionary
        cur_Target_ID=row[0]
        if cur_Target_ID in loc_dict:
            row[1]=loc_dict[cur_Target_ID][0]  #index location row[1]=SHAPE@X and row[2]=SHAPE@Y
            row[2] = loc_dict[cur_Target_ID][1]
            print row

            Tcurs.updateRow(row)
