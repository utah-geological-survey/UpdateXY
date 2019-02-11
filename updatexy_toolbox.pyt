from pylab import rcParams
import os

import arcpy

arcpy.env.overwriteOutput = True

### UPDATE SHAPEFILE ###

class CursorCopy(object):

    def __init__(self):
        self.infile = None
        self.inid = 'AltLocID'
        self.outfile = None
        self.outid = 'AltLocat_1'
        self.xfield = None
        self.yfield = None
        self.xoutfield = 'X'
        self.youtfield = 'Y'

    def copywcursor(self):

        inftype = arcpy.Describe(self.infile).dataType
        outftype = arcpy.Describe(self.outfile).dataType

        if inftype == 'TextFile':
            inlist = [self.inid, self.xfield, self.yfield]
        elif inftype == 'ShapeFile':
            inlist = [self.inid, 'SHAPE@Y', 'SHAPE@X']
        elif inftype == 'FeatureClass':
            inlist = [self.inid, 'SHAPE@Y', 'SHAPE@X']
            workspace = arcpy.Describe(self.infile).path
            edit = arcpy.da.Editor(workspace)
            edit.startEditing(False, False)  # Set as "False" when working with unversioned data
            edit.startOperation
        else:
            arcpy.AddMessage('Input Filetype Not Recognized')

        if outftype == 'TextFile':
            outlist = [self.outid, self.xoutfield, self.youtfield]
        elif outftype == 'ShapeFile' or inftype == 'FeatureClass':
            outlist = [self.outid, 'SHAPE@Y', 'SHAPE@X']
        elif outftype == 'FeatureClass':
            outlist = [self.inid, 'SHAPE@Y', 'SHAPE@X']
            workspace = arcpy.Describe(self.outfile).path
            edit = arcpy.da.Editor(workspace)
            edit.startEditing(False, False)  # Set as "False" when working with unversioned data
            edit.startOperation
        else:
            arcpy.AddMessage('Output Filetype Not Recognized')


        loc_dict = {}
        with arcpy.da.SearchCursor(self.infile, inlist)as Scurs:
            for row in Scurs:
                loc_dict[row[0]] = (row[1], row[2])  # update dictionary
        print(loc_dict)

        # update cursor
        with arcpy.da.UpdateCursor(self.outfile, outlist) as Tcurs:
            for row in Tcurs:
                cur_Target_ID = row[0]  # get value from dictionary if value is in dictionary
                if cur_Target_ID in loc_dict:
                    row[1] = loc_dict[cur_Target_ID][0]
                    # index location row[1]=SHAPE@X and row[2]=SHAPE@Y that matches index locations in dictionary
                    row[2] = loc_dict[cur_Target_ID][1]
                    Tcurs.updateRow(row)


# ---------------ArcGIS Python Toolbox Classes and Functions-------------------------------------------------------------

def parameter(displayName, name, datatype, parameterType='Required', direction='Input', defaultValue=None):
    """The parameter implementation makes it a little difficult to quickly create parameters with defaults. This method
    prepopulates some of these values to make life easier while also allowing setting a default value."""
    # create parameter with a few default properties
    param = arcpy.Parameter(
        displayName=displayName,
        name=name,
        datatype=datatype,
        parameterType=parameterType,
        direction=direction)

    # set new parameter to a default value
    param.value = defaultValue

    # return complete parameter object
    return param


class Toolbox(object):
    def __init__(self):
        self.label = "updateXY"
        self.alias = "Update XY"

        # List of tool classes associated with this toolbox
        self.tools = [UpdateShapefile]


class UpdateShapefile(object):
    def __init__(self):
        self.label = "Update Shapefile"
        self.description = """Update a Shapefile geometry based on values from a cs"""
        self.canRunInBackground = False
        self.parameters = [
            parameter("Input File", "infile", "DEFile"),
            parameter("Input ID", "inid", "Field"),
            parameter("Output File", "well_file", "DEFile"),
            parameter("Input ID", "inid", "Field"),
            parameter("X Field", "xfield", "GPString", parameterType="Optional", defaultValue=None),
            parameter("Y Field", "yfield", "GPString", parameterType="Optional", defaultValue=None),
            parameter("X Out Field", "xoutfield", "GPString", parameterType="Optional", defaultValue='X'),
            parameter("Y Out Field", "youtfield", "GPString", parameterType="Optional", defaultValue='Y'),
        ]

    def getParameterInfo(self):
        """Define parameter definitions; http://joelmccune.com/lessons-learned-and-ideas-for-python-toolbox-coding/"""
        return self.parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter"""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        ccopy = CursorCopy()
        ccopy.infile = parameters[0].valueAsText
        ccopy.inid = parameters[1].valueAsText
        ccopy.outfile = parameters[2].valueAsText
        ccopy.outid = parameters[3].valueAsText
        ccopy.xfield = parameters[4].value
        ccopy.yfield =  parameters[5].valueAsText
        ccopy.xoutfield = parameters[6].valueAsText
        ccopy.youtfield = parameters[7].valueAsText
        ccopy.copywcursor()
        arcpy.GetMessages()
        return
