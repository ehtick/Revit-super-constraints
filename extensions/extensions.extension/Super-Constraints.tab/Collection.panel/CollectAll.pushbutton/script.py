#! python3
import sys
# print(sys.version)
# for problems with packages once uncommet line below (with correct site-packages directory)
sys.path.append(r"C:\Users\elyah\AppData\Local\Programs\Python\Python38\Lib\site-packages")

import os
import os.path
import numpy as np
import pandas as pd
import statistics
import bisect
# from openpyxl.workbook import Workbook

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from System.Windows.Forms import FolderBrowserDialog
from System.Collections.Generic import List
from Autodesk.Revit.DB.IFC import *

global doc

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# t = Transaction(doc, "Get all elements in the model")
# t.Start()

# filter categories
directory = os.path.dirname(os.path.abspath(__file__))
name = "Revit-Categories-2022_arc.xlsx"
filename = os.path.join(directory,name)
# data directory for filter categories
data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(directory)))))
data_cat = pd.read_excel(filename)
df_cat = pd.DataFrame(data_cat)
df_cat = df_cat.loc[df_cat['Support'] == "Yes"]
category = df_cat.values
df_fur = df_cat.loc[df_cat['Furniture'] == "Yes"]
furniture = df_fur.values
#collect rooms and elements from entire model
room_collection = FilteredElementCollector(doc).WherePasses(ElementCategoryFilter(BuiltInCategory.OST_Rooms)).WhereElementIsNotElementType().ToElements()
all_collection = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

elements  = List[ElementId]()
all_doors_elements = List[ElementId]() 
all_windows_elements = List[ElementId]()
all_furniture_elements = List[ElementId]()
all_ceiling_elements = List[ElementId]()
# separate all elements into several categories
for elem in all_collection:
    try:
        filter_cat = elem.Category.Name
    except:
        filter_cat = None
    if filter_cat in category:
        elements.Add(elem.Id)
        if filter_cat == "Doors":
            all_doors_elements.Add(elem.Id)
        if filter_cat == "Windows":
            all_windows_elements.Add(elem.Id)
        if filter_cat in furniture:
            all_furniture_elements.Add(elem.Id)
        if filter_cat == "Ceilings":
            all_ceiling_elements.Add(elem.Id)


#==============================================================================
#  function ckecks if element locates in the room 
#  otherwise checks intersection between geometry representation
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

        else:
            # find intersections
            inter = find_intersection_elemToRoomSolid(elem,room_solid)
            if inter == 1:
                return elem.Id
#==============================================================================
# function finds opening cut in the wall
# returns curve loop
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
#  function finds intersection between element solid and room solid
#  returns 1 if intersection occur
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
                                    return 1
                            except:
                                pass
        elif geomInst.GetType().ToString() == "Autodesk.Revit.DB.Solid":
                if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                    furn_solid = geomInst
                    try:
                        interSolid = BooleanOperationsUtils.ExecuteBooleanOperation(room_solid,furn_solid,BooleanOperationsType.Intersect)
                        if interSolid.Volume > 0.0:
                            return 1
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
    # convert room into solid
    options = SpatialElementBoundaryOptions()
    calculator = SpatialElementGeometryCalculator(doc,options)
    results = calculator.CalculateSpatialElementGeometry(room)
    room_solid = results.GetGeometry()

    # create collection of room containing elements e.g. windows,doors,furniture
    room_elements = List[ElementId]()
    windows_elements = List[ElementId]()
    doors_elements = List[ElementId]()
    furniture_elements = List[ElementId]()
    ceiling_elements = List[ElementId]()

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
            if all_ceiling_elements.Contains(id):
                room_elements.Add(id)
                ceiling_elements.Add(id)

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
                                        'ElementId':elem.Id.IntegerValue,
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
                                    distance = round((line.Project(start_point_an).Distance -width_1/2 - width_2/2)*0.3048,3)
                                    if distance>0.0:
                                        distances.append(distance)
                                        parallel_walls.append(id_temp)
                                else:
                                    distance = round((line.Project(start_point_an).Distance -width_1/2 - width_2/2)*0.3048,3)
                                    if distance>0.0:
                                        distances.append(distance)
                                        parallel_walls.append(id_temp)
                                perpId.append(None)
                                nearest_walls.append(None)
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
            com_dis = [d for d in distances if d != None]    
            if len(com_dis) == 0:
                com_dis = [0] 
            min_dis = round(min(com_dis),3)
            mean_dis =  round(statistics.mean(com_dis),3)
            max_dis =round(max(com_dis),3)
            if min_dis < 0.:
                min_dis = 0.
            if mean_dis < 0.:
                mean_dis = 0.
            if max_dis < 0.:
                max_dis = 0.
            new_row_walls = pd.Series({'Room_Id':room.Id,
                                        'Room_uniqueId':room.UniqueId,
                                        'ElementId': id,
                                        'Element_uniqueId': elem.UniqueId,
                                        'Width': width_1*0.3048,
                                        'Height':height*0.3048,
                                        'Perpendicular_walls_id':perpId,
                                        'Perpendicular_walls_count':len(perpId),
                                        'Parallel_walls_id':parallel_walls,
                                        'Parallel_walls_count':len(parallel_walls),
                                        'Distance_to_parall':distances,
                                        'Distance_to_parall_mi':min_dis,
                                        'Distance_to_parall_mean':mean_dis,
                                        'Distance_to_parall_ma':max_dis,
                                        'Nearest_walls_id':nearest_walls,
                                        'Angles_to_walls':angles,
                                        'Angles_to_walls_mi':min(angles),
                                        'Angles_to_walls_mean':round(statistics.mean(angles),3),
                                        'Angles_to_walls_ma':max(angles)})
            df_walls = pd.concat([df_walls,new_row_walls.to_frame().T],ignore_index= True)
    # 
    # 
    # 
    # 
    #
    # collect constraints from floors: parallelity!, angles?, distance!     
    #
    ceiling_point_list = []
    ceiling_point_dic = {}
    for id in ceiling_elements:
        ceiling = doc.GetElement(id)
        elem_geom = ceiling.get_Geometry(Options())
        for geomInst in elem_geom:
            if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                    ceiling_solid = geomInst
                    for edge in geomInst.Edges:
                        for e in edge.Tessellate():
                            p_z = e.Z
                            if p_z not in ceiling_point_list:
                                ceiling_point_list.append(p_z)
        min_ceiling_p_z = min(ceiling_point_list)
        max_ceiling_p_z = max(ceiling_point_list)
        ceiling_point_dic[id.IntegerValue] = [min_ceiling_p_z,max_ceiling_p_z]

    floors = []
    parallel_floors = []
    roof = []
    room_bb = room.ClosedShell.GetBoundingBox()
    room_bb_min = room_bb.Min
    room_bb_max = room_bb.Max
    df_floors = pd.DataFrame()
    for id in face_dic.keys():
        dir = face_dic[id]
        elem = doc.GetElement(ElementId(id))
        category = elem.Category.Name
        if abs(dir.Z) == 1.0 and ("Floors" in category or "Ceiling" in category):
            parallel_floors.append(id)
            floors.append(id)
        elif abs(dir.Z) > 0.0 :
            roof.append(id)
    
    floor_points_dic = {}                               
    for id in floors:
        floor_point_list = []
        floor = doc.GetElement(ElementId(id))
        elem_geom = floor.get_Geometry(Options())
        for geomInst in elem_geom:
            if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                    floor_solid = geomInst
                    for edge in geomInst.Edges:
                        for e in edge.Tessellate():
                            p_z = e.Z
                            if p_z not in floor_point_list:
                                floor_point_list.append(p_z)
        min_floor_point_z = min(floor_point_list)
        max_floor_point_z = max(floor_point_list)
        floor_points_dic[id] = [min_floor_point_z,max_floor_point_z]

    for id in floor_points_dic.keys():
        paral_floors_new = []
        roof_new = []
        distance_par_list = []
        distance_nonpar_list = []
        floor = doc.GetElement(ElementId(id))
        min_val_floor = floor_points_dic[id][0]
        max_val_floor = floor_points_dic[id][1]
        for id_c in ceiling_point_dic.keys():
            min_val_ceiling = ceiling_point_dic[id_c][0]
            max_val_ceiling  = ceiling_point_dic[id_c][1]
            dis_1 = abs(min_val_floor-max_val_ceiling)
            dis_2 = abs(max_val_floor-min_val_ceiling)
            if id in parallel_floors:
                paral_floors_new.append(id_c)
                if dis_1 > dis_2:
                    distance_par = round(dis_2*0.3048,3)
                    distance_par_list.append(distance_par)
                else:
                    distance_par = round(dis_1*0.3048,3)
                    distance_par_list.append(distance_par)
            if id in roof:
                roof_new.append(id_c)
                if dis_1 > dis_2:
                    distance_nonpar = round(dis_2*0.3048,3)
                    distance_nonpar_list.append(distance_nonpar)
                else:
                    distance_nonpar = round(dis_1*0.3048,3)
                    distance_nonpar_list.append(distance_nonpar)
        for id_f in floor_points_dic.keys():
            min_val_floor_f = floor_points_dic[id_f][0]
            max_val_floor_f = floor_points_dic[id_f][1]
            dis_1 = abs(min_val_floor-max_val_floor_f)
            dis_2 = abs(max_val_floor-min_val_floor_f)
            if id != id_f:
                if id in parallel_floors and id_f in parallel_floors:
                    paral_floors_new.append(id_f)
                    if dis_1 > dis_2:
                        distance_par = round(dis_2*0.3048,3)
                        distance_par_list.append(distance_par)
                    else:
                        distance_par = round(dis_1*0.3048,3)
                        distance_par_list.append(distance_par)
                if id in roof or id_f in roof:
                    roof_new.append(id_f)
                    if dis_1 > dis_2:
                        distance_nonpar = round(dis_2*0.3048,3)
                        distance_nonpar_list.append(distance_nonpar)
                    else:
                        distance_nonpar = round(dis_1*0.3048,3)
                        distance_nonpar_list.append(distance_nonpar)
        new_row_floors = pd.Series({'Room_Id':room.Id,
                                        'Room_uniqueId':room.UniqueId,
                                        'ElementId': id,
                                        'Element_uniqueId': floor.UniqueId,
                                        'Parallel_floor_id':paral_floors_new,
                                        'Nonparallel_floor_id': roof_new,
                                        'Distance_to_parallel':distance_par_list,
                                        'Distance_to_nonparallel':distance_nonpar_list})
        df_floors = pd.concat([df_floors,new_row_floors.to_frame().T],ignore_index= True)

    

    # df_floors = pd.DataFrame()
    # resultArray = IntersectionResultArray()
    # floor_distance = {}
    # dis_to_m = []
    # dir_t = 0
    # id_t = None

    # for id in floors:
    #     if len(floors) <3:
    #         # room has only top and bottom floor
    #         floor = doc.GetElement(ElementId(id))
    #         room_bb = room.ClosedShell.GetBoundingBox()
    #         room_bb_min = room_bb.Min
    #         room_bb_max = room_bb.Max
    #         # floor_distance[id] = dis
    #         new_par = None
    #         paral_count = 0
    #         dis_par = 0
    #         dis_op = 0
    #         roof_id = None
    #         for id_n in parallel_floors:
    #             if id_n != id and id not in roof:
    #                 new_par = id_n
    #                 paral_count = 1
    #                 dis_par = round(abs(room_bb_max.Z-room_bb_min.Z)*0.3048,3)
    #         for id_n in roof:
    #             if id_n != id:
    #                 roof_id = id_n
    #                 dis_op = round(abs(room_bb_max.Z-room_bb_min.Z)*0.3048,3)
    #         new_row_floors = pd.Series({'Room_Id':room.Id,
    #                                     'Room_uniqueId':room.UniqueId,
    #                                     'ElementId': id,
    #                                     'Element_uniqueId': floor.UniqueId,
    #                                     'Parallel_floor_id':[new_par],
    #                                     'Parallel_floors_count':paral_count,
    #                                     'Nonparallel_floor_id': [roof_id],
    #                                     'Distance_to_nonparallel':[dis_op],
    #                                     'Distance_to_parallel':[dis_par]})
    #         df_floors = pd.concat([df_floors,new_row_floors.to_frame().T],ignore_index= True)
    #     else:
    #         # room has additional ceiling or floor
    #         elem = doc.GetElement(ElementId(id))
    #         elem_geom = elem.get_Geometry(Options())
    #         for geomInst in elem_geom:
    #             if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
    #                     floor_solid = geomInst
    #                     for face in floor_solid.Faces:
    #                         normal = face.ComputeNormal(UV(room_location.X,room_location.Y))
    #                         if abs(normal.Z)==1.0 and face != None:
    #                             try:
    #                                 dis = face.Project(room_location).Distance
    #                                 floor_distance[id] = [normal.Z,dis]
    #                                 break
    #                             except:
    #                                 pass

    # for id in floor_distance.keys():
    #     val = floor_distance[id]
    #     dir = val[0]
    #     dis_to_room = val[1]
    #     floor = doc.GetElement(ElementId(id))
    #     paral_count = 0
    #     distance = 0
    #     new_par = []
    #     distance_to_parallel = []
    #     for id_t in floor_distance.keys():
    #         if id_t != id and id not in roof and id_t not in roof and id_t in parallel_floors and id in parallel_floors:
    #             paral_count = paral_count + 1
    #             val_t = floor_distance[id_t]
    #             dir_t = val_t[0]
    #             dis_to_room_t = val_t[1]
    #             new_par.append(id_t)
    #             if dir != dir_t:
    #                 distance = dis_to_room + dis_to_room_t
    #                 distance_to_parallel.append(round(distance*0.3048,3))
    #             else:
    #                 distance = abs(dis_to_room - dis_to_room_t)
    #                 distance_to_parallel.append(round(distance*0.3048,3))

    #     new_row_floors = pd.Series({'Room_Id':room.Id,
    #                                     'Room_uniqueId':room.UniqueId,
    #                                     'ElementId': id,
    #                                     'Element_uniqueId': floor.UniqueId,
    #                                     'Parallel_floor_id':new_par,
    #                                     'Parallel_floors_count':paral_count,
    #                                     'Nonparallel_floor_id': [None],
    #                                     'Distance_to_nonparallel':[0],
    #                                     'Distance_to_parallel': distance_to_parallel})
    #     df_floors = pd.concat([df_floors,new_row_floors.to_frame().T],ignore_index= True)
    # 
    # 
    # 
    # 
    #
    # collect constraints from doors: distance to edges (floor, wall), width, hight
    df_doors = pd.DataFrame()
    doors_wh = {}
    distance_dic = {}
    door_edge_dic = {}
    wall_door = {}
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
        except:
            cut_loop = get_opening_cut(door,wall,dir,room)
            pass
        if wall.Id.IntegerValue in wall_door.keys():
            wall_door[wall.Id.IntegerValue].append(id.IntegerValue)
        else:
            wall_door[wall.Id.IntegerValue] = [id.IntegerValue]
        perp_elem = perpId_dic[id_wall.IntegerValue]
        closest_dis = []
        distance_ids = []
        distance_vert_ids = []
        distance_hor_ids = []
        closest_dis_hor = []
        closest_dis_vert = []
        door_loc = door.Location.Point
        for id_el in perp_elem:
            if id_el != None:
                elem = doc.GetElement(ElementId(id_el))
                if cut_loop != None:
                    for curve in cut_loop:
                        if str(curve.GetType()) == 'Autodesk.Revit.DB.CurveLoop':
                            len_vert = 0.
                            cur_vert = None
                            len_hor = 0.
                            cur_hor = None
                            for cur in curve:
                                len_cur = cur.Length*0.3048
                                dir_c = Line.CreateBound(cur.GetEndPoint(0),cur.GetEndPoint(1)).Direction
                                if abs(dir_c.Z) == 1.0:
                                    len_cur = cur.Length*0.3048
                                    if len_cur > len_vert:
                                        len_vert = len_cur
                                        cur_vert = cur
                                else:
                                    len_cur = cur.Length*0.3048
                                    if len_cur > len_hor:
                                        len_hor = len_cur
                                        cur_hor = cur
                            cut_loop = [cur_hor,cur_vert,cur_hor,cur_vert]
                    for curve in cut_loop:         
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
                                    dis_to_cut = round(first_point.DistanceTo(second_point)*0.3048 - width_p/2*0.3048,3)
                                    if dis_to_cut not in closest_dis_hor:
                                        closest_dis_hor.append(dis_to_cut)
                                        distance_hor_ids.append(id_el)

                        for id_f in floor_points_dic.keys():
                            dist_1 = round(abs(curve.GetEndPoint(0).Z - floor_points_dic[id_f][0])*0.3048,3)
                            dist_2 = round(abs(curve.GetEndPoint(0).Z - floor_points_dic[id_f][1])*0.3048,3)
                            if dist_1>dist_2:
                                if dist_2 not in closest_dis_vert and dist_2 != 0.0:
                                    closest_dis_vert.append(dist_2)
                                    distance_vert_ids.append(id_f)
                            if dist_2>dist_1:
                                if dist_1 not in closest_dis_vert and dist_1 != 0.0:
                                    closest_dis_vert.append(dist_1)
                                    distance_vert_ids.append(id_f)
                        for id_c in ceiling_point_dic.keys():
                            dist_1 = round(abs(curve.GetEndPoint(0).Z - ceiling_point_dic[id_c][0])*0.3048,3)
                            dist_2 = round(abs(curve.GetEndPoint(0).Z - ceiling_point_dic[id_c][1])*0.3048,3)
                            if dist_1>dist_2:
                                if dist_2 not in closest_dis_vert and dist_2 != 0.0:
                                    closest_dis_vert.append(dist_2)
                                    distance_vert_ids.append(id_c)
                            if dist_2>dist_1:
                                if dist_1 not in closest_dis_vert and dist_1 != 0.0:
                                    closest_dis_vert.append(dist_1)
                                    distance_vert_ids.append(id_c)
        distance_dic[id] = closest_dis
        dType = doc.GetElement(door.GetTypeId())
        width = dType.get_Parameter(BuiltInParameter.DOOR_WIDTH).AsDouble() 
        height = dType.get_Parameter(BuiltInParameter.DOOR_HEIGHT).AsDouble()
        l_edge = XYZ(door_loc.X + width/2,door_loc.Y,room_location.Z)
        r_edge = XYZ(door_loc.X - width/2,door_loc.Y,room_location.Z)
        door_edge_dic[id.IntegerValue] = [l_edge,r_edge]
        doors_wh[id] = [width,height]
        com_dis = distance_dic[id]
        if len(com_dis) == 0:
            com_dis = [0]
        if len(closest_dis_hor) == 0:
            closest_dis_hor = [0]
        if len(closest_dis_vert) == 0:
            closest_dis_vert = [0]
        new_row_doors = pd.Series({'Room_Id':room.Id,
                                    'Room_uniqueId':room.UniqueId,
                                    'ElementId': id.IntegerValue,
                                    'Element_uniqueId': door.UniqueId,
                                    'Door_width':round(width*0.3048,3),
                                    'Door_height':round(height*0.3048,3),
                                    #'Nearest_elementIds':distance_ids,
                                    # 'Distance_to_edges':distance_dic[id],
                                    'ElementId_hor':distance_hor_ids,
                                    'ElementId_vert': distance_vert_ids,
                                    'Distance_to_edges_hor': closest_dis_hor,
                                    'Distance_to_edges_vert': closest_dis_vert,
                                    'Distance_to_edges_hor_mi': min(closest_dis_hor),
                                    'Distance_to_edges_hor_mean': round(statistics.mean(closest_dis_hor),3),
                                    'Distance_to_edges_hor_ma': max(closest_dis_hor),
                                    'Distance_to_edges_vert_mi': min(closest_dis_vert),
                                    'Distance_to_edges_vert_mean': round(statistics.mean(closest_dis_vert),3),
                                    'Distance_to_edges_vert_ma': max(closest_dis_vert),
                                    # 'Distance_to_edges_mi':min(com_dis),
                                    # 'Distance_to_edges_mean':round(statistics.mean(com_dis),3),
                                    #'Distance_to_edges_ma':max(com_dis),
                                    'ElementId_next_door':[],
                                    'Distance_to_next_door_min': []})
        df_doors = pd.concat([df_doors,new_row_doors.to_frame().T],ignore_index= True) 
    for wall,doors in wall_door.items():
        for d in doors:
            l_edge = door_edge_dic[d][0]
            r_edge = door_edge_dic[d][1]
            distance = 0.
            id_next = None
            for d_t in doors:
                if d != d_t:
                    l_edge_t = door_edge_dic[d_t][0]
                    r_edge_t = door_edge_dic[d_t][1]
                    dis_1 = l_edge.DistanceTo(r_edge_t)
                    dis_2 = r_edge.DistanceTo(l_edge_t)
                    dis = round(min(dis_1,dis_2),3)
                    if distance == 0.:
                        distance = dis
                        id_next = d_t
                    if distance > dis:
                        distance = dis
                        id_next = d_t
            df_doors.loc[df_doors['ElementId'] == d,['ElementId_next_door']]= id_next
            df_doors.loc[df_doors['ElementId'] == d,['Distance_to_next_door_min']] = round(distance*0.3048,3)                                           
    # 
    # 
    # 
    # 
    #
    #collect constraints from windows: distance to edges (floor, wall), width, hight
    df_windows = pd.DataFrame()
    distance_dic = {}
    wall_win = {}
    win_edge_dic = {}
    for id in windows_elements:
        window = doc.GetElement(id)
        if str(window.Host.GetType()) == 'Autodesk.Revit.DB.ExtrusionRoof':
            continue
        window_loc = window.Location.Point
        wall = window.Host
        if wall.Id.IntegerValue in wall_win.keys():
            wall_win[wall.Id.IntegerValue].append(id.IntegerValue)
        else:
            wall_win[wall.Id.IntegerValue] = [id.IntegerValue]
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
        closest_dis_hor = []
        closest_dis_vert = []
        distance_vert_ids = []
        distance_hor_ids = []
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
                                    dis_to_cut = round(first_point.DistanceTo(second_point)*0.3048 - width_p/2*0.3048,3)
                                    if dis_to_cut not in closest_dis_hor:
                                        distance_hor_ids.append(id_el)
                                        closest_dis_hor.append(dis_to_cut)

                        # if abs(dir_c.Z) == 0.0:
                        #     if face_dic[id_el].Z == 1.0:
                        #         proj_pnt = curve.GetEndPoint(0)
                        #         elem_geom = elem.get_Geometry(Options())
                        #         dis = 1
                        #         temp_dist = []
                        #         for geomInst in elem_geom:
                        #             if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                        #                     floor_solid = geomInst
                        #                     for face in floor_solid.Faces:
                        #                         if dis != 0:
                        #                             normal = face.ComputeNormal(UV(proj_pnt.X,proj_pnt.Y))
                        #                             if normal.Z==-1.0:
                        #                                 dis = round(face.Project(proj_pnt).Distance*0.3084,3)
                        #                                 temp_dist.append(dis)
                        #         min_dis = min(temp_dist)
                        #         distance_vert_ids.append(id_el)
                        #         closest_dis_vert.append(dis)
                                # if dis_to_cut not in distance_ids:
                                #     distance_ids.append(id_el)
                                #     closest_dis.append(dis)
                                #     distance_vert_ids.append(id_el)
                                #     closest_dis_vert.append(round(dis,3))

                            # elif face_dic[id_el].Z == -1.0:
                            #     proj_pnt = curve.GetEndPoint(0)
                            #     elem_geom = elem.get_Geometry(Options())
                            #     dis = 1
                            #     temp_dist = []
                            #     for geomInst in elem_geom:
                            #         if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                            #                 floor_solid = geomInst
                            #                 for face in floor_solid.Faces:
                            #                     if dis != 0:
                            #                         normal = face.ComputeNormal(UV(proj_pnt.X,proj_pnt.Y))
                            #                         if normal.Z==1.0:
                            #                             dis = round(face.Project(proj_pnt).Distance*0.3084,3)
                            #                             temp_dist.append(dis)
                            #     min_dis = min(temp_dist)
                            #     closest_dis_vert.append(dis)
                            #     distance_vert_ids.append(id_el)
                            #     # if id_el not in distance_ids:
                            #     #     distance_ids.append(id_el)
                            #     #     closest_dis.append(dis)
                            #     #     closest_dis_vert.append(round(dis,3))
                            #     #     distance_vert_ids.append(id_el)
                        for id_f in floor_points_dic.keys():
                            dist_1 = round(abs(curve.GetEndPoint(0).Z - floor_points_dic[id_f][0])*0.3048,3)
                            dist_2 = round(abs(curve.GetEndPoint(0).Z - floor_points_dic[id_f][1])*0.3048,3)
                            if dist_1>dist_2:
                                if dist_2 not in closest_dis_vert:
                                    closest_dis_vert.append(dist_2)
                                    distance_vert_ids.append(id_f)
                            if dist_2>dist_1:
                                if dist_1 not in closest_dis_vert:
                                    closest_dis_vert.append(dist_1)
                                    distance_vert_ids.append(id_f)
                        for id_c in ceiling_point_dic.keys():
                            dist_1 = round(abs(curve.GetEndPoint(0).Z - ceiling_point_dic[id_c][0])*0.3048,3)
                            dist_2 = round(abs(curve.GetEndPoint(0).Z - ceiling_point_dic[id_c][1])*0.3048,3)
                            if dist_1>dist_2:
                                if dist_2 not in closest_dis_vert:
                                    closest_dis_vert.append(dist_2)
                                    distance_vert_ids.append(id_c)
                            if dist_2>dist_1:
                                if dist_1 not in closest_dis_vert:
                                    closest_dis_vert.append(dist_1)
                                    distance_vert_ids.append(id_c)
        distance_dic[id.IntegerValue] = closest_dis
        wType = doc.GetElement(window.GetTypeId())
        w = min(dim_arr)
        l_edge = XYZ(window_loc.X + w/2,window_loc.Y,room_location.Z)
        r_edge = XYZ(window_loc.X - w/2,window_loc.Y,room_location.Z)
        win_edge_dic[id.IntegerValue] = [l_edge,r_edge]
        # com_dis = distance_dic[id.IntegerValue]
        if len(closest_dis_hor) == 0:
            closest_dis_hor = [0]
        if len(closest_dis_vert) == 0:
            closest_dis_vert = [0]
        new_row_windows = pd.Series({'Room_Id':room.Id,
                                        'Room_uniqueId':room.UniqueId,
                                        'ElementId': id.IntegerValue,
                                        'Element_uniqueId': window.UniqueId,
                                        'Window_width':round(min(dim_arr)*0.3048,3),
                                        'Window_height':round(max(dim_arr)*0.3048,3),
                                        #'Nearest_elementIds':distance_ids,
                                        # 'Distance_to_edges':distance_dic[id.IntegerValue],
                                        'ElementId_vert': distance_vert_ids,
                                        'ElementId_hor':distance_hor_ids,
                                        'Distance_to_edges_hor':closest_dis_hor,
                                        'Distance_to_edges_vert':closest_dis_vert,
                                        'Distance_to_edges_hor_mi': min(closest_dis_hor),
                                        'Distance_to_edges_hor_mean': round(statistics.mean(closest_dis_hor),3),
                                        'Distance_to_edges_hor_ma': max(closest_dis_hor),
                                        'Distance_to_edges_vert_mi': min(closest_dis_vert),
                                        'Distance_to_edges_vert_mean': round(statistics.mean(closest_dis_vert),3),
                                        'Distance_to_edges_vert_ma': max(closest_dis_vert),
                                        'ElementId_next_win':[],
                                        'Distance_to_next_win_min': []})
        df_windows = pd.concat([df_windows,new_row_windows.to_frame().T],ignore_index= True)
    for wall,wins in wall_win.items():
        for w in wins:
            l_edge = win_edge_dic[w][0]
            r_edge = win_edge_dic[w][1]
            distance = 0.
            id_next = None
            for w_t in wins:
                if w != w_t:
                    l_edge_t = win_edge_dic[w_t][0]
                    r_edge_t = win_edge_dic[w_t][1]
                    dis_1 = l_edge.DistanceTo(r_edge_t)
                    dis_2 = r_edge.DistanceTo(l_edge_t)

                    dis = min(dis_1,dis_2)
                    if distance == 0.:
                        distance = dis
                        id_next = w_t
                    if distance > dis:
                        distance = dis
                        id_next = w_t
            df_windows.loc[df_windows['ElementId'] == w,['ElementId_next_win']]= id_next
            df_windows.loc[df_windows['ElementId'] == w,['Distance_to_next_win_min']] = round(distance*0.3048,3)
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
                    dist = round(wall_point.DistanceTo(loc_furn_new)*0.3048,3)
                    closest_dis.append(dist)
                    distance_ids.append(b_el.IntegerValue)
                if location_type == "Autodesk.Revit.DB.LocationCurve":
                    wall_curve = wall_loc.Curve
                    wall_w = wall.Width
                    loc_furn_new = XYZ(loc_furn.X,loc_furn.Y,wall_curve.GetEndPoint(0).Z)
                    dist = round(wall_curve.Project(loc_furn_new).Distance*0.3048 - wall_w/2*0.3048,3)
                    closest_dis.append(dist)
                    distance_ids.append(b_el.IntegerValue)
            if dir.Z == 1.0:
                # floors
                for id_f in floor_points_dic.keys():
                    distance_ids.append(id_f)
                    dist_1 = abs(loc_furn.Z - floor_points_dic[id_f][0])
                    dist_2 = abs(loc_furn.Z - floor_points_dic[id_f][1])
                    if dist_1>dist_2:
                        closest_dis.append(round(dist_2*0.3028,3))
                    if dist_2>dist_1:
                        closest_dis.append(round(dist_1*0.3028,3))
        for id_c in ceiling_point_dic.keys():
            distance_ids.append(id_c)
            dist_1 = abs(loc_furn.Z - ceiling_point_dic[id_c][0])
            dist_2 = abs(loc_furn.Z - ceiling_point_dic[id_c][1])
            if dist_1>dist_2:
                closest_dis.append(round(dist_2*0.3028,3))
            if dist_2>dist_1:
                closest_dis.append(round(dist_1*0.3028,3))

        distance_dic[id] = closest_dis
        com_dis = distance_dic[id]
        if len(com_dis) == 0:
            com_dis = [0]
        min_com_dis = min(com_dis)
        if min_com_dis < 0.:
            min_com_dis = 0.
        new_row_furn = pd.Series({'Room_Id':room.Id,
                                    'Room_uniqueId':room.UniqueId,
                                    'ElementId': id,
                                    'Element_uniqueId': furn.UniqueId,
                                    'Nearest_elementIds':distance_ids,
                                    'Nearest_elementIds_count':len(distance_ids),
                                    'Distance_to_nearest':distance_dic[id],
                                    'Distance_to_nearest_mi': min_com_dis,
                                    'Distance_to_nearest_mean': round(statistics.mean(com_dis),3),
                                    'Distance_to_nearest_ma': max(com_dis)})
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
                             'ElementId': elem.Id.IntegerValue,
                             'Element_uniqueId': elem.UniqueId,
                             'Family':fam_name,
                             'Typ':elem.Name,
                             'Category':elem.Category.Name})
        df = pd.concat([df,new_row.to_frame().T],ignore_index= True)


    #add individual data to general data frame
    df_bound_all = pd.concat([df_bound_all,df_bound],ignore_index=True)
    df_walls_all = pd.concat([df_walls_all,df_walls],ignore_index=True)
    df_floors_all = pd.concat([df_floors_all,df_floors],ignore_index=True)
    df_windows_all = pd.concat([df_windows_all,df_windows],ignore_index=True)
    df_doors_all = pd.concat([df_doors_all,df_doors],ignore_index=True)
    df_furn_dist_all = pd.concat([df_furn_dist_all,df_furn_dist],ignore_index=True)
    df_all = pd.concat([df_all,df],ignore_index=True)

# print all data frames
nameOfFile_csv = 'data\\tables\\room_elements_bounds.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_bound_all.to_csv(completename_csv)

nameOfFile_csv = 'data\\tables\\room_elements_walls.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_walls_all.to_csv(completename_csv)

nameOfFile_csv = 'data\\tables\\room_elements_floors.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_floors_all.to_csv(completename_csv)

nameOfFile_csv = 'data\\tables\\room_elements_doors.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_doors_all.to_csv(completename_csv) 

nameOfFile_csv = 'data\\tables\\room_elements_windows.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_windows_all.to_csv(completename_csv) 

nameOfFile_csv = 'data\\tables\\room_elements_furniture.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_furn_dist_all.to_csv(completename_csv)

nameOfFile = 'data\\tables\\room_elements.xlsx'
nameOfFile_csv = 'data\\tables\\room_elements.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_all.to_csv(completename_csv)

# experimental solution
# win_nearest_dim = df_windows_all.agg({'Distance_to_next_win_min':['mean','min','max']})
# # apply min = 0.5

# df_windows_all = df_windows_all[df_windows_all['Distance_to_next_win_min']> 0.]
# min_val = df_windows_all['Distance_to_next_win_min'].min()
# print(min_val)
# df_windows_all.loc[df_windows_all['Distance_to_next_win_min'] == min_val,['Distance_to_next_win_min']] = 0.5
# win_id = df_windows_all.loc[df_windows_all['Distance_to_next_win_min'] == 0.5,'ElementId']
# print(win_id.values)
# dif = abs(min_val- 0.5)*3.28084
# # transl = XYZ(0.,dif,0.)
# # w = win_id.values[0]
# # print(w)
# # win = doc.GetElement(ElementId(w))
# # loc = win.Location
# # loc.Move(transl)
# # id_prev = None
# for w in win_id:
#     win = doc.GetElement(ElementId(w))
#     loc = win.Location
#     loc_p = loc.Point
#     # loc.Move(transl)
#     id_prev = w
#     near = df_windows_all.loc[df_windows_all['ElementId'] == w,'ElementId_next_win'].values
#     win_near = doc.GetElement(ElementId(near))
#     loc_near = win_near.Location
#     loc_near_p = loc_near.Point
#     normal_to_near = XYZ(loc_near_p.X-loc_p.X,loc_near_p.Y-loc_p.Y,loc_p.Z).Normalize()
#     move_vec = normal_to_near.Multiply(dif)
#     loc.Move(move_vec)
#     if near == id_prev:
#         continue
# df_sum = pd.DataFrame()
# print('####### ROOM REPORT ######')
# print(df['Category'].value_counts())
# print("Number of doors:" + str(df_doors.shape[0]))
# print(df_doors.agg({'Door_width':['mean','min','max'],'Door_height':['mean','min','max']}))
# print("Number of floors:" + str(df_floors.shape[0]))
# print(df_floors.agg({'Distance_to_parall':['count','mean','min','max']}))
# t.Commit()