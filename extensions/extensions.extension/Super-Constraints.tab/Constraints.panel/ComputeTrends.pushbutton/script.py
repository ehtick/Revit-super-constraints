#! python3
import sys
# for problems with packages once uncommet line below (with correct site-packages directory)
# sys.path.append(r"C:\Users\elyah\AppData\Local\Programs\Python\Python38\Lib\site-packages")
import os
import os.path
import statistics
import numpy as np
import pandas as pd

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from System.Windows.Forms import FolderBrowserDialog
from System.Collections.Generic import List
from Autodesk.Revit.DB.IFC import *

from openpyxl.workbook import Workbook

global doc

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

t = Transaction(doc, "Get all elements in the model")
t.Start()


# filter categories
directory = os.path.dirname(os.path.abspath(__file__))

# data directory for filter categories
data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(directory)))))

# get windows
nameOfFile_csv = 'data\\tables\\room_elements_windows.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_win = pd.read_csv(completename_csv)
df_win_new = pd.DataFrame()

# get doors
nameOfFile_csv = 'data\\tables\\room_elements_doors.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_doors = pd.read_csv(completename_csv)

# get walls
nameOfFile_csv = 'data\\tables\\room_elements_walls.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_walls = pd.read_csv(completename_csv)

# get floors
nameOfFile_csv = 'data\\tables\\room_elements_floors.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_floors = pd.read_csv(completename_csv)

# get furniture
nameOfFile_csv = 'data\\tables\\room_elements_furniture.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_furniture = pd.read_csv(completename_csv)

# get elements
nameOfFile_csv = 'data\\tables\\room_elements.csv'
completename_csv =os.path.join(data_dir,nameOfFile_csv)
df_elements = pd.read_csv(completename_csv)


# WINDOWS
# analyse windows

# nameOfFile_txt = 'data\\tables\\windows_report.txt'
# completename_txt = os.path.join(data_dir,nameOfFile_txt)
# win_file = open(completename_txt,'w+')
# win_file.write("Analyse windows \n")
# win_file.write('1. Analyse all windows (by category:Windows) \n')
# analyse windows all by category - completed
#width and hight
str_wh = df_win.agg({'Window_width':['min','mean','max'],'Window_height':['min','mean','max']}).T.values
mode_win_w = df_win['Window_width'].agg(pd.Series.mode).values[0]
mode_win_h = df_win['Window_height'].agg(pd.Series.mode).values[0]
win_w = list(np.append(str_wh[0],mode_win_w))
win_h = list(np.append(str_wh[1],mode_win_h))
#distance
distance_list_h = []
for item in list(df_win['Distance_to_edges_hor'].values):
    item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
    distance_list_h.extend(item_num)
distance_list_v = []
for item in list(df_win['Distance_to_edges_vert'].values):
    item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
    distance_list_v.extend(item_num)
max_dist_h = np.max(distance_list_h)
max_dist_v = np.max(distance_list_v)
min_dist_h = np.min(distance_list_h)
min_dist_v = np.min(distance_list_v)
mean_dist_h = round(np.mean(distance_list_h),3)
mean_dist_v = round(np.mean(distance_list_v),3)
mode_dist_h = statistics.mode(distance_list_h)
mode_dist_v = statistics.mode(distance_list_v)
str_n_min = df_win['Distance_to_next_win_min'].values
mode_win_n = df_win['Distance_to_next_win_min'].agg(pd.Series.mode).values[0]
min_dist_n = min(str_n_min)
max_dist_n = max(str_n_min)
mean_dist_n = round(statistics.mean(str_n_min),3)
#all
str_1 = pd.Series({'Category': 'Windows','Width':win_w,'Height':win_h,
                    'Distance_to_edges_hor':[min_dist_h,mean_dist_h,max_dist_h,mode_dist_h],
                    'Distance_to_edges_vert':[min_dist_v,mean_dist_v,max_dist_v,mode_dist_v],
                    'Distance_to_next':[min_dist_n,mean_dist_n,max_dist_n,mode_win_n]})
#win_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
df_win_new_cat = pd.concat([df_win_new,str_1.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\windows_report_category.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_win_new_cat.to_csv(completename_csv,index=False)

# analyse by room names - completed
#win_file.write('2. Analyse all windows by room names \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_win_new_roomname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_win_sorted = df_win.loc[df_win['Element_uniqueId'].isin(uniqueid)]
    if len(df_win_sorted)>0:
        #width and hight
        str_wh = df_win_sorted.agg({'Window_width':['min','mean','max'],'Window_height':['min','mean','max']}).T.values
        mode_win_w = df_win_sorted['Window_width'].agg(pd.Series.mode).values[0]
        mode_win_h = df_win_sorted['Window_height'].agg(pd.Series.mode).values[0]
        win_w = list(np.append(str_wh[0],mode_win_w))
        win_h = list(np.append(str_wh[1],mode_win_h))
        #distance
        distance_list_h = []
        for item in list(df_win_sorted['Distance_to_edges_hor'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            distance_list_h.extend(item_num)
        distance_list_v = []
        for item in list(df_win_sorted['Distance_to_edges_vert'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            distance_list_v.extend(item_num)
        max_dist_h = np.max(distance_list_h)
        max_dist_v = np.max(distance_list_v)
        min_dist_h = np.min(distance_list_h)
        min_dist_v = np.min(distance_list_v)
        mean_dist_h = round(np.mean(distance_list_h),3)
        mean_dist_v = round(np.mean(distance_list_v),3)
        mode_dist_h = statistics.mode(distance_list_h)
        mode_dist_v = statistics.mode(distance_list_v)
        str_n_min = df_win_sorted['Distance_to_next_win_min'].values
        mode_win_n = df_win_sorted['Distance_to_next_win_min'].agg(pd.Series.mode).values[0]
        min_dist_n = min(str_n_min)
        max_dist_n = max(str_n_min)
        mean_dist_n = round(statistics.mean(str_n_min),3)
        #all
        str_1 = pd.Series({'Room_name': key,'Width':win_w,'Height':win_h,
                            'Distance_to_edges_hor':[min_dist_h,mean_dist_h,max_dist_h,mode_dist_h],
                            'Distance_to_edges_vert':[min_dist_v,mean_dist_v,max_dist_v,mode_dist_v],
                            'Distance_to_next':[min_dist_n,mean_dist_n,max_dist_n,mode_win_n]})
        #win_file.write(str_1.to_frame().T.to_string()  + '\n')
        df_win_new_roomname = pd.concat([df_win_new_roomname,str_1.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\windows_report_roomname.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_win_new_roomname.to_csv(completename_csv,index=False)

# analyse by family- completed
#win_file.write('3. Analyse all windows by their family name \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_win_new_famname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_win_sorted = df_win.loc[df_win['Element_uniqueId'].isin(uniqueid)]
    if len(df_win_sorted)>0:
        #width and hight
        str_wh = df_win_sorted.agg({'Window_width':['min','mean','max'],'Window_height':['min','mean','max']}).T.values
        mode_win_w = df_win_sorted['Window_width'].agg(pd.Series.mode).values[0]
        mode_win_h = df_win_sorted['Window_height'].agg(pd.Series.mode).values[0]
        win_w = list(np.append(str_wh[0],mode_win_w))
        win_h = list(np.append(str_wh[1],mode_win_h))
        #distance
        distance_list_h = []
        for item in list(df_win_sorted['Distance_to_edges_hor'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            distance_list_h.extend(item_num)
        distance_list_v = []
        for item in list(df_win_sorted['Distance_to_edges_vert'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            distance_list_v.extend(item_num)
        max_dist_h = np.max(distance_list_h)
        max_dist_v = np.max(distance_list_v)
        min_dist_h = np.min(distance_list_h)
        min_dist_v = np.min(distance_list_v)
        mean_dist_h = round(np.mean(distance_list_h),3)
        mean_dist_v = round(np.mean(distance_list_v),3)
        mode_dist_h = statistics.mode(distance_list_h)
        mode_dist_v = statistics.mode(distance_list_v)
        str_n_min = df_win_sorted['Distance_to_next_win_min'].values
        mode_win_n = df_win_sorted['Distance_to_next_win_min'].agg(pd.Series.mode).values[0]
        min_dist_n = min(str_n_min)
        max_dist_n = max(str_n_min)
        mean_dist_n = round(statistics.mean(str_n_min),3)

        #all
        str_1 = pd.Series({'Family': key,'Width':win_w,'Height':win_h,
                            'Distance_to_edges_hor':[min_dist_h,mean_dist_h,max_dist_h,mode_dist_h],
                            'Distance_to_edges_vert':[min_dist_v,mean_dist_v,max_dist_v,mode_dist_v],
                            'Distance_to_next':[min_dist_n,mean_dist_n,max_dist_n,mode_win_n]})
        df_win_new_famname = pd.concat([df_win_new_famname,str_1.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\windows_report_family.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_win_new_famname.to_csv(completename_csv,index=False)


#
#
# DOORS - completed
# analyse doors all by category - completed
# nameOfFile_txt = 'data\\tables\\doors_report.txt'
# completename_txt = os.path.join(data_dir,nameOfFile_txt)
# door_file = open(completename_txt,'w+')
# door_file.write("Analyse doors \n")
# door_file.write('1. Analyse all doors (by category: Doors) \n')
df_door_new_cat = pd.DataFrame()

# #width and hight
str_wh = df_doors.agg({'Door_width':['min','mean','max'],'Door_height':['min','mean','max']}).T.values
mode_door_w = df_doors['Door_width'].agg(pd.Series.mode).values[0]
mode_door_h = df_doors['Door_height'].agg(pd.Series.mode).values[0]
door_w = list(np.append(str_wh[0],mode_door_w))
door_h = list(np.append(str_wh[1],mode_door_h))
#distance
distance_list_h = []
for item in list(df_doors['Distance_to_edges_hor'].values):
    item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
    distance_list_h.extend(item_num)
distance_list_v = []
for item in list(df_doors['Distance_to_edges_vert'].values):
    item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
    distance_list_v.extend(item_num)
max_dist_h = np.max(distance_list_h)
max_dist_v = np.max(distance_list_v)
min_dist_h = np.min(distance_list_h)
min_dist_v = np.min(distance_list_v)
mean_dist_h = round(np.mean(distance_list_h),3)
mean_dist_v = round(np.mean(distance_list_v),3)
mode_dist_h = statistics.mode(distance_list_h)
mode_dist_v = statistics.mode(distance_list_v)
str_n_min = df_doors['Distance_to_next_door_min'].values
mode_win_n = df_doors['Distance_to_next_door_min'].agg(pd.Series.mode).values[0]
min_dist_n = min(str_n_min)
max_dist_n = max(str_n_min)
mean_dist_n = round(statistics.mean(str_n_min),3)

#all
str_1 = pd.Series({'Category': 'Doors','Width':door_w,'Height':door_h,
                    'Distance_to_edges_hor':[min_dist_h,mean_dist_h,max_dist_h,mode_dist_h],
                    'Distance_to_edges_vert':[min_dist_v,mean_dist_v,max_dist_v,mode_dist_v],
                    'Distance_to_next':[min_dist_n,mean_dist_n,max_dist_n,mode_win_n]})

#door_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
df_door_new_cat = pd.concat([df_door_new_cat,str_1.to_frame().T],ignore_index=True)
nameOfFile_csv = 'data\\tables\\doors_report_category.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_door_new_cat.to_csv(completename_csv,index=False)

# analyse by room names - completed
#door_file.write('2. Analyse all doors by room names \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_doors_new_roomname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_doors_sorted = df_doors.loc[df_doors['Element_uniqueId'].isin(uniqueid)]
    if len(df_doors_sorted)>0:
        # #width and hight
        str_wh = df_doors_sorted.agg({'Door_width':['min','mean','max'],'Door_height':['min','mean','max']}).T.values
        mode_door_w = df_doors_sorted['Door_width'].agg(pd.Series.mode).values[0]
        mode_door_h = df_doors_sorted['Door_height'].agg(pd.Series.mode).values[0]
        door_w = list(np.append(str_wh[0],mode_door_w))
        door_h = list(np.append(str_wh[1],mode_door_h))
        #distance
        distance_list_h = []
        for item in list(df_doors_sorted['Distance_to_edges_hor'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            distance_list_h.extend(item_num)
        distance_list_v = []
        for item in list(df_doors_sorted['Distance_to_edges_vert'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            distance_list_v.extend(item_num)
        max_dist_h = np.max(distance_list_h)
        max_dist_v = np.max(distance_list_v)
        min_dist_h = np.min(distance_list_h)
        min_dist_v = np.min(distance_list_v)
        mean_dist_h = round(np.mean(distance_list_h),3)
        mean_dist_v = round(np.mean(distance_list_v),3)
        mode_dist_h = statistics.mode(distance_list_h)
        mode_dist_v = statistics.mode(distance_list_v)
        str_n_min = df_doors_sorted['Distance_to_next_door_min'].values
        mode_win_n = df_doors_sorted['Distance_to_next_door_min'].agg(pd.Series.mode).values[0]
        min_dist_n = min(str_n_min)
        max_dist_n = max(str_n_min)
        mean_dist_n = round(statistics.mean(str_n_min),3)
        #all
        str_2 = pd.Series({'Room_name': key,'Width':door_w,'Height':door_h,
                            'Distance_to_edges_hor':[min_dist_h,mean_dist_h,max_dist_h,mode_dist_h],
                            'Distance_to_edges_vert':[min_dist_v,mean_dist_v,max_dist_v,mode_dist_v],
                            'Distance_to_next':[min_dist_n,mean_dist_n,max_dist_n,mode_win_n]})
        #door_file.write(str_2.to_frame().T.to_string()  + '\n')
        df_doors_new_roomname = pd.concat([df_doors_new_roomname,str_2.to_frame().T])

nameOfFile_csv = 'data\\tables\\doors_report_roomname.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_doors_new_roomname.to_csv(completename_csv,index=False)


# analyse by families - completed
#door_file.write('3. Analyse all doors by their family name \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_doors_new_famname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_doors_sorted = df_doors.loc[df_doors['Element_uniqueId'].isin(uniqueid)]
    if len(df_doors_sorted)>0:
        # #width and hight
        str_wh = df_doors_sorted.agg({'Door_width':['min','mean','max'],'Door_height':['min','mean','max']}).T.values
        mode_door_w = df_doors_sorted['Door_width'].agg(pd.Series.mode).values[0]
        mode_door_h = df_doors_sorted['Door_height'].agg(pd.Series.mode).values[0]
        door_w = list(np.append(str_wh[0],mode_door_w))
        door_h = list(np.append(str_wh[1],mode_door_h))
        #distance
        distance_list_h = []
        for item in list(df_doors_sorted['Distance_to_edges_hor'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            distance_list_h.extend(item_num)
        distance_list_v = []
        for item in list(df_doors_sorted['Distance_to_edges_vert'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            distance_list_v.extend(item_num)
        max_dist_h = np.max(distance_list_h)
        max_dist_v = np.max(distance_list_v)
        min_dist_h = np.min(distance_list_h)
        min_dist_v = np.min(distance_list_v)
        mean_dist_h = round(np.mean(distance_list_h),3)
        mean_dist_v = round(np.mean(distance_list_v),3)
        mode_dist_h = statistics.mode(distance_list_h)
        mode_dist_v = statistics.mode(distance_list_v)
        str_n_min = df_doors_sorted['Distance_to_next_door_min'].values
        mode_win_n = df_doors_sorted['Distance_to_next_door_min'].agg(pd.Series.mode).values[0]
        min_dist_n = min(str_n_min)
        max_dist_n = max(str_n_min)
        mean_dist_n = round(statistics.mean(str_n_min),3)
        # min_dist_n = min(str_n_min[str_n_min!=0])
        # max_dist_n = max(str_n_min[str_n_min!=0])
        #mean_dist_n = round(statistics.mean(str_n_min[str_n_min!=0]),3)
        #all
        str_3 = pd.Series({'Family': key,'Width':door_w,'Height':door_h,
                            'Distance_to_edges_hor':[min_dist_h,mean_dist_h,max_dist_h,mode_dist_h],
                            'Distance_to_edges_vert':[min_dist_v,mean_dist_v,max_dist_v,mode_dist_v],
                            'Distance_to_next':[min_dist_n,mean_dist_n,max_dist_n,mode_win_n]})
        #door_file.write(str_3.to_frame().T.to_string()  + '\n')
        df_doors_new_famname = pd.concat([df_doors_new_famname,str_3.to_frame().T])

nameOfFile_csv = 'data\\tables\\doors_report_family.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_doors_new_famname.to_csv(completename_csv,index=False)

# analyse by families with frequency - completed
#
#
#
# WALLS - completed
# analyse walls all by category - completed
# nameOfFile_txt = 'data\\tables\\walls_report.txt'
# completename_txt = os.path.join(data_dir,nameOfFile_txt)
# walls_file = open(completename_txt,'w+')
# walls_file.write("Analyse walls \n")
# walls_file.write('1. Analyse all walls (by category: Walls) \n')
df_walls_new_cat = pd.DataFrame()
#width and hight
str_wh = df_walls.agg({'Width':['min','mean','max'],'Height':['min','mean','max']}).T.values
min_wall_w = round(min(df_walls['Width'].values),3)
max_wall_w = round(max(df_walls['Width'].values),3)
mean_wall_w = round(df_walls['Width'].agg(pd.Series.mean),3)
min_wall_h = round(min(df_walls['Height'].values),3)
max_wall_h = round(max(df_walls['Height'].values),3)
mean_wall_h = round(df_walls['Height'].agg(pd.Series.mean),3)
mode_wall_w = round(df_walls['Width'].agg(pd.Series.mode).values[0],3)
mode_wall_h = round(df_walls['Height'].agg(pd.Series.mode).values[0],3)
wall_w = [min_wall_w,mean_wall_w,max_wall_w,mode_wall_w]
wall_h = [min_wall_h,mean_wall_h,max_wall_h,mode_wall_h]
#distance
distance_list_p = []
for item in list(df_walls['Distance_to_parall'].values):
    item = item.replace('None,', '')
    item = item.replace('None', '')
    item = item.replace(',', '')
    item_num = np.fromstring(item[1:-1],dtype=float,sep=' ')
    distance_list_p.extend(item_num)
angles_list = []
for item in list(df_walls['Angles_to_walls'].values):
    item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
    item_num = item_num[~np.isnan(item_num)]
    angles_list.extend(item_num)
max_dist_p = np.max(distance_list_p)
min_dist_p = np.min(distance_list_p)
mean_dist_p = round(np.mean(distance_list_p),3)
mode_dist_p = statistics.mode(distance_list_p)
max_angle= np.max(angles_list)
min_angle = np.min(angles_list)
mean_angle = round(np.mean(angles_list),3)
mode_angle= statistics.mode(angles_list)
#all
str_1 = pd.Series({'Category': 'Walls','Width':wall_w,'Height':wall_h,
                    'Distance_to_parall_walls':[min_dist_h,mean_dist_h,max_dist_h,mode_dist_h],
                    'Angles_to_walls':[min_angle,mean_angle,max_angle,mode_angle]})
#walls_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
df_walls_new_cat = pd.concat([df_walls_new_cat,str_1.to_frame().T],ignore_index=True)
nameOfFile_csv = 'data\\tables\\walls_report_category.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_walls_new_cat.to_csv(completename_csv,index=False)

# analyse by room names - completed
#walls_file.write('2. Analyse all walls by room names \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_walls_new_roomname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_walls_sorted = df_walls.loc[df_walls['Element_uniqueId'].isin(uniqueid)]
    if len(df_walls_sorted)>0:
        #width and hight
        str_wh = df_walls_sorted.agg({'Width':['min','mean','max'],'Height':['min','mean','max']}).T.values
        min_wall_w = round(min(df_walls_sorted['Width'].values),3)
        max_wall_w = round(max(df_walls_sorted['Width'].values),3)
        mean_wall_w = round(df_walls_sorted['Width'].agg(pd.Series.mean),3)
        min_wall_h = round(min(df_walls_sorted['Height'].values),3)
        max_wall_h = round(max(df_walls_sorted['Height'].values),3)
        mean_wall_h = round(df_walls_sorted['Height'].agg(pd.Series.mean),3)
        mode_wall_w = round(df_walls_sorted['Width'].agg(pd.Series.mode).values[0],3)
        mode_wall_h = round(df_walls_sorted['Height'].agg(pd.Series.mode).values[0],3)
        # wall_w = list(np.append(str_wh[0],mode_wall_w))
        # wall_h = list(np.append(str_wh[1],mode_wall_h))
        wall_w = [min_wall_w,mean_wall_w,max_wall_w,mode_wall_w]
        wall_h = [min_wall_h,mean_wall_h,max_wall_h,mode_wall_h]
        #distance
        distance_list_p = []
        for item in list(df_walls_sorted['Distance_to_parall'].values):
            item = item.replace('None,', '')
            item = item.replace('None', '')
            item = item.replace(',', '')
            item_num = np.fromstring(item[1:-1],dtype=float,sep=' ')
            distance_list_p.extend(item_num)
        angles_list = []
        for item in list(df_walls_sorted['Angles_to_walls'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            item_num = item_num[~np.isnan(item_num)]
            angles_list.extend(item_num)
        max_dist_p = np.max(distance_list_p)
        min_dist_p = np.min(distance_list_p)
        mean_dist_p = round(np.mean(distance_list_p),3)
        mode_dist_p = statistics.mode(distance_list_p)
        max_angle= np.max(angles_list)
        min_angle = np.min(angles_list)
        mean_angle = round(np.mean(angles_list),3)
        mode_angle= statistics.mode(angles_list)
        #all
        str_1 = pd.Series({'Room_name': key,'Width':wall_w,'Height':wall_h,
                            'Distance_to_parall_walls':[min_dist_h,mean_dist_h,max_dist_h,mode_dist_h],
                            'Angles_to_walls':[min_angle,mean_angle,max_angle,mode_angle]})
        #walls_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
        df_walls_new_roomname = pd.concat([df_walls_new_roomname,str_1.to_frame().T],ignore_index=True)   
nameOfFile_csv = 'data\\tables\\walls_report_roomname.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_walls_new_roomname.to_csv(completename_csv,index=False)

# analyse by room names - completed
#walls_file.write('3. Analyse all walls by their family name \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_wall_new_famname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_walls_sorted = df_walls.loc[df_walls['Element_uniqueId'].isin(uniqueid)]
    if len(df_walls_sorted)>0:
        #width and hight
        str_wh = df_walls_sorted.agg({'Width':['min','mean','max'],'Height':['min','mean','max']}).T.values
        min_wall_w = round(min(df_walls_sorted['Width'].values),3)
        max_wall_w = round(max(df_walls_sorted['Width'].values),3)
        mean_wall_w = round(df_walls_sorted['Width'].agg(pd.Series.mean),3)
        min_wall_h = round(min(df_walls_sorted['Height'].values),3)
        max_wall_h = round(max(df_walls_sorted['Height'].values),3)
        mean_wall_h = round(df_walls_sorted['Height'].agg(pd.Series.mean),3)
        mode_wall_w = round(df_walls_sorted['Width'].agg(pd.Series.mode).values[0],3)
        mode_wall_h = round(df_walls_sorted['Height'].agg(pd.Series.mode).values[0],3)
        # wall_w = list(np.append(str_wh[0],mode_wall_w))
        # wall_h = list(np.append(str_wh[1],mode_wall_h))
        wall_w = [min_wall_w,mean_wall_w,max_wall_w,mode_wall_w]
        wall_h = [min_wall_h,mean_wall_h,max_wall_h,mode_wall_h]
        #distance
        distance_list_p = []
        for item in list(df_walls_sorted['Distance_to_parall'].values):
            item = item.replace('None,', '')
            item = item.replace('None', '')
            item = item.replace(',', '')
            item_num = np.fromstring(item[1:-1],dtype=float,sep=' ')
            distance_list_p.extend(item_num)
        angles_list = []
        for item in list(df_walls_sorted['Angles_to_walls'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            item_num = item_num[~np.isnan(item_num)]
            angles_list.extend(item_num)
        max_dist_p = np.max(distance_list_p)
        min_dist_p = np.min(distance_list_p)
        mean_dist_p = round(np.mean(distance_list_p),3)
        mode_dist_p = statistics.mode(distance_list_p)
        max_angle= np.max(angles_list)
        min_angle = np.min(angles_list)
        mean_angle = round(np.mean(angles_list),3)
        mode_angle= statistics.mode(angles_list)
        #all
        str_1 = pd.Series({'Family': key,'Width':wall_w,'Height':wall_h,
                            'Distance_to_parall_walls':[min_dist_h,mean_dist_h,max_dist_h,mode_dist_h],
                            'Angles_to_walls':[min_angle,mean_angle,max_angle,mode_angle]})
        #walls_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
        df_wall_new_famname = pd.concat([df_wall_new_famname,str_1.to_frame().T],ignore_index=True)   
nameOfFile_csv = 'data\\tables\\walls_report_family.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_wall_new_famname.to_csv(completename_csv,index=False)
#
#
#
# FLOORS
# analyse floors all by category - completed
# nameOfFile_txt = 'data\\tables\\floors_report.txt'
# completename_txt = os.path.join(data_dir,nameOfFile_txt)
# floors_file = open(completename_txt,'w+')
# floors_file.write("Analyse floors \n")
# floors_file.write('1. Analyse all floors (by category: Floors) \n')
df_floors_new_cat = pd.DataFrame()

col1 = list(df_floors['Distance_to_nonparallel'].values)
for i in range(len(col1)):
    col1[i] = eval(col1[i])
col1_new = pd.Series(col1)
col1_new = col1_new.explode().values
col1_new = [float(i) for i in col1_new]

col2 = list(df_floors['Distance_to_parallel'].values)
for i in range(len(col2)):
    col2[i] = eval(col2[i])
col2_new = pd.Series(col2)
col2_new = col2_new.explode().values

col2_new = [float(i) for i in col2_new]

str_1 = pd.Series({'Category': 'Floors',
                   'Distance_to_nonparallel': [round(min(col1_new),3),round(statistics.mean(col1_new),3),round(max(col1_new),3),statistics.mode(col1_new)],
                    'Distance_to_parallel':[round(min(col2_new),3),round(statistics.mean(col2_new),3),round(max(col2_new),3),statistics.mode(col2_new)] })
#floors_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
df_floors_new_cat = pd.concat([df_floors_new_cat,str_1.to_frame().T],ignore_index=True)
nameOfFile_csv = 'data\\tables\\floors_report_category.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_floors_new_cat.to_csv(completename_csv,index=False)

# analyse by room names - completed
#floors_file.write('2. Analyse all floors by room names \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_floors_new_roomname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_floors_sorted = df_floors.loc[df_floors['Element_uniqueId'].isin(uniqueid)]
    if len(df_floors_sorted)>0:
        col1 = list(df_floors_sorted['Distance_to_nonparallel'].values)
        for i in range(len(col1)):
            col1[i] = eval(col1[i])
        col1_new = pd.Series(col1)
        col1_new = col1_new.explode().values
        col1_new = [float(i) for i in col1_new]

        col2 = list(df_floors_sorted['Distance_to_parallel'].values)
        for i in range(len(col2)):
            col2[i] = eval(col2[i])
        col2_new = pd.Series(col2)
        col2_new = col2_new.explode().values

        col2_new = [float(i) for i in col2_new]
        str_1 = pd.Series({'Room_name': key,
                        'Distance_to_nonparallel': [round(min(col1_new),3),round(statistics.mean(col1_new),3),round(max(col1_new),3),statistics.mode(col1_new)],
                            'Distance_to_parallel':[round(min(col2_new),3),round(statistics.mean(col2_new),3),round(max(col2_new),3),statistics.mode(col2_new)] })
        #floors_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
        df_floors_new_roomname = pd.concat([df_floors_new_roomname,str_1.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\floors_report_roomname.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_floors_new_roomname.to_csv(completename_csv,index=False)

# analyse by family names - completed
#floors_file.write('3. Analyse all floors by their family name \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_floors_new_famname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_floors_sorted = df_floors.loc[df_floors['Element_uniqueId'].isin(uniqueid)]
    if len(df_floors_sorted)>0:
        col1 = list(df_floors_sorted['Distance_to_nonparallel'].values)
        for i in range(len(col1)):
            col1[i] = eval(col1[i])
        col1_new = pd.Series(col1)
        col1_new = col1_new.explode().values
        col1_new = [float(i) for i in col1_new]

        col2 = list(df_floors_sorted['Distance_to_parallel'].values)
        for i in range(len(col2)):
            col2[i] = eval(col2[i])
        col2_new = pd.Series(col2)
        col2_new = col2_new.explode().values

        col2_new = [float(i) for i in col2_new]
        str_1 = pd.Series({'Family': key,
                        'Distance_to_nonparallel': [round(min(col1_new),3),round(statistics.mean(col1_new),3),round(max(col1_new),3),statistics.mode(col1_new)],
                            'Distance_to_parallel':[round(min(col2_new),3),round(statistics.mean(col2_new),3),round(max(col2_new),3),statistics.mode(col2_new)] })
        #floors_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
        df_floors_new_famname = pd.concat([df_floors_new_famname,str_1.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\floors_report_family.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_floors_new_famname.to_csv(completename_csv,index=False)
#
#
#
# FURNITURE - OK
# analyse furniture all by category
# nameOfFile_txt = 'data\\tables\\furniture_report.txt'
# completename_txt = os.path.join(data_dir,nameOfFile_txt)
# furniture_file = open(completename_txt,'w+')
# furniture_file.write("Analyse furniture \n")
# furniture_file.write('1. Analyse all furniture (by category: Furniture) \n')
df_furniture_new_cat = pd.DataFrame()
# str_wh = df_furniture.agg({'Distance_to_nearest_mi':['mean'],
#                           'Distance_to_nearest_mean':['mean'],
#                           'Distance_to_nearest_ma':['mean']}).values[0].tolist()
distance_list = []
for item in list(df_furniture['Distance_to_nearest'].values):
    item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
    distance_list.extend(item_num)
max_dist = np.max(distance_list)
min_dist = np.min(distance_list)
mean_dist = round(np.mean(distance_list),3)
mode_dist = statistics.mode(distance_list)
str_1 = pd.Series({'Category':'Furniture',
                    'Distance_to_nearest':[min_dist,mean_dist,max_dist,mode_dist]})
#furniture_file.write(str_1.to_frame().T.to_string()  + '\n')
df_furniture_new_cat = pd.concat([df_furniture_new_cat,str_1.to_frame().T],ignore_index=True)
nameOfFile_csv = 'data\\tables\\furniture_report_category.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_furniture_new_cat.to_csv(completename_csv,index=False)

# analyse by room names - completed
#furniture_file.write('2. Analyse all furniture by room names \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_furniture_new_roomname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_furniture_sorted = df_furniture.loc[df_furniture['Element_uniqueId'].isin(uniqueid)]
    if len(df_furniture_sorted)>0:
        distance_list = []
        for item in list(df_furniture_sorted['Distance_to_nearest'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            distance_list.extend(item_num)
        max_dist = np.max(distance_list)
        min_dist = np.min(distance_list)
        mean_dist = round(np.mean(distance_list),3)
        mode_dist = statistics.mode(distance_list)
        str_1 = pd.Series({'Room_name':key,
                            'Distance_to_nearest':[min_dist,mean_dist,max_dist,mode_dist]})
        df_furniture_new_roomname = pd.concat([df_furniture_new_roomname,str_1.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\furniture_report_roomname.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_furniture_new_roomname.to_csv(completename_csv,index=False)

# analyse by family names - completed
#furniture_file.write('3. Analyse all furniture by their family name \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_furniture_new_famname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_furniture_sorted = df_furniture.loc[df_furniture['Element_uniqueId'].isin(uniqueid)]
    if len(df_furniture_sorted)>0:
        distance_list = []
        for item in list(df_furniture_sorted['Distance_to_nearest'].values):
            item_num = np.fromstring(item[1:-1],dtype=float,sep=',')
            distance_list.extend(item_num)
        max_dist = np.max(distance_list)
        min_dist = np.min(distance_list)
        mean_dist = round(np.mean(distance_list),3)
        mode_dist = statistics.mode(distance_list)
        str_1 = pd.Series({'Family':key,
                            'Distance_to_nearest':[min_dist,mean_dist,max_dist,mode_dist]})
        df_furniture_new_famname = pd.concat([df_furniture_new_famname,str_1.to_frame().T],ignore_index=True)


nameOfFile_csv = 'data\\tables\\furniture_report_family.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_furniture_new_famname.to_csv(completename_csv,index=False)
t.Commit()