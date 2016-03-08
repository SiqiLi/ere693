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

            # Import arcpy module
            import arcpy


            # Local variables:
            Reclass_rast1 = "Reclass_rast1"
            FlowDir_DEMf1 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\FlowDir_DEMf1"
            Impervious = "Impervious"
            Impervious__3_ = Impervious
            Feature_Impe1 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\Feature_Impe1"
            BlockSt_Feat1 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\BlockSt_Feat1"
            Aggrega_Bloc1 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\Aggrega_Bloc1"
            flowacc_weight = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\flowacc_weight"
            Flowacc_unweight = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\Flowacc_unweight"
            rastercalc1 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\rastercalc1"
            Reclass_rast2 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\Reclass_rast2"
            rastercalc2 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\rastercalc2"
            StreamT_rasterc1 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\Lab06Data.gdb\\StreamT_rasterc1"

            # Process: Calculate Field
            arcpy.CalculateField_management(Impervious, "LENGTH", "1", "VB", "")

            # Process: Feature to Raster
            arcpy.FeatureToRaster_conversion(Impervious__3_, "LENGTH", Feature_Impe1, "4")

            # Process: Block Statistics
            BlockSt_Feat1 = arcpy.gp.BlockStatistics_sa(Feature_Impe1, "Rectangle 10 10 CELL", "SUM", "DATA")

            # Process: Aggregate
            Aggrega_Bloc1 = arcpy.gp.Aggregate_sa(BlockSt_Feat1, "10", "MEAN", "EXPAND", "DATA")

            # Process: Flow Accumulation
            flowacc_weight = arcpy.gp.FlowAccumulation_sa(FlowDir_DEMf1, Aggrega_Bloc1, "FLOAT")

            # Process: Flow Accumulation (2)
            Flowacc_unweight = arcpy.gp.FlowAccumulation_sa(FlowDir_DEMf1, "", "FLOAT")

            # Process: Raster Calculator
            rastercalc1 = arcpy.gp.RasterCalculator_sa("\"%flowacc_weight%\" / \"%Flowacc_unweight%\"")

            # Process: Reclassify
            Reclass_rast2 = arcpy.gp.Reclassify_sa(rastercalc1, "Value", "0 10 1;10 20 2;20 30 3;30 40 4;40 50 5;50 60 6;60 70 7;70 80 8;80 90 9;90 100 10", "DATA")

            # Process: Raster Calculator (2)
            rastercalc2 = arcpy.gp.RasterCalculator_sa("\"%Reclass_rast1%\" * \"%Reclass_rast2%\"")

            # Process: Stream to Feature
            StreamT_rasterc1 = arcpy.gp.StreamToFeature_sa(rastercalc2, FlowDir_DEMf1, "SIMPLIFY")

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
            # Import arcpy module
            import arcpy


            # Local variables:
            rastercalc = "rastercalc"
            rastc5 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\rastc5"
            rastc10 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\rastc10"
            rastc50 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\rastc50"
            rastc100 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\rastc100"
            rastercalc1 = "rastercalc1"
            rastc = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\rastc"
            q2 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\q2"
            q5 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\q5"
            q10 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\q10"
            rastc25 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\rastc25"
            q25 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\q25"
            q50 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\q50"
            q100 = "\\\\hd.ad.syr.edu\\01\\e51673\\Documents\\Desktop\\Courses\\ERE693 GIS-Modeling\\Lab_06\\processdata.gdb\\q100"

            # Process: Raster Calculator (2)
            rastc5 = arcpy.gp.RasterCalculator_sa("248 * Power(\"%rastercalc%\" * 43560 / 5280 / 5280,0.670)")

            # Process: Raster Calculator (3)
            rastc10 = arcpy.gp.RasterCalculator_sa("334 * Power(\"%rastercalc%\" * 43560 / 5280 / 5280,0.665)")

            # Process: Raster Calculator (5)
            rastc50 = arcpy.gp.RasterCalculator_sa("581 * Power(\"%rastercalc%\" * 43560 / 5280 / 5280,0.650)")

            # Process: Raster Calculator (6)
            rastc100 = arcpy.gp.RasterCalculator_sa("719 * Power(\"%rastercalc%\" * 43560 * 43560 / 5280 / 5280,0.643)")

            # Process: Raster Calculator
            rastc = arcpy.gp.RasterCalculator_sa("144 * Power(\"%rastercalc%\"  * 43560 / 5280 / 5280,0.691)")

            # Process: Raster Calculator (7)
            q2 = arcpy.gp.RasterCalculator_sa("7.87*Power(\"%rastercalc%\",0.539) *Power( \"%rastercalc1%\",0.686)*Power(\"%rastc%\",0.29)")

            # Process: Raster Calculator (8)
            q5 = arcpy.gp.RasterCalculator_sa("16.3*Power(\"%rastercalc%\",0.489) *Power( \"%rastercalc1%\",0.572)*Power(\"%rastc%\",0.286)")

            # Process: Raster Calculator (9)
            q10 = arcpy.gp.RasterCalculator_sa("22.7*Power(\"%rastercalc%\",0.463) *Power( \"%rastercalc1%\",0.515)*Power(\"%rastc%\",0.289)")

            # Process: Raster Calculator (4)
            rastc25 = arcpy.gp.RasterCalculator_sa("467 * Power(\"%rastercalc%\" * 43560 / 5280 / 5280,0.655)")

            # Process: Raster Calculator (10)
            q25 = arcpy.gp.RasterCalculator_sa("28.5*Power(\"%rastercalc%\",0.39) *Power( \"%rastercalc1%\",0.436)*Power(\"%rastc25%\",0.338)")

            # Process: Raster Calculator (11)
            q50 = arcpy.gp.RasterCalculator_sa("37.4*Power(\"%rastercalc%\",0.391) *Power( \"%rastercalc1%\",0.396)*Power(\"%rastc%\",0.325)")

            # Process: Raster Calculator (12)
            q100 = arcpy.gp.RasterCalculator_sa("48*Power(\"%rastercalc%\",0.392) *Power( \"%rastercalc1%\",0.358)*Power(\"%rastc%\",0.312)")
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
		
