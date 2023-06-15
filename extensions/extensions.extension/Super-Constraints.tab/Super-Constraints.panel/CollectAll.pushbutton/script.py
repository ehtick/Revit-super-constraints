#! python3
import sys
# print(sys.version)
# for problems with packages once uncommet line below (with correct site-packages directory)
# sys.path.append(r"C:\Users\elyah\AppData\Local\Programs\Python\Python38\Lib\site-packages")
# import clr
import os
import os.path

# clr.AddReference("System")
# clr.AddReference('RevitAPI')
# clr.AddReference('RevitServices')
import numpy as np
import pandas as pd

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from System.Windows.Forms import FolderBrowserDialog
from System.Collections.Generic import List
from Autodesk.Revit.DB.IFC import *

from openpyxl.workbook import Workbook

global doc
# global room_solid

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

t = Transaction(doc, "Get all elements in the model")
t.Start()
 
# pic room object
# choise = uidoc.Selection
# pickedElement = choise.PickObject(ObjectType.Element, "Select room")
# selectedElement = doc.GetElement(pickedElement.ElementId)
# print(selectedElement.GetType().ToString())
# if selectedElement.GetType().ToString() != "Autodesk.Revit.DB.Architecture.Room":
#     print("Wrong element selected. Operation breaks.")
#     t.Commit()

# filter categories
directory = os.path.dirname(os.path.abspath(__file__))
name = "Revit-Categories-2022_arc.xlsx"
filename = os.path.join(directory,name)
# data directory for filter categories
data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(directory)))))
data_cat = pd.read_excel(filename)
df_cat = pd.DataFrame(data_cat)
df_cat = df_cat.loc[df_cat['Support'] == "Yes"]
df_fur = df_cat.loc[df_cat['Furniture'] == "Yes"]

#collect rooms from entire model
room_collection = FilteredElementCollector(doc).WherePasses(ElementCategoryFilter(BuiltInCategory.OST_Rooms)).WhereElementIsNotElementType().ToElements()
all_collection = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

elements  = List[ElementId]()
all_doors_elements = List[ElementId]() 
all_windows_elements = List[ElementId]()
all_furniture_elements = List[ElementId]()

# separate all elements into several categories
for elem in all_collection:
    try:
        filter_cat = elem.Category.Name
    except:
        filter_cat = None
    if df_cat['Support'][(df_cat['English'] == filter_cat)].any():
        elements.Add(elem.Id)
        if filter_cat == "Doors":
            all_doors_elements.Add(elem.Id)
        if filter_cat == "Windows":
            all_windows_elements.Add(elem.Id)
        if len(df_fur.loc[df_fur['English'] == filter_cat])>0:
            all_furniture_elements.Add(elem.Id)

#==============================================================================
#  function ckecks if element locates in the room 
#  otherwise check intersection between geometry representation
#  returns element id if element id located in the selected room
def find_room_from_elem_location(elem,room,room_solid):
    location = elem.Location
    phase_id = room.LookupParameter("Phase").AsElementId()
    phase  = doc.GetElement(phase_id)
    if location != None:
        location_type = location.GetType().ToString()
        if location_type == "Autodesk.Revit.DB.LocationPoint":
            # point location
            loc_point = location.Point
            room_elem = doc.GetRoomAtPoint(loc_point,phase)

            if room_elem != None:
                # cannot find room for columns
                if room_elem.Id.Equals(room.Id):
                    return elem.Id
            else:
                inter = find_intersection_elemToRoomSolid(elem,room_solid)
                if inter == 1:
                    return elem.Id
                elif inter == 0 and elem.Category.Name == 'Doors':
                    room_elem = elem.ToRoom
                    if room_elem != None:
                        if room_elem.Id.Equals(room.Id):
                            return elem.Id
                    else:
                        # in case it is a door
                        offset_x = 0.5
                        offset_y = 0.5
                        offset_z = 0
                        new_point = XYZ(loc_point.X + offset_x,loc_point.Y + offset_y,loc_point.Z)
                        room_elem = doc.GetRoomAtPoint(new_point,phase)
                        if room_elem != None:
                            if room_elem.Id.Equals(room.Id):
                                return elem.Id
                        else:
                            new_point = XYZ(loc_point.X - offset_x,loc_point.Y - offset_y,loc_point.Z)
                            room_elem = doc.GetRoomAtPoint(new_point,phase)
                            if room_elem != None:
                                if room_elem.Id.Equals(room.Id):
                                    return elem.Id
                elif inter == 0 and elem.Category.Name == "Windows":
                    # in case it is a window
                    # wall = elem.Host
                    # wall_loc = wall.Location.Curve
                    # dir = Line.CreateBound(loc_point,room.Location.Point).Direction
                    # curve_loop = ExporterIFCUtils.GetInstanceCutoutFromWall(doc, wall, elem, dir)[0]
                    # for c in curve_loop:
                    #     dir_c = Line.CreateBound(c.GetEndPoint(0),c.GetEndPoint(1)).Direction
                    #     if abs(dir_c.Z) == 1.:
                    #         curve = c
                    #         break
                    # vec_1 = XYZ((curve.GetEndPoint(1).X + curve.GetEndPoint(0).X)/2,
                    #             (curve.GetEndPoint(1).Y + curve.GetEndPoint(0).Y)/2,
                    #             room.Location.Point.Z)
                    # dir = Line.CreateBound(vec_1,room.Location.Point).Direction
                    # print(dir)
                    # vec_1_off= vec_1.Add(dir)
                    # vec_1_off = XYZ(vec_1_off.X,vec_1_off.Y,room.Location.Point.Z)
                    # print(doc.GetRoomAtPoint(vec_1_off,phase).Id)
                    
                    offset_x = 1.
                    offset_y = 1.
                    offset_z = 0.5
                    new_point = XYZ(loc_point.X + offset_x,loc_point.Y + offset_y,loc_point.Z)
                    room_elem = doc.GetRoomAtPoint(new_point,phase)
                    if room_elem != None:
                        if room_elem.Id.Equals(room.Id):
                            return elem.Id
                    else:
                        new_point = XYZ(loc_point.X - offset_x,loc_point.Y - offset_y,loc_point.Z)
                        room_elem = doc.GetRoomAtPoint(new_point,phase)
                        if room_elem != None:
                            if room_elem.Id.Equals(room.Id):
                                return elem.Id
                        else:
                            new_point = XYZ(loc_point.X,loc_point.Y,loc_point.Z-offset_z)
                            room_elem = doc.GetRoomAtPoint(new_point,phase)
                            if room_elem != None:
                                if room_elem.Id.Equals(room.Id):
                                    return elem.Id

        elif location_type == "Autodesk.Revit.DB.LocationCurve":
            # curve location
            loc_curve = location.Curve
            if room_solid.IntersectWithCurve(loc_curve,SolidCurveIntersectionOptions()) != None:
                return elem.Id
            else:
                inter = find_intersection_elemToRoomSolid(elem,room_solid)
                if inter == 1:
                    return elem.Id
        # elif location_type == "Location":

        else:
            # find intersections
            inter = find_intersection_elemToRoomSolid(elem,room_solid)
            if inter == 1:
                return elem.Id
#==============================================================================
# function finds opening cut in the wall
def get_opening_cut(door,wall,dir,room):
    elem_geom = door.get_Geometry(Options())
    door_solid = None
    for geomInst in elem_geom:
        if geomInst.GetType().ToString() == "Autodesk.Revit.DB.GeometryInstance":
                instGeom = geomInst.GetInstanceGeometry()
                for instObj in instGeom:
                    if instObj.GetType().ToString() == "Autodesk.Revit.DB.Solid":
                        if instObj.Faces.Size != 0 and instObj.Edges.Size != 0 and instObj.Volume > 0.0:
                            door_solid = instObj
                            door_solid = BooleanOperationsUtils.ExecuteBooleanOperation(door_solid,instObj,BooleanOperationsType.Union)
    dif_solid = None
    wall_solid = None
    elem_geom = wall.get_Geometry(Options())
    for geomInst in elem_geom:
        # if geomInst.GetType().ToString() == "Autodesk.Revit.DB.Solid":
        if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0 and geomInst.Volume > 0.0:
            wall_solid = geomInst
            dif_solid = BooleanOperationsUtils.ExecuteBooleanOperation(door_solid,wall_solid,BooleanOperationsType.Difference)
            
    if dif_solid != None:
        for face in dif_solid.Faces:
            loc = room.Location.Point
            dir_rm = face.ComputeNormal(UV(loc.X,loc.Y))
            if dir.IsAlmostEqualTo(dir_rm):
                return face.GetEdgesAsCurveLoops()
#==============================================================================
#  function finds intersections between element solid and room solid
#  returns i if intersections occured   
def find_intersection_elemToRoomSolid(elem, room_solid):
    elem_geom = elem.get_Geometry(Options())
    inter = 0
    for geomInst in elem_geom:
        if geomInst.GetType().ToString() == "Autodesk.Revit.DB.GeometryInstance":
                instGeom = geomInst.GetInstanceGeometry()
                for instObj in instGeom:
                    if instObj.GetType().ToString() == "Autodesk.Revit.DB.Solid":
                        if instObj.Faces.Size != 0 and instObj.Edges.Size != 0:
                            furn_solid = instObj
                            try:
                                interSolid = BooleanOperationsUtils.ExecuteBooleanOperation(room_solid,furn_solid,BooleanOperationsType.Intersect)
                                if interSolid.Volume > 0.0000001:
                                    inter = 1 
                                    return inter
                            except:
                                pass
        elif geomInst.GetType().ToString() == "Autodesk.Revit.DB.Solid":
                if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                    furn_solid = geomInst
                    try:
                        interSolid = BooleanOperationsUtils.ExecuteBooleanOperation(room_solid,furn_solid,BooleanOperationsType.Intersect)
                        if interSolid.Volume > 0.0:
                            inter = 1 
                            return inter
                    except:
                        pass
        elif geomInst.GetType().ToString() == "Autodesk.Revit.DB.Line":
            inter_options = SolidCurveIntersectionOptions()
            interSolid = room_solid.IntersectWithCurve(geomInst,inter_options)
            # print(interSolid.ResultType)
            res = interSolid.ResultType
            if res == 0:
                return 1          
    return inter

# data frames for writing all information
df_bound_all = pd.DataFrame()
df_walls_all = pd.DataFrame()
df_floors_all = pd.DataFrame()
df_windows_all = pd.DataFrame()
df_doors_all = pd.DataFrame()
df_furn_dist_all = pd.DataFrame()
df_all = pd.DataFrame()

# script starts
for room in room_collection:
    room_location = room.Location.Point
    options = SpatialElementBoundaryOptions()
    calculator = SpatialElementGeometryCalculator(doc,options)
    results = calculator.CalculateSpatialElementGeometry(room)
    room_solid = results.GetGeometry()

    # create collection of room containing elements e.g. windows,doors,furniture
    room_elements = List[ElementId]()
    windows_elements = List[ElementId]()
    doors_elements = List[ElementId]()
    furniture_elements = List[ElementId]()
    floor_elements = List[ElementId]()

    for id in elements:
        elem = doc.GetElement(id)
        elemId = find_room_from_elem_location(elem,room,room_solid)
        if elemId != None:
            if all_windows_elements.Contains(id):
                windows_elements.Add(id)
                room_elements.Add(id)
            if all_doors_elements.Contains(id):
                doors_elements.Add(id)
                room_elements.Add(id)
            if all_furniture_elements.Contains(id):
                furniture_elements.Add(id)
                room_elements.Add(id)
    # 
    # 
    # 
    # 
    # 
    # collect all bounding elements of the room: walls and floors
    face_dic = {}
    bounds_elem = List[ElementId]()
    added_elements = List[ElementId]()
    df_bound = pd.DataFrame()#local data frame
    for face in room_solid.Faces:
        face_list = results.GetBoundaryFaceInfo(face)
        for f in face_list:
            link_elem = f.SpatialBoundaryElement
            try:
                link_elem_Id = link_elem.HostElementId
            except:
                link_elem_Id = link_elem.LinkedElementId
            elem = doc.GetElement(link_elem_Id)
            if not bounds_elem.Contains(elem.Id):
                # added_elements.Add(elem.Id)
                bounds_elem.Add(elem.Id)
                if not room_elements.Contains(elem.Id):
                    room_elements.Add(elem.Id)
                face_dic[elem.Id.IntegerValue] = f.GetSubface().ComputeNormal(UV(room_location.X,room_location.Y))
                new_row = pd.Series({'Room_Id':room.Id,
                                        'Room_uniqueId':room.UniqueId,
                                        'ElementId':elem.Id,
                                        'Element_uniqueId': elem.UniqueId,
                                        'Type' : elem.Name,
                                        'Normal_to_center_room': face_dic[elem.Id.IntegerValue]})
                df_bound = pd.concat([df_bound,new_row.to_frame().T],ignore_index=True)
    # 
    # 
    # 
    # 
    #   
    #collect constraints from walls: perpendiculary, parallelity, angles, distance           
    df_walls = pd.DataFrame()
    resultArray = IntersectionResultArray()
    # check if volume of intersection/touching between walls are max (!?)
    # filter for only maximum values
    perpId_dic ={}
    for id in face_dic.keys():
        dir = face_dic[id]
        elem = doc.GetElement(ElementId(id))
        perpId = []
        angles = []
        nearest_walls = []
        nearest_angles = []
        distances = []
        parallel_walls = []
        if abs(dir.X) == 1.0 or abs(dir.Y)==1.0 and abs(dir.Z) == 0.0:
            # we mean a wall
            loc_curve = elem.get_Location()
            curve = loc_curve.Curve
            start_point = curve.GetEndPoint(0)
            end_point = curve.GetEndPoint(1)
            direction = Line.CreateBound(start_point,end_point).Direction
            line = Line.CreateUnbound(start_point,direction)
            vec_1 = end_point.Subtract(start_point).Normalize()
            width_1 = elem.Width
            for id_temp in face_dic.keys():
                dir_temp = face_dic[id_temp]
                if id != id_temp and (abs(dir_temp.X) == 1.0 or abs(dir_temp.Y)==1.0) and abs(dir_temp.Z)==0.0:
                    elem_an = doc.GetElement(ElementId(id_temp))
                    loc_curve_an = elem_an.Location
                    curve_an = loc_curve_an.Curve
                    start_point_an = curve_an.GetEndPoint(0)
                    end_point_an = curve_an.GetEndPoint(1)
                    direction_an = Line.CreateBound(start_point_an,end_point_an).Direction
                    line_an = Line.CreateUnbound(start_point_an,direction_an)
                    vec_2 = end_point_an.Subtract(start_point_an).Normalize()
                    inter = curve.Intersect(curve_an)
                    width_2 = elem_an.Width
                    angle = round(vec_1.AngleTo(vec_2)*180/np.pi)
                    if inter == SetComparisonResult.Overlap:
                        # check if walls are perpendicular 
                        distances.append(None)
                        parallel_walls.append(None)
                        if angle == 90 or angle == 0:
                            angles.append(90)
                            perpId.append(id_temp)
                            nearest_walls.append(id_temp)
                        else:
                            angles.append(angle)
                            perpId.append(None)
                            nearest_walls.append(None)
                    if inter == SetComparisonResult.Disjoint:
                        # means that walls are disjoint!
                        # check if walls perpendicular
                        if line.Intersect(line_an) == SetComparisonResult.Overlap:
                            distances.append(None)
                            parallel_walls.append(None)
                            if angle == 90 or angle == 0:
                                angles.append(90)
                                perpId.append(id_temp)
                                nearest_walls.append(id_temp)
                            else:
                                angles.append(angle)
                                perpId.append(None)
                                nearest_walls.append(id_temp)
                        else:
                            if angle == 0 or angle == 180:
                                # parallel
                                angles.append(0)
                                distance = None
                                closest_pnt = line.Project(start_point_an).XYZPoint
                                if closest_pnt.Equals(start_point):
                                    direction = Line.CreateBound(end_point,start_point).Direction
                                    line = Line.CreateUnbound(start_point,direction)
                                    distance = round((line.Project(start_point_an).Distance -width_1/2 - width_2/2)*0.3048,2)
                                    distances.append(distance)
                                else:
                                    distance = round((line.Project(start_point_an).Distance -width_1/2 - width_2/2)*0.3048,2)
                                    distances.append(distance)
                                perpId.append(None)
                                nearest_walls.append(None)
                                parallel_walls.append(id_temp)
                            elif angle == 90:
                                #perpendicular
                                angles.append(90)
                                distances.append(None)
                                perpId.append(id_temp)
                                nearest_walls.append(None)
                                parallel_walls.append(None)
                            else:
                                # not parallel or perpendicular
                                angles.append(angle)
                                distances.append(None)
                                perpId.append(None)
                                nearest_walls.append(id_temp)
                                parallel_walls.append(None)
                elif id != id_temp and abs(dir_temp.Z) == 1 and abs(dir_temp.X) == 0.0 and abs(dir_temp.Y) == 0.0:
                    # means that walls are perpendicular to the floor
                    angles.append(90)
                    distances.append(None)
                    perpId.append(id_temp)
                    nearest_walls.append(None)
                    parallel_walls.append(None)
            
            perpId_dic[id] = perpId
            height = elem.LookupParameter('Unconnected Height').AsDouble()              
            new_row_walls = pd.Series({'Room_Id':room.Id,
                                        'Room_uniqueId':room.UniqueId,
                                        'ElementId': id,
                                        'Element_uniqueId': elem.UniqueId,
                                        'Width': width_1*0.3048,
                                        'Height':height*0.3048,
                                        'Perpendicular_walls_id':perpId,
                                        'Parallel_walls_id':parallel_walls,
                                        'Distance_to_parall':distances,
                                        'Nearest_walls_id':nearest_walls,
                                        'Angles_to_walls':angles})
            df_walls = pd.concat([df_walls,new_row_walls.to_frame().T],ignore_index= True)
    # 
    # 
    # 
    # 
    #
    # collect constraints from floors: parallelity!, angles?, distance!         
    df_floors = pd.DataFrame()
    resultArray = IntersectionResultArray()
    floor_distance = {}
    dis_to_m = []
    dir_t = 0
    id_t = None
    parallel_floors = []
    roof = []
    for id in face_dic.keys():
        dir = face_dic[id]
        if abs(dir.Z) == 1.0 or abs(dir.Z)> 0.:
            if abs(dir.Z) == 1.0:
                parallel_floors.append(id)
            else:
                roof.append(id)
            room_bb = room.ClosedShell.GetBoundingBox()
            room_bb_min = room_bb.Min
            room_bb_max = room_bb.Max
            dis = round(abs(room_bb_max.Z-room_bb_min.Z)*0.3048,2)
            floor_distance[id] = dis
    for id in face_dic.keys():
        dir = face_dic[id]
        elem = doc.GetElement(ElementId(id))
        if abs(dir.Z) == 1.0 or abs(dir.Z)> 0.:
            new_par = []
            for val in parallel_floors:
                if val != id and id not in roof:
                    new_par.append(val)
            new_row_floors = pd.Series({'Room_Id':room.Id,
                                            'Room_uniqueId':room.UniqueId,
                                            'ElementId': id,
                                            'Element_uniqueId': elem.UniqueId,
                                            'Parallel_floor_id':new_par,
                                            'Distance_max':floor_distance[id]})
            df_floors = pd.concat([df_floors,new_row_floors.to_frame().T],ignore_index= True)
    # 
    # 
    # 
    # 
    #
    # collect constraints from doors: distance to edges (floor, wall), width, hight
    df_doors = pd.DataFrame()
    doors_wh = {}
    distance_dic = {}
    for id in doors_elements:
        door = doc.GetElement(id)
        wall = door.Host
        width = wall.Width
        id_wall = wall.Id
        cut_loop = None
        if id_wall.IntegerValue not in face_dic.keys():
            continue
        dir = face_dic[id_wall.IntegerValue]
        try:
            cut_loop = ExporterIFCUtils.GetInstanceCutoutFromWall(doc, wall, door, dir)[0]
            # print('test')

        except:
            cut_loop = get_opening_cut(door,wall,dir,room)
            pass
        perp_elem = perpId_dic[id_wall.IntegerValue]
        closest_dis = []
        distance_ids = []
        for id_el in perp_elem:
            if id_el != None:
                elem = doc.GetElement(ElementId(id_el))
                if cut_loop != None:
                    for curve in cut_loop:
                        if str(curve.GetType()) == 'Autodesk.Revit.DB.CurveLoop':
                            break

                        dir_c = Line.CreateBound(curve.GetEndPoint(0),curve.GetEndPoint(1)).Direction
                        if abs(dir_c.Z) == 1.0:
                            if face_dic[id_el].Z == 0.0:
                                dir_c = Line.CreateBound(curve.GetEndPoint(0),curve.GetEndPoint(1)).Direction
                                line = Line.CreateUnbound(curve.GetEndPoint(0),dir_c)
                                width_p = elem.Width
                                loc_elem = elem.Location.Curve
                                point_list = List[ClosestPointsPairBetweenTwoCurves]()
                                closest_pnt = curve.ComputeClosestPoints(loc_elem, False, False,False,point_list)
                                for points in closest_pnt:
                                    first_point = points.XYZPointOnFirstCurve
                                    second_point = points.XYZPointOnSecondCurve
                                    dis_to_cut = round(first_point.DistanceTo(second_point)*0.3048 - width_p/2*0.3048,2)
                                    closest_dis.append(dis_to_cut)
                                    distance_ids.append(id_el)
                        if abs(dir_c.Z) == 0.0:
                            if face_dic[id_el].Z == 1.0:
                                proj_pnt = curve.GetEndPoint(0)
                                elem_geom = elem.get_Geometry(Options())
                                dis = 1
                                temp_dist = []
                                for geomInst in elem_geom:
                                    if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                                            floor_solid = geomInst
                                            for face in floor_solid.Faces:
                                                if dis != 0:
                                                    normal = face.ComputeNormal(UV(proj_pnt.X,proj_pnt.Y))
                                                    if normal.Z==-1.0 and face != None:
                                                        try:
                                                            dis = round(face.Project(proj_pnt).Distance*0.3084,3)
                                                            temp_dist.append(dis)
                                                        except:
                                                            dis = 0.0
                                                            temp_dist.append(dis)
                                min_dis = min(temp_dist)
                                distance_ids.append(id_el)
                                closest_dis.append(dis)
                            elif face_dic[id_el].Z == -1.0:
                                proj_pnt = curve.GetEndPoint(0)
                                elem_geom = elem.get_Geometry(Options())
                                dis = 1
                                temp_dist = []
                                for geomInst in elem_geom:
                                    if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                                            floor_solid = geomInst
                                            for face in floor_solid.Faces:
                                                if dis != 0:
                                                    normal = face.ComputeNormal(UV(proj_pnt.X,proj_pnt.Y))
                                                    if normal.Z==1.0:
                                                        dis = round(face.Project(proj_pnt).Distance*0.3084,3)
                                                        temp_dist.append(dis)
                                min_dis = min(temp_dist)
                                distance_ids.append(id_el)
        distance_dic[id] = closest_dis
        dType = doc.GetElement(door.GetTypeId())
        width = dType.get_Parameter(BuiltInParameter.DOOR_WIDTH).AsDouble() 
        height = dType.get_Parameter(BuiltInParameter.DOOR_HEIGHT).AsDouble()
        doors_wh[id] = [width,height]
        new_row_doors = pd.Series({'Room_Id':room.Id,
                                    'Room_uniqueId':room.UniqueId,
                                    'ElementId': id,
                                    'Element_uniqueId': door.UniqueId,
                                    'Door_width':width*0.3048,
                                    'Door_height':height*0.3048,
                                    'Nearest_elementIds':distance_ids,
                                    'Distance_to_edges':distance_dic[id]})
        df_doors = pd.concat([df_doors,new_row_doors.to_frame().T],ignore_index= True)                                              
    # 
    # 
    # 
    # 
    #
    #collect constraints from windows: distance to edges (floor, wall), width, hight
    df_windows = pd.DataFrame()
    distance_dic = {}
    for id in windows_elements:
        window = doc.GetElement(id)
        if str(window.Host.GetType()) == 'Autodesk.Revit.DB.ExtrusionRoof':
            continue
        window_loc = window.Location.Point
        wall = window.Host
        width = wall.Width
        id_wall = wall.Id
        cut_loop = None
        if id_wall.IntegerValue not in face_dic.keys():
            continue
        dir = face_dic[id_wall.IntegerValue]
        try:
            cut_loop = ExporterIFCUtils.GetInstanceCutoutFromWall(doc, wall, window, dir)[0]
        except:
            cut_loop = get_opening_cut(window,wall,dir,room)
            pass
        perp_elem = perpId_dic[id_wall.IntegerValue]
        closest_dis = []
        distance_ids = []
        for id_el in perp_elem:
            if id_el != None:
                elem = doc.GetElement(ElementId(id_el))
                if cut_loop != None:
                    dim_arr  = []
                    for curve in cut_loop:
                        dim_arr.append(curve.Length)
                        dir_c = Line.CreateBound(curve.GetEndPoint(0),curve.GetEndPoint(1)).Direction
                        if abs(dir_c.Z) == 1.0:
                            if face_dic[id_el].Z == 0.0:
                                dir_c = Line.CreateBound(curve.GetEndPoint(0),curve.GetEndPoint(1)).Direction
                                line = Line.CreateUnbound(curve.GetEndPoint(0),dir_c)
                                width_p = elem.Width
                                loc_elem = elem.Location.Curve
                                point_list = List[ClosestPointsPairBetweenTwoCurves]()
                                closest_pnt = curve.ComputeClosestPoints(loc_elem, False, False,False,point_list)
                                for points in closest_pnt:
                                    first_point = points.XYZPointOnFirstCurve
                                    second_point = points.XYZPointOnSecondCurve
                                    dis_to_cut = round(first_point.DistanceTo(second_point)*0.3048 - width_p/2*0.3048,2)
                                    closest_dis.append(dis_to_cut)
                                    distance_ids.append(id_el)
                        if abs(dir_c.Z) == 0.0:
                            if face_dic[id_el].Z == 1.0:
                                proj_pnt = curve.GetEndPoint(0)
                                elem_geom = elem.get_Geometry(Options())
                                dis = 1
                                temp_dist = []
                                for geomInst in elem_geom:
                                    if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                                            floor_solid = geomInst
                                            for face in floor_solid.Faces:
                                                if dis != 0:
                                                    normal = face.ComputeNormal(UV(proj_pnt.X,proj_pnt.Y))
                                                    if normal.Z==-1.0:
                                                        dis = round(face.Project(proj_pnt).Distance*0.3084,3)
                                                        temp_dist.append(dis)
                                min_dis = min(temp_dist)
                                distance_ids.append(id_el)
                                closest_dis.append(dis)

                            elif face_dic[id_el].Z == -1.0:
                                proj_pnt = curve.GetEndPoint(0)
                                elem_geom = elem.get_Geometry(Options())
                                dis = 1
                                temp_dist = []
                                for geomInst in elem_geom:
                                    if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                                            floor_solid = geomInst
                                            for face in floor_solid.Faces:
                                                if dis != 0:
                                                    normal = face.ComputeNormal(UV(proj_pnt.X,proj_pnt.Y))
                                                    if normal.Z==1.0:
                                                        dis = round(face.Project(proj_pnt).Distance*0.3084,3)
                                                        temp_dist.append(dis)
                                min_dis = min(temp_dist)
                                distance_ids.append(id_el)
        distance_dic[id] = closest_dis
        wType = doc.GetElement(window.GetTypeId())
        # width = wType.get_Parameter(BuiltInParameter.WINDOW_WIDTH).AsDouble() 
        # height = wType.get_Parameter(BuiltInParameter.WINDOW_HEIGHT).AsDouble()
        new_row_windows = pd.Series({'Room_Id':room.Id,
                                        'Room_uniqueId':room.UniqueId,
                                        'ElementId': id,
                                        'Element_uniqueId': window.UniqueId,
                                        'Window_width':min(dim_arr)*0.3048,
                                        'Window_height':max(dim_arr)*0.3048,
                                        'Nearest_elementIds':distance_ids,
                                        'Distance_to_edges':distance_dic[id]})
        df_windows = pd.concat([df_windows,new_row_windows.to_frame().T],ignore_index= True)            
    # 
    # 
    # 
    # 
    #           
    # analyse furniture, calculate nearest bounding element
    df_furn_dist = pd.DataFrame()
    i = 0
    for id in furniture_elements:
        furn = doc.GetElement(id)
        loc_furn = furn.Location.Point
        nearest_elem = []
        distance = []
        distance_ids = []
        closest_dis = []
        nearest_elem = []
        for b_el in bounds_elem:
            dir = face_dic[b_el.IntegerValue]
            if dir.Z == 0.0:
                #walls
                wall = doc.GetElement(b_el)
                wall_loc = wall.Location
                location_type = wall_loc.GetType().ToString()
                if location_type == "Autodesk.Revit.DB.LocationPoint":
                    wall_point = wall_loc.Point
                    loc_furn_new = XYZ(loc_furn.X,loc_furn.Y,wall_point.Z)
                    dist = round(wall_point.DistanceTo(loc_furn_new)*0.3048,2)
                    closest_dis.append(dist)
                    distance_ids.append(b_el.IntegerValue)
                if location_type == "Autodesk.Revit.DB.LocationCurve":
                    wall_curve = wall_loc.Curve
                    wall_w = wall.Width
                    loc_furn_new = XYZ(loc_furn.X,loc_furn.Y,wall_curve.GetEndPoint(0).Z)
                    dist = round(wall_curve.Project(loc_furn_new).Distance*0.3048 - wall_w/2*0.3048,2)
                    closest_dis.append(dist)
                    distance_ids.append(b_el.IntegerValue)

        distance_dic[id] = closest_dis
        new_row_furn = pd.Series({'Room_Id':room.Id,
                                    'Room_uniqueId':room.UniqueId,
                                    'ElementId': id,
                                    'Element_uniqueId': furn.UniqueId,
                                    'Nearest_elementIds':distance_ids,
                                    'Distance_to_nearest':distance_dic[id]})
        df_furn_dist = pd.concat([df_furn_dist,new_row_furn.to_frame().T],ignore_index= True)
    # 
    # 
    # 
    # 
    #  
    # write all in dataframe
    df = pd.DataFrame()
    for id in room_elements:
        elem = doc.GetElement(id)
        try:
                eId = elem.GetTypeId()
                elemType = doc.GetElement(eId)
                if elemType != None:
                    fam_name = elemType.FamilyName
        except:
            fam_name = elem.Symbol.Family.Name
        room_name = room.LookupParameter('Name').AsString()
        new_row = pd.Series({'Level_Id': room.LevelId,
                             'Level_name':room.Level.Name,
                             'Room_uniqueId':room.UniqueId,
                             'Room_Id': room.Id,
                             'Room_number':room.Number,
                             'Room_name':room_name,
                             'ElementId': elem.Id,
                             'Element_uniqueId': elem.UniqueId,
                             'Family':fam_name,
                             'Typ':elem.Name,
                             'Category':elem.Category.Name})
        df = pd.concat([df,new_row.to_frame().T],ignore_index= True)


    #add individual data from to general data frame
    df_bound_all = pd.concat([df_bound_all,df_bound],ignore_index=True)
    df_walls_all = pd.concat([df_walls_all,df_walls],ignore_index=True)
    df_floors_all = pd.concat([df_floors_all,df_floors],ignore_index=True)
    df_windows_all = pd.concat([df_windows_all,df_windows],ignore_index=True)
    df_doors_all = pd.concat([df_doors_all,df_doors],ignore_index=True)
    df_furn_dist_all = pd.concat([df_furn_dist_all,df_furn_dist],ignore_index=True)
    df_all = pd.concat([df_all,df],ignore_index=True)

# print all data frames
nameOfFile_csv = 'data\\tables\\space_elements_bounds.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_bound_all.to_csv(completename_csv)

nameOfFile_csv = 'data\\tables\\space_elements_walls.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_walls_all.to_csv(completename_csv)

nameOfFile_csv = 'data\\tables\\space_elements_floors.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_floors_all.to_csv(completename_csv)

nameOfFile_csv = 'data\\tables\\space_elements_doors.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_doors_all.to_csv(completename_csv) 

nameOfFile_csv = 'data\\tables\\space_elements_windows.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_windows_all.to_csv(completename_csv) 

nameOfFile_csv = 'data\\tables\\space_elements_furniture.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_furn_dist_all.to_csv(completename_csv)

nameOfFile = 'data\\tables\\space_elements.xlsx'
nameOfFile_csv = 'data\\tables\\space_elements.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_all.to_csv(completename_csv)

# df_sum = pd.DataFrame()
# print('####### ROOM REPORT ######')
# print(df['Category'].value_counts())
# print("Number of doors:" + str(df_doors.shape[0]))
# print(df_doors.agg({'Door_width':['mean','min','max'],'Door_height':['mean','min','max']}))
# print("Number of floors:" + str(df_floors.shape[0]))
# print(df_floors.agg({'Distance_to_parall':['count','mean','min','max']}))
t.Commit()