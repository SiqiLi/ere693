import os, sys, shutil, arcpy
import traceback, time

def log(message):
    arcpy.AddMessage(message)
    with file(sys.argv[0]+".log", 'a') as logFile:
        logFile.write("%s:\t%s\n" % (time.asctime(), message))
    
class Toolbox(object):
    def __init__(self):
        self.label = "WIP tools"
        self.alias = ""
        self.tools = [TopoHydro, ImpCov, Runoff]
        
class TopoHydro(object):
    def __init__(self):
        self.label = "Topography and Hydrology Analysis"
        self.description = "Establishes the watershed and stream network"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Input Digital Elevation Model",
            name="DEM",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Analysis Mask",
            name="Mask",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        param2 = arcpy.Parameter(
            displayName="Threshold accumulation for Stream formation (acres)",
            name="StreamFormation",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1, param2 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameters are %s, %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText))


            # Import arcpy module
            import arcpy


            # Local variables:
            DEM = "DEM"
            DEMfill = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\DEMfill"
            AnalysisMask = "AnalysisMask"
            AnalysisMaskRaster = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\AnalysisMaskRaster"
            Output_drop_raster = ""
            FlowDir_DEMf1 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\FlowDir_DEMf1"
            FlowAcc_Flow1 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\FlowAcc_Flow1"
            rastercalc = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\rastercalc"
            Reclass_rast1 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\Reclass_rast1"
            StreamT_Reclass1 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\StreamT_Reclass1"

            # Set Geoprocessing environments
            arcpy.env.snapRaster = "DEM"
            arcpy.env.mask = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\AnalysisMaskRaster"

            # Process: Fill
            DEMfill = arcpy.gp.Fill_sa(DEM, "")

            # Process: Polygon to Raster
            AnalysisMaskRaster = arcpy.PolygonToRaster_conversion(AnalysisMask, "OBJECTID", "CELL_CENTER", "NONE", "140")

            # Process: Flow Direction
            tempEnvironment0 = arcpy.env.mask
            arcpy.env.mask = AnalysisMaskRaster
            FlowDir_DEMf1 = arcpy.gp.FlowDirection_sa(DEMfill, "NORMAL", Output_drop_raster)
            arcpy.env.mask = tempEnvironment0

            # Process: Flow Accumulation
            FlowAcc_Flow1 = arcpy.gp.FlowAccumulation_sa(FlowDir_DEMf1, "", "FLOAT")

            # Process: Raster Calculator
            rastercalc = arcpy.gp.RasterCalculator_sa("\"%FlowAcc_Flow1%\" * 40*40 / 43560")

            # Process: Reclassify
            Reclass_rast1 = arcpy.gp.Reclassify_sa(rastercalc, "Value", "0 6997 NODATA;6997 28312.03125 1", "DATA")

            # Process: Stream to Feature
            StreamT_Reclass1 = arcpy.gp.StreamToFeature_sa(Reclass_rast1, FlowDir_DEMf1, "SIMPLIFY")


        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return

class ImpCov(object):
    def __init__(self):
        self.label = "Imperviousness Analysis"
        self.description = "Impervious area contributions"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Impervious Areas",
            name="ImperviousAreas",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Lakes",
            name="Lakes",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameters are %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
        
class Runoff(object):
    def __init__(self):
        self.label = "Runoff Calculations"
        self.description = "Calculation of standard storm flows via USGS regression equations"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Curve Number",
            name="Landuse",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameter is %s" % (parameters[0].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
		
www