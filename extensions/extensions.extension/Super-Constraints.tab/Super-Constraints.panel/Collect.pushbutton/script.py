#! python3
import clr
clr.AddReference("System")
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
import numpy as np
import pandas as pd
import os.path

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from System.Windows.Forms import FolderBrowserDialog
from System.Collections.Generic import List

from openpyxl.workbook import Workbook

global doc

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

t = Transaction(doc, "Get all elements from links")
t.Start()

# pic room object
choise = uidoc.Selection
pickedElement = choise.PickObject(ObjectType.Element, "Select room")
selectedElement = doc.GetElement(pickedElement.ElementId)
print(selectedElement.GetType().ToString())
if selectedElement.GetType().ToString() != "Autodesk.Revit.DB.Architecture.Room":
    print("Wrong element selected. Operation breaks.")
    t.Commit()

#empty database
df = pd.DataFrame()
data_cat = pd.read_excel('D:/Bachelor_thesis/super-constraints/extensions/extensions.extension/Super-Constraints.tab/Super-Constraints.panel/Collect.pushbutton/Revit-Categories-2022_arc.xlsx')
df_cat = pd.DataFrame(data_cat)
df_cat = df_cat.loc[df_cat['Support'] == "Yes"]
df_fur = df_cat.loc[df_cat['Furniture'] == "Yes"]

# collector_2 = FilteredElementCollector(doc)
# # collector_2.OfClass(FamilyInstance)
# collector_2.WherePasses(ElementIntersectsSolidFilter(room_solid))
# furniture_elements = List[ElementId]()

def get_roomSolid(room):
    calculator = SpatialElementGeometryCalculator(doc)
    results = calculator.CalculateSpatialElementGeometry(selectedElement)
    room_solid = results.GetGeometry()
    return room_solid

def find_room_from_elem_location(elem,room):
    location = elem.Location
    location_type = location.GetType().ToString()
    room_solid = get_roomSolid(room)
    if location_type == "LocationPoint":
        # point location
        loc_point = location.Point
        room_elem = doc.GetRoomAtPoint(loc_point)
        if room_elem != None:
            # cannot find room for columns
            if room.Id.Equals(selectedElement.Id):
                return elem.Id
        else:
            inter = find_intersection_elemToRoomSolid(elem,room_solid)
            if inter:
                return elem.Id
    elif location_type == "LocationCurve":
        # curve location
        loc_curve = location.Curve
        if room_solid.IntersectWithCurve(curve,SolidCurveIntersectionOptions()) != None:
            return elem.Id
        else:
            inter = find_intersection_elemToRoomSolid(elem,room_solid)
            if inter:
                return elem.Id
    else:
        # find intersections
        inter = find_intersection_elemToRoomSolid(elem,room_solid)
        if inter:
            return elem.Id
    
def find_intersection_elemToRoomSolid(elem, room_solid):
    elem_geom = elem.get_Geometry(Options())
    inter = 0
    for geomInst in elem_geom:
        print(geomInst.GetType().ToString())
        if geomInst.GetType().ToString() != "Autodesk.Revit.DB.Solid" and inter == 0:
            for instObj in geomInst.SymbolGeometry:
                if instObj.GetType().ToString() == "Autodesk.Revit.DB.Solid":
                    if instObj.Faces.Size != 0 and instObj.Edges.Size != 0:
                        furn_solid = instObj
                        interSolid = BooleanOperationsUtils.ExecuteBooleanOperation(room_solid,furn_solid,BooleanOperationsType.Intersect)
                        print(interSolid.Volume)
                        if interSolid.Volume > 0.0:
                            inter = 1  
                            print(interSolid.Volume)
                            return 1
        elif geomInst.GetType().ToString() == "Autodesk.Revit.DB.Solid" and inter == 0:
            if geomInst.Faces.Size != 0 and geomInst.Edges.Size != 0:
                furn_solid = geomInst
                interSolid = BooleanOperationsUtils.ExecuteBooleanOperation(room_solid,furn_solid,BooleanOperationsType.Intersect)
                if interSolid.Volume > 0.0:
                    inter = 1  
                    return 1


# collect all bounding elements of the room: walls and floors
sel_location = selectedElement.Location.Point
calculator = SpatialElementGeometryCalculator(doc)
results = calculator.CalculateSpatialElementGeometry(selectedElement)
room_solid = results.GetGeometry()
face_dic = {}
bounds_elem = List[ElementId]()
added_elements = List[ElementId]()
furniture_elements = List[ElementId]()
for face in room_solid.Faces:
    face_list = results.GetBoundaryFaceInfo(face)
    for f in face_list:
        link_elem = f.SpatialBoundaryElement
        try:
            link_elem_Id = link_elem.HostElementId
        except:
            link_elem_Id = link_elem.LinkedElementId
        elem = doc.GetElement(link_elem_Id)
        if not added_elements.Contains(elem.Id) and not bounds_elem.Contains(elem.Id):
            added_elements.Add(elem.Id)
            bounds_elem.Add(elem.Id)
            face_dic[elem.Id.IntegerValue] = f.GetSubface().ComputeNormal(UV(sel_location.X,sel_location.Y))

# ellements collector
boundingBox = selectedElement.ClosedShell.GetBoundingBox()
offset = 0.164042 # 0.05 m
boundingBox.Min = XYZ(boundingBox.Min.X- offset, boundingBox.Min.Y- offset, boundingBox.Min.Z)
boundingBox.Max = XYZ(boundingBox.Max.X + offset, boundingBox.Max.Y + offset, boundingBox.Max.Z)

outline = Outline(boundingBox.Min,boundingBox.Max)
collection = FilteredElementCollector(doc).WherePasses(BoundingBoxIntersectsFilter(outline))
elements = collection.ToElements()  

for elem in elements:
    try:
        filter_cat = elem.Category.Name
    except:
        filter_cat = None
    if df_cat['Support'][(df_cat['English'] == filter_cat)].any() and not added_elements.Contains(elem.Id):
        location = elem.Location
        # print(elem.Category.Name)
        # write function to find Location
        # try:
        #     point = location.Point
        #     room = doc.GetRoomAtPoint(point)
        #     if room != None:
        #         # cannot find room for columns
        #         roomId = room.Id
        #         if room.Id.Equals(selectedElement.Id):
        #             added_elements.Add(elem.Id)
        # except:
        #     pass
        # try:
        #     curve = location.Curve
        #     print(elem.Category.Name)
        #     if room_solid.IntersectWithCurve(curve,SolidCurveIntersectionOptions()) != None:
        #         added_elements.Add(elem.Id)
        # except:
        #     pass
        # try:
        #     location = elem.get_Location()
        #     print(elem.Category.Name)
        #     print(type(location))
        # except:
        #     pass
        
        elemId = find_room_from_elem_location(elem,selectedElement)

        if elemId != None:
            added_elements.Add(elemId)

    #     if filter_cat == "Doors" or filter_cat == "Windows":
    #         room = elem.FromRoom
    #         if room != None:
    #             roomId = room.Id
    #             if room.Id.Equals(selectedElement.Id):
    #                     added_elements.Add(elem.Id)

    #     # if filter_cat == "Plumbing Fixtures":
    #     #     added_elements.Add(elem.Id)

    if df_fur['Furniture'][(df_cat['English'] == filter_cat)].any() and not added_elements.Contains(elem.Id):
        inter = find_intersection_elemToRoomSolid(elem,room_solid)
        print(inter)
        if inter:
            furniture_elements.Add(elem.Id)
            added_elements.Add(elem.Id)

        # furn_geom = elem.get_Geometry(Options())
        # print("Furniture")
        # inter = 0
        # for f_g in furn_geom:
        #     if f_g != None and inter == 0:
        #         for instObj in f_g.SymbolGeometry:
        #             if instObj.GetType().ToString() == "Autodesk.Revit.DB.Solid":
        #                 if instObj.Faces.Size != 0 and instObj.Edges.Size != 0:
        #                     furn_solid = instObj
        #                     interSolid = BooleanOperationsUtils.ExecuteBooleanOperation(room_solid,furn_solid,BooleanOperationsType.Intersect)
        #                     if interSolid.Volume > 0.0:
        #                         inter = 1                   
        # if inter == 1:
        #     furniture_elements.Add(elem.Id)
        #     added_elements.Add(elem.Id)

# collect constraints from the wall: perpendiculary, parallelity, angles, distance           
df_walls = pd.DataFrame()
resultArray = IntersectionResultArray()
for id in face_dic.keys():
    dir = face_dic[id]
    elem = doc.GetElement(ElementId(id))
    if abs(dir.X) == 1 or abs(dir.Y)==1:
        # we mean that is a wall
        loc_curve = elem.get_Location()
        curve = loc_curve.Curve
        start_point = curve.GetEndPoint(0)
        end_point = curve.GetEndPoint(1)
        direction = Line.CreateBound(start_point,end_point).Direction
        line = Line.CreateUnbound(start_point,direction)
        vec_1 = end_point.Subtract(start_point).Normalize()
        width_1 = elem.Width
        perpId = []
        angles = []
        nearest_walls = []
        nearest_angles = []
        distances = []
        parallel_walls = []
        for id_temp in face_dic.keys():
            dir_temp = face_dic[id_temp]
            if id != id_temp and (abs(dir_temp.X) == 1 or abs(dir_temp.Y)==1):
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
                        nearest_walls.append(id_temp)
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
                            distance = round((line.Project(start_point_an).Distance - width_1/2 - width_2/2)*0.3048,3)
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
                            nearest_walls.append(None)
                            parallel_walls.append(None)

        new_row = pd.Series({'ElementId': id,
                            'Perpendicular_walls_id':perpId,
                            'Parallel_walls_id':parallel_walls,
                            'Distance_to_parall':distances,
                            'Nearest_walls_id':nearest_walls,
                            'Angles_to_walls':angles})
        df_walls = pd.concat([df_walls,new_row.to_frame().T],ignore_index= True)
# write walls into dataframe
nameOfFile_csv = 'space_elements_walls.csv'
completename_csv = 'D:/Bachelor_thesis/super-constraints/data/' + nameOfFile_csv
df_walls.to_csv(completename_csv)

# analyse furniture, calculate nearest furniture
df_furn_dist = pd.DataFrame()
i = 0
for id in furniture_elements:
    elem = doc.GetElement(id)
    location_point = elem.Location.Point
    print(elem.Name)
    nearest_elem = []
    distance = []
    nearest_elem_dict = {}
    nearest_elem_dict['ElementId'] = id
    n = 0
    for b_id in bounds_elem:
        b_elem = doc.GetElement(b_id)
        b_geom = b_elem.get_Geometry(Options())
        print(b_elem)
        b_elem_cat = b_elem.Category.Name
        for solid in b_geom:
            for face in solid.Faces:
                projection = face.Project(location_point)
                if projection != None:
                    normal = face.ComputeNormal(UV(location_point.X,location_point.Y))
                    if b_elem_cat == "Floors" and normal.Z == -1.0:
                        # dist_dic[b_id] = projection.Distance
                        nearest_elem_dict['Nearest_elem_id_'f'{n}'] = b_id
                        nearest_elem_dict['Distance_to_nearest_'f'{n}'] = projection.Distance
                        # nearest_elem.append(b_id)
                        # distance.append(projection.Distance)
                        n = n + 1

                    if b_elem_cat == "Walls" and (normal.X == -1.0 or normal.Y == -1.0):
                        # nearest_elem.append(b_id)
                        # distance.append(projection.Distance)
                        nearest_elem_dict['Nearest_elem_id_'f'{n}'] = b_id
                        nearest_elem_dict['Distance_to_nearest_'f'{n}'] = projection.Distance
                        n = n + 1

    new_row = pd.Series(nearest_elem_dict)
    df_furn_dist = pd.concat([df_furn_dist,new_row.to_frame().T],ignore_index= True)
    # b_elements = dist_dic.keys()
    # b_distances = dist_dic.values()
    # print(b_elements)
    # print(b_distances)
    # new_row = pd.Series({'ElementId':id,'Nearest_elem_id':b_elements,'Distance_to_nearest':b_distances})
    # df_furn_dist = pd.concat([df_furn_dist,new_row.to_frame().T],ignore_index= True)

                    # print("Normal: " + str(face.ComputeNormal(UV(location_point.X,location_point.Y))))
                    # print(projection.Distance)
                    #print(projection.XYZPoint)

nameOfFile_csv = 'space_elements_furniture.csv'
completename_csv = 'D:/Bachelor_thesis/super-constraints/data/' + nameOfFile_csv
df_furn_dist.to_csv(completename_csv)


for id in added_elements:
    print(id)
    elem = doc.GetElement(id)
    try:

        dep_el = elem.FindInserts(True,True,True,True)
        for d in dep_el:
            if added_elements.Contains(d):
                # recognise windows and door which belongs to the room
                print("Connections between wall and door/window")
                print(str(id) + ":" + str(d))
    except:
        pass
    # find connections between walls
    # try:
    #     location = elem.Location
    #     elem_join = location.get_ElementsAtJoin(0) #connections on the start point
    #     for e in elem_join:
    #         if added_elements.Contains(e.Id):
    #             print("connections in the beginnig of the wall")
    #             print(str(id) + ":" + str(e.Id))
    # except:
    #     pass
    # # find connections between walls
    # try:
    #     location = elem.Location
    #     elem_join = location.get_ElementsAtJoin(1) #connections on the end point
    #     for e in elem_join:
    #         if added_elements.Contains(e.Id):
    #             print("connections in the end of the wall")
    #             print(str(id) + ":" + str(e.Id))
    #     # after finding adjacent walls check if the walls are perpendicular to each other 
    #     # here find destination curve with Location.Curve.Derivative(add specific point on curve)
    # except:
    #     pass


# write all in dataframe
for id in added_elements:

    elem = doc.GetElement(id)
    try:
            eId = elem.GetTypeId()
            elemType = doc.GetElement(eId)
            if elemType != None:
                fam_name = elemType.FamilyName
    except:
        fam_name = elem.Symbol.Family.Name
    new_row = pd.Series({'Selected_roomI_uniqueId':selectedElement.UniqueId,
                                    'Selected_roomI_Id': selectedElement.Id,
                                    'UniqueId':elem.UniqueId,
                                    'ElementId': elem.Id,
                                    'Family':fam_name,
                                    'Typ':elem.Name,
                                    'Category':elem.Category.Name,
                                    'LevelId': elem.LevelId})
    df = pd.concat([df,new_row.to_frame().T],ignore_index= True)

# df_result = pd.merge(df,df_furn_dist, how = "outer", on = "ElementId")
# print space elements
nameOfFile = 'space_elements.xlsx'
# completeName = 'D:/Bachelor_thesis/super-constraints/data/' + nameOfFile
# with pd.ExcelWriter(completeName) as writer:
#     df_result.to_excel(writer, index = False)

nameOfFile_csv = 'space_elements.csv'
completename_csv = 'D:/Bachelor_thesis/super-constraints/data/' + nameOfFile_csv
df.to_csv(completename_csv)
t.Commit()