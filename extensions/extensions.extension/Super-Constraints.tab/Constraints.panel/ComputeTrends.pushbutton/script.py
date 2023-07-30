#! python3
import sys
# print(sys.version)
# for problems with packages once uncommet line below (with correct site-packages directory)
# sys.path.append(r"C:\Users\elyah\AppData\Local\Programs\Python\Python38\Lib\site-packages")
# import clr
import os
import os.path
import statistics
import numpy as np
import pandas as pd
import collections

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

def find_frequency_value(distance_list):
    duplicates = []
    non_duplicates = set()
    for val in distance_list:
        if val in non_duplicates:
            duplicates.append(val)
        else:
            non_duplicates.add(val)
    if len(duplicates)>0:
        counter = collections.Counter(duplicates)
        most_common = [counter.most_common(1)[0][0]]
    else:
        most_common = [min(distance_list),max(distance_list)]
    return most_common


# WINDOWS
# analyse windows
nameOfFile_txt = 'data\\tables\\windows_report.txt'
completename_txt = os.path.join(data_dir,nameOfFile_txt)
win_file = open(completename_txt,'w+')
win_file.write("Analyse windows \n")
win_file.write('1. Analyse all windows (by category:Windows) \n')
# analyse windows all by category - completed
str_wh = df_win.agg({'Window_width':['min','mean','max'],'Window_height':['min','mean','max']}).T.values
str_e_hor_min = df_win.agg({'Distance_to_edges_hor_mi':['min']}).values[0]
str_e_hor_mean = df_win.agg({'Distance_to_edges_hor_mean':['mean']}).values[0]
str_e_hor_max = df_win.agg({'Distance_to_edges_hor_ma':['max']}).values[0]
str_e_vert_min = df_win.agg({'Distance_to_edges_vert_mi':['min']}).values[0]
str_e_vert_mean = df_win.agg({'Distance_to_edges_vert_mean':['mean']}).values[0]
str_e_vert_max = df_win.agg({'Distance_to_edges_vert_ma':['max']}).values[0]
str_n_ = df_win['Distance_to_next_win_min'].values
if len(str_n_) == 0:
    str_n_min = 0.
    str_n_max = 0.
    str_n_mean = 0.
else:
    try:
        str_n_min = min(str_n_[str_n_!=0])
        str_n_max = max(str_n_[str_n_!=0])
        str_n_mean = round(statistics.mean(str_n_[str_n_!=0]),3)
    except:
        str_n_min = 0.
        str_n_max = 0.
        str_n_mean = 0.
str_1 = pd.Series({'Category': 'Windows','Width':list(str_wh[0]),'Height':list(str_wh[1]),
                    'Distance_to_edges_hor':[str_e_hor_min[0],str_e_hor_mean[0],str_e_hor_max[0]],
                    'Distance_to_edges_vert':[str_e_vert_min[0],str_e_vert_mean[0],str_e_vert_max[0]],
                    'Distance_to_next':[str_n_min,str_n_mean,str_n_max]})
win_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
df_win_new_cat = pd.concat([df_win_new,str_1.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\windows_report_category.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_win_new_cat.to_csv(completename_csv,index=False)

# analyse by room names - completed
win_file.write('2. Analyse all windows by room names \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_win_new_roomname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_win_sorted = df_win.loc[df_win['Element_uniqueId'].isin(uniqueid)]
    if len(df_win_sorted)>0:
        str_wh = df_win_sorted.agg({'Window_width':['min','mean','max'],'Window_height':['min','mean','max']}).T.values
        str_e_hor_min = df_win_sorted.agg({'Distance_to_edges_hor_mi':['min']}).values[0]
        str_e_hor_mean = df_win_sorted.agg({'Distance_to_edges_hor_mean':['mean']}).values[0]
        str_e_hor_max = df_win_sorted.agg({'Distance_to_edges_hor_ma':['max']}).values[0]
        str_e_vert_min = df_win_sorted.agg({'Distance_to_edges_vert_mi':['min']}).values[0]
        str_e_vert_mean = df_win_sorted.agg({'Distance_to_edges_vert_mean':['mean']}).values[0]
        str_e_vert_max = df_win_sorted.agg({'Distance_to_edges_vert_ma':['max']}).values[0]
        #str_n_min = df_win_sorted.agg({'Distance_to_next_win_min':['min']}).values[0]
        str_n_ = df_win_sorted['Distance_to_next_win_min'].values
        if len(str_n_) == 0:
            str_n_min = 0.
            str_n_max = 0.
            str_n_mean = 0.
        else:
            try:
                str_n_min = min(str_n_[str_n_!=0])
                str_n_max = max(str_n_[str_n_!=0])
                str_n_mean = round(statistics.mean(str_n_[str_n_!=0]),3)
            except:
                str_n_min = 0.
                str_n_max = 0.
                str_n_mean = 0.
        str_2 = pd.Series({'Room_name': key,'Width':list(str_wh[0]),'Height':list(str_wh[1]),
                           'Distance_to_edges_hor':[str_e_hor_min[0],str_e_hor_mean[0],str_e_hor_max[0]],
                           'Distance_to_edges_vert':[str_e_vert_min[0],str_e_vert_mean[0],str_e_vert_max[0]],
                           'Distance_to_next':[str_n_min,str_n_mean,str_n_max]})
        win_file.write(str_2.to_frame().T.to_string()  + '\n')
        df_win_new_roomname = pd.concat([df_win_new_roomname,str_2.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\windows_report_roomname.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_win_new_roomname.to_csv(completename_csv,index=False)

# analyse by room names and frequency - completed
win_file.write('2. Analyse all windows by room names and frequency \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_win_new_roomname_fr = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)

    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_win_sorted = df_win.loc[df_win['Element_uniqueId'].isin(uniqueid)]
    if len(df_win_sorted)>0:
        dupl_width = find_frequency_value(df_win_sorted['Window_width'].values.tolist())
        if len(dupl_width)>1:
            dupl_width = [dupl_width[0]]
        dupl_height = find_frequency_value(df_win_sorted['Window_height'].values.tolist())
        if len(dupl_height)>1:
            dupl_height = [dupl_height[0]]
        dupl_hor_dis_min = find_frequency_value(df_win_sorted['Distance_to_edges_hor_mi'].values.tolist())
        if len(dupl_hor_dis_min)>1:
            dupl_hor_dis_min = dupl_hor_dis_min[0]
        else:
            dupl_hor_dis_min = dupl_hor_dis_min[0]
        dupl_hor_dis_max = find_frequency_value(df_win_sorted['Distance_to_edges_hor_ma'].values.tolist())
        if len(dupl_hor_dis_max)>1:
            dupl_hor_dis_max = dupl_hor_dis_max[1]
        else:
            dupl_hor_dis_max = dupl_hor_dis_max[0]
        dupl_ver_dis_min = find_frequency_value(df_win_sorted['Distance_to_edges_vert_mi'].values.tolist())
        if len(dupl_ver_dis_min)>1:
            dupl_ver_dis_min = dupl_ver_dis_min[0]
        else:
            dupl_ver_dis_min = dupl_ver_dis_min[0]
        dupl_ver_dis_max = find_frequency_value(df_win_sorted['Distance_to_edges_vert_ma'].values.tolist())
        if len(dupl_ver_dis_max)>1:
            dupl_ver_dis_max = dupl_ver_dis_max[1]
        else:
            dupl_ver_dis_max = dupl_ver_dis_max[0]
        dupl_next_dis_min = find_frequency_value(df_win_sorted['Distance_to_next_win_min'].values.tolist())
        if len(dupl_next_dis_min)>1:
            dupl_next_dis_min = dupl_next_dis_min[0]
        else:
            dupl_next_dis_min = dupl_next_dis_min[0]

        str_2 = pd.Series({'Room_name': key,'Width':dupl_width,'Height':dupl_height,
                           'Distance_to_edges_hor':[dupl_hor_dis_min,dupl_hor_dis_max],
                           'Distance_to_edges_vert':[dupl_ver_dis_min,dupl_ver_dis_max],
                           'Distance_to_next':[dupl_next_dis_min]})
        win_file.write(str_2.to_frame().T.to_string()  + '\n')
        df_win_new_roomname_fr = pd.concat([df_win_new_roomname_fr,str_2.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\windows_report_roomname_freq.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_win_new_roomname_fr.to_csv(completename_csv,index=False)

# analyse by family- completed
win_file.write('3. Analyse all windows by their family name \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_win_new_famname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_win_sorted = df_win.loc[df_win['Element_uniqueId'].isin(uniqueid)]
    if len(df_win_sorted)>0:
        str_wh = df_win_sorted.agg({'Window_width':['min','mean','max'],'Window_height':['min','mean','max']}).T.values
        str_e_hor_min = df_win_sorted.agg({'Distance_to_edges_hor_mi':['min']}).values[0]
        str_e_hor_mean = df_win_sorted.agg({'Distance_to_edges_hor_mean':['mean']}).values[0]
        str_e_hor_max = df_win_sorted.agg({'Distance_to_edges_hor_ma':['max']}).values[0]
        str_e_vert_min = df_win_sorted.agg({'Distance_to_edges_vert_mi':['min']}).values[0]
        str_e_vert_mean = df_win_sorted.agg({'Distance_to_edges_vert_mean':['mean']}).values[0]
        str_e_vert_max = df_win_sorted.agg({'Distance_to_edges_vert_ma':['max']}).values[0]
        str_n_ = df_win_sorted['Distance_to_next_win_min'].values
        if len(str_n_) == 0:
            str_n_min = 0.
            str_n_max = 0.
            str_n_mean = 0.
        else:
            try:
                str_n_min = min(str_n_[str_n_!=0])
                str_n_max = max(str_n_[str_n_!=0])
                str_n_mean = round(statistics.mean(str_n_[str_n_!=0]),3)
            except:
                str_n_min = 0.
                str_n_max = 0.
                str_n_mean = 0.
        str_2 = pd.Series({'Family': key,'Width':list(str_wh[0]),'Height':list(str_wh[1]),
                           'Distance_to_edges_hor':[str_e_hor_min[0],str_e_hor_mean[0],str_e_hor_max[0]],
                           'Distance_to_edges_vert':[str_e_vert_min[0],str_e_vert_mean[0],str_e_vert_max[0]],
                           'Distance_to_next':[str_n_min,str_n_mean,str_n_max]})
        win_file.write(str_2.to_frame().T.to_string()  + '\n')
        df_win_new_famname = pd.concat([df_win_new_famname,str_2.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\windows_report_family.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_win_new_famname.to_csv(completename_csv,index=False)

# analyse by family and frequency- completed
win_file.write('3. Analyse all windows by their family name and frequency \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_win_new_famname_fr = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_win_sorted = df_win.loc[df_win['Element_uniqueId'].isin(uniqueid)]
    if len(df_win_sorted)>0:
        dupl_width = find_frequency_value(df_win_sorted['Window_width'].values.tolist())
        if len(dupl_width)>1:
            dupl_width = [dupl_width[0]]
        dupl_height = find_frequency_value(df_win_sorted['Window_height'].values.tolist())
        if len(dupl_height)>1:
            dupl_height = [dupl_height[0]]
        dupl_hor_dis_min = find_frequency_value(df_win_sorted['Distance_to_edges_hor_mi'].values.tolist())
        if len(dupl_hor_dis_min)>1:
            dupl_hor_dis_min = dupl_hor_dis_min[0]
        else:
            dupl_hor_dis_min = dupl_hor_dis_min[0]
        dupl_hor_dis_max = find_frequency_value(df_win_sorted['Distance_to_edges_hor_ma'].values.tolist())
        if len(dupl_hor_dis_max)>1:
            dupl_hor_dis_max = dupl_hor_dis_max[1]
        else:
            dupl_hor_dis_max = dupl_hor_dis_max[0]
        dupl_ver_dis_min = find_frequency_value(df_win_sorted['Distance_to_edges_vert_mi'].values.tolist())
        if len(dupl_ver_dis_min)>1:
            dupl_ver_dis_min = dupl_ver_dis_min[0]
        else:
            dupl_ver_dis_min = dupl_ver_dis_min[0]
        dupl_ver_dis_max = find_frequency_value(df_win_sorted['Distance_to_edges_vert_ma'].values.tolist())
        if len(dupl_ver_dis_max)>1:
            dupl_ver_dis_max = dupl_ver_dis_max[1]
        else:
            dupl_ver_dis_max = dupl_ver_dis_max[0]
        dupl_next_dis_min = find_frequency_value(df_win_sorted['Distance_to_next_win_min'].values.tolist())
        if len(dupl_next_dis_min)>1:
            dupl_next_dis_min = dupl_next_dis_min[0]
        else:
            dupl_next_dis_min = dupl_next_dis_min[0]

        str_2 = pd.Series({'Room_name': key,'Width':dupl_width,'Height':dupl_height,
                        'Distance_to_edges_hor':[dupl_hor_dis_min,dupl_hor_dis_max],
                        'Distance_to_edges_vert':[dupl_ver_dis_min,dupl_ver_dis_max],
                        'Distance_to_next':[dupl_next_dis_min]})
        win_file.write(str_2.to_frame().T.to_string()  + '\n')
        df_win_new_famname_fr = pd.concat([df_win_new_famname_fr,str_2.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\windows_report_family_freq.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_win_new_famname_fr.to_csv(completename_csv,index=False)
#
#
#
# DOORS - completed
# analyse doors all by category - completed
nameOfFile_txt = 'data\\tables\\doors_report.txt'
completename_txt = os.path.join(data_dir,nameOfFile_txt)
door_file = open(completename_txt,'w+')
door_file.write("Analyse doors \n")
door_file.write('1. Analyse all doors (by category: Doors) \n')
df_door_new_cat = pd.DataFrame()
str_wh = df_doors.agg({'Door_width':['min','mean','max'],'Door_height':['min','mean','max']}).T.values
str_e_hor_min = df_doors.agg({'Distance_to_edges_hor_mi':['min']}).values[0]
str_e_hor_mean = df_doors.agg({'Distance_to_edges_hor_mean':['mean']}).values[0]
str_e_hor_max = df_doors.agg({'Distance_to_edges_hor_ma':['max']}).values[0]
str_e_vert_min = df_doors.agg({'Distance_to_edges_vert_mi':['min']}).values[0]
str_e_vert_mean = df_doors.agg({'Distance_to_edges_vert_mean':['mean']}).values[0]
str_e_vert_max = df_doors.agg({'Distance_to_edges_vert_ma':['max']}).values[0]
str_n_min = df_doors.agg({'Distance_to_next_door_min':['min','mean','max']}).T.values
str_1 = pd.Series({'Category': 'Doors','Width':list(str_wh[0]),'Height':list(str_wh[1]),
                    'Distance_to_edges_hor':[str_e_hor_min[0],str_e_hor_mean[0],str_e_hor_max[0]],
                    'Distance_to_edges_vert':[str_e_vert_min[0],str_e_vert_mean[0],str_e_vert_max[0]],
                    'Distance_to_next':list(str_n_min[0])})
door_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
df_door_new_cat = pd.concat([df_door_new_cat,str_1.to_frame().T],ignore_index=True)
nameOfFile_csv = 'data\\tables\\doors_report_category.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_door_new_cat.to_csv(completename_csv,index=False)

# analyse by room names - completed
door_file.write('2. Analyse all doors by room names \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_doors_new_roomname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_doors_sorted = df_doors.loc[df_doors['Element_uniqueId'].isin(uniqueid)]
    if len(df_doors_sorted)>0:
        str_wh = df_doors_sorted.agg({'Door_width':['min','mean','max'],'Door_height':['min','mean','max']}).T.values
        str_e_hor_min = df_doors_sorted.agg({'Distance_to_edges_hor_mi':['min']}).values[0]
        str_e_hor_mean = df_doors_sorted.agg({'Distance_to_edges_hor_mean':['mean']}).values[0]
        str_e_hor_max = df_doors_sorted.agg({'Distance_to_edges_hor_ma':['max']}).values[0]
        str_e_vert_min = df_doors_sorted.agg({'Distance_to_edges_vert_mi':['min']}).values[0]
        str_e_vert_mean = df_doors_sorted.agg({'Distance_to_edges_vert_mean':['mean']}).values[0]
        str_e_vert_max = df_doors_sorted.agg({'Distance_to_edges_vert_ma':['max']}).values[0]
        str_n_min = df_doors_sorted.agg({'Distance_to_next_door_min':['min','mean','max']}).T.values
        str_2 = pd.Series({'Room_name': key,'Width':list(str_wh[0]),'Height':list(str_wh[1]),
                           'Distance_to_edges_hor':[str_e_hor_min[0],str_e_hor_mean[0],str_e_hor_max[0]],
                           'Distance_to_edges_vert':[str_e_vert_min[0],str_e_vert_mean[0],str_e_vert_max[0]],
                           'Distance_to_next':list(str_n_min[0])})
        door_file.write(str_2.to_frame().T.to_string()  + '\n')
        df_doors_new_roomname = pd.concat([df_doors_new_roomname,str_2.to_frame().T])

nameOfFile_csv = 'data\\tables\\doors_report_roomname.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_doors_new_roomname.to_csv(completename_csv,index=False)

# analyse by room names and frequency - completed
win_file.write('2. Analyse all doors by room names and frequency \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_doors_new_roomname_fr = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_door_sorted = df_doors.loc[df_doors['Element_uniqueId'].isin(uniqueid)]
    if len(df_door_sorted)>0:
        dupl_width = find_frequency_value(df_door_sorted['Door_width'].values.tolist())
        if len(dupl_width)>1:
            dupl_width = [dupl_width[0]]
        dupl_height = find_frequency_value(df_door_sorted['Door_height'].values.tolist())
        if len(dupl_height)>1:
            dupl_height = [dupl_height[0]]
        dupl_hor_dis_min = find_frequency_value(df_door_sorted['Distance_to_edges_hor_mi'].values.tolist())
        if len(dupl_hor_dis_min)>1:
            dupl_hor_dis_min = dupl_hor_dis_min[0]
        else:
            dupl_hor_dis_min = dupl_hor_dis_min[0]
        dupl_hor_dis_max = find_frequency_value(df_door_sorted['Distance_to_edges_hor_ma'].values.tolist())
        if len(dupl_hor_dis_max)>1:
            dupl_hor_dis_max = dupl_hor_dis_max[1]
        else:
            dupl_hor_dis_max = dupl_hor_dis_max[0]
        dupl_ver_dis_min = find_frequency_value(df_door_sorted['Distance_to_edges_vert_mi'].values.tolist())
        if len(dupl_ver_dis_min)>1:
            dupl_ver_dis_min = dupl_ver_dis_min[0]
        else:
            dupl_ver_dis_min = dupl_ver_dis_min[0]
        dupl_ver_dis_max = find_frequency_value(df_door_sorted['Distance_to_edges_vert_ma'].values.tolist())
        if len(dupl_ver_dis_max)>1:
            dupl_ver_dis_max = dupl_ver_dis_max[1]
        else:
            dupl_ver_dis_max = dupl_ver_dis_max[0]
        dupl_next_dis_min = find_frequency_value(df_door_sorted['Distance_to_next_door_min'].values.tolist())
        if len(dupl_next_dis_min)>1:
            dupl_next_dis_min = dupl_next_dis_min[0]
        else:
            dupl_next_dis_min = dupl_next_dis_min[0]

        str_2 = pd.Series({'Room_name': key,'Width':dupl_width,'Height':dupl_height,
                           'Distance_to_edges_hor':[dupl_hor_dis_min,dupl_hor_dis_max],
                           'Distance_to_edges_vert':[dupl_ver_dis_min,dupl_ver_dis_max],
                           'Distance_to_next':[dupl_next_dis_min]})
        win_file.write(str_2.to_frame().T.to_string()  + '\n')
        df_doors_new_roomname_fr = pd.concat([df_doors_new_roomname_fr,str_2.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\doors_report_roomname_freq.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_doors_new_roomname_fr.to_csv(completename_csv,index=False)

# analyse by families - completed
door_file.write('3. Analyse all doors by their family name \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_doors_new_famname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_doors_sorted = df_doors.loc[df_doors['Element_uniqueId'].isin(uniqueid)]
    if len(df_doors_sorted)>0:
        str_wh = df_doors_sorted.agg({'Door_width':['min','mean','max'],'Door_height':['min','mean','max']}).T.values
        str_e_hor_min = df_doors_sorted.agg({'Distance_to_edges_hor_mi':['min']}).values[0]
        str_e_hor_mean = df_doors_sorted.agg({'Distance_to_edges_hor_mean':['mean']}).values[0]
        str_e_hor_max = df_doors_sorted.agg({'Distance_to_edges_hor_ma':['max']}).values[0]
        str_e_vert_min = df_doors_sorted.agg({'Distance_to_edges_vert_mi':['min']}).values[0]
        str_e_vert_mean = df_doors_sorted.agg({'Distance_to_edges_vert_mean':['mean']}).values[0]
        str_e_vert_max = df_doors_sorted.agg({'Distance_to_edges_vert_ma':['max']}).values[0]
        str_n_min = df_doors_sorted.agg({'Distance_to_next_door_min':['min','mean','max']}).T.values
        str_3 = pd.Series({'Family': key,'Width':list(str_wh[0]),'Height':list(str_wh[1]),
                           'Distance_to_edges_hor':[str_e_hor_min[0],str_e_hor_mean[0],str_e_hor_max[0]],
                           'Distance_to_edges_vert':[str_e_vert_min[0],str_e_vert_mean[0],str_e_vert_max[0]],
                           'Distance_to_next':list(str_n_min[0])})
        door_file.write(str_3.to_frame().T.to_string()  + '\n')
        df_doors_new_famname = pd.concat([df_doors_new_famname,str_3.to_frame().T])

nameOfFile_csv = 'data\\tables\\doors_report_family.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_doors_new_famname.to_csv(completename_csv,index=False)

# analyse by families with frequency - completed
door_file.write('3. Analyse all doors by their family name and frequency \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_doors_new_famname_fr = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_doors_sorted = df_doors.loc[df_doors['Element_uniqueId'].isin(uniqueid)]
    if len(df_doors_sorted)>0:
        dupl_width = find_frequency_value(df_door_sorted['Door_width'].values.tolist())
        if len(dupl_width)>1:
            dupl_width = [dupl_width[0]]
        dupl_height = find_frequency_value(df_door_sorted['Door_height'].values.tolist())
        if len(dupl_height)>1:
            dupl_height = [dupl_height[0]]
        dupl_hor_dis_min = find_frequency_value(df_door_sorted['Distance_to_edges_hor_mi'].values.tolist())
        if len(dupl_hor_dis_min)>1:
            dupl_hor_dis_min = dupl_hor_dis_min[0]
        else:
            dupl_hor_dis_min = dupl_hor_dis_min[0]
        dupl_hor_dis_max = find_frequency_value(df_door_sorted['Distance_to_edges_hor_ma'].values.tolist())
        if len(dupl_hor_dis_max)>1:
            dupl_hor_dis_max = dupl_hor_dis_max[1]
        else:
            dupl_hor_dis_max = dupl_hor_dis_max[0]
        dupl_ver_dis_min = find_frequency_value(df_door_sorted['Distance_to_edges_vert_mi'].values.tolist())
        if len(dupl_ver_dis_min)>1:
            dupl_ver_dis_min = dupl_ver_dis_min[0]
        else:
            dupl_ver_dis_min = dupl_ver_dis_min[0]
        dupl_ver_dis_max = find_frequency_value(df_door_sorted['Distance_to_edges_vert_ma'].values.tolist())
        if len(dupl_ver_dis_max)>1:
            dupl_ver_dis_max = dupl_ver_dis_max[1]
        else:
            dupl_ver_dis_max = dupl_ver_dis_max[0]
        dupl_next_dis_min = find_frequency_value(df_door_sorted['Distance_to_next_door_min'].values.tolist())
        if len(dupl_next_dis_min)>1:
            dupl_next_dis_min = dupl_next_dis_min[0]
        else:
            dupl_next_dis_min = dupl_next_dis_min[0]

        str_2 = pd.Series({'Room_name': key,'Width':dupl_width,'Height':dupl_height,
                           'Distance_to_edges_hor':[dupl_hor_dis_min,dupl_hor_dis_max],
                           'Distance_to_edges_vert':[dupl_ver_dis_min,dupl_ver_dis_max],
                           'Distance_to_next':[dupl_next_dis_min]})
        win_file.write(str_2.to_frame().T.to_string()  + '\n')
        df_doors_new_famname_fr = pd.concat([df_doors_new_famname_fr,str_2.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\doors_report_family_freq.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_doors_new_famname_fr.to_csv(completename_csv,index=False)
#
#
#
# WALLS - completed
# analyse walls all by category - completed
nameOfFile_txt = 'data\\tables\\walls_report.txt'
completename_txt = os.path.join(data_dir,nameOfFile_txt)
walls_file = open(completename_txt,'w+')
walls_file.write("Analyse walls \n")
walls_file.write('1. Analyse all walls (by category: Walls) \n')
df_walls_new_cat = pd.DataFrame()
str_wh = df_walls.agg({'Width':['min','mean','max'],'Height':['min','mean','max']}).T.values
str_dis_to_paral_min = df_walls.agg({'Distance_to_parall_mi':['min']}).values[0]
str_dis_to_paral_mean = df_walls.agg({'Distance_to_parall_mean':['mean']}).values[0]
str_dis_to_paral_max = df_walls.agg({'Distance_to_parall_ma':['max']}).values[0]
str_angle_min = df_walls.agg({'Angles_to_walls_mi':['min']}).values[0]
str_angle_mean = df_walls.agg({'Angles_to_walls_mean':['mean']}).values[0]
str_angle_max = df_walls.agg({'Angles_to_walls_ma':['max']}).values[0]
str_1 = pd.Series({'Category': 'Walls','Width':list(str_wh[0]),'Height':list(str_wh[1]),
                    'Distance_to_parall_walls':[str_dis_to_paral_min[0],str_dis_to_paral_mean[0],str_dis_to_paral_max[0]],
                    'Angles_to_walls':[str_angle_min[0],str_angle_mean[0],str_angle_max[0]]})
walls_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
df_walls_new_cat = pd.concat([df_walls_new_cat,str_1.to_frame().T],ignore_index=True)
nameOfFile_csv = 'data\\tables\\walls_report_category.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_walls_new_cat.to_csv(completename_csv,index=False)

# analyse by room names - completed
walls_file.write('2. Analyse all walls by room names \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_walls_new_roomname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_walls_sorted = df_walls.loc[df_walls['Element_uniqueId'].isin(uniqueid)]
    if len(df_walls_sorted)>0:
        str_wh = df_walls_sorted.agg({'Width':['min','mean','max'],'Height':['min','mean','max']}).T.values
        str_dis_to_paral_min = df_walls_sorted.agg({'Distance_to_parall_mi':['min']}).values[0]
        str_dis_to_paral_mean = df_walls_sorted.agg({'Distance_to_parall_mean':['mean']}).values[0]
        str_dis_to_paral_max = df_walls_sorted.agg({'Distance_to_parall_ma':['max']}).values[0]
        str_angle_min = df_walls_sorted.agg({'Angles_to_walls_mi':['min']}).values[0]
        str_angle_mean = df_walls_sorted.agg({'Angles_to_walls_mean':['mean']}).values[0]
        str_angle_max = df_walls_sorted.agg({'Angles_to_walls_ma':['max']}).values[0]
        str_1 = pd.Series({'Room_name': key,'Width':list(str_wh[0]),'Height':list(str_wh[1]),
                            'Distance_to_parall_walls':[str_dis_to_paral_min[0],str_dis_to_paral_mean[0],str_dis_to_paral_max[0]],
                            'Angles_to_walls':[str_angle_min[0],str_angle_mean[0],str_angle_max[0]]})
        walls_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
        df_walls_new_roomname = pd.concat([df_walls_new_roomname,str_1.to_frame().T],ignore_index=True)   
nameOfFile_csv = 'data\\tables\\walls_report_roomname.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_walls_new_roomname.to_csv(completename_csv,index=False)

# analyse by room names - completed
walls_file.write('3. Analyse all walls by their family name \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_wall_new_famname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_walls_sorted = df_walls.loc[df_walls['Element_uniqueId'].isin(uniqueid)]
    if len(df_walls_sorted)>0:
        str_wh = df_walls_sorted.agg({'Width':['min','mean','max'],'Height':['min','mean','max']}).T.values
        str_dis_to_paral_min = df_walls_sorted.agg({'Distance_to_parall_mi':['min']}).values[0]
        str_dis_to_paral_mean = df_walls_sorted.agg({'Distance_to_parall_mean':['mean']}).values[0]
        str_dis_to_paral_max = df_walls_sorted.agg({'Distance_to_parall_ma':['max']}).values[0]
        str_angle_min = df_walls_sorted.agg({'Angles_to_walls_mi':['min']}).values[0]
        str_angle_mean = df_walls_sorted.agg({'Angles_to_walls_mean':['mean']}).values[0]
        str_angle_max = df_walls_sorted.agg({'Angles_to_walls_ma':['max']}).values[0]
        str_1 = pd.Series({'Family': key,'Width':list(str_wh[0]),'Height':list(str_wh[1]),
                            'Distance_to_parall_walls':[str_dis_to_paral_min[0],str_dis_to_paral_mean[0],str_dis_to_paral_max[0]],
                            'Angles_to_walls':[str_angle_min[0],str_angle_mean[0],str_angle_max[0]]})
        walls_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
        df_wall_new_famname = pd.concat([df_wall_new_famname,str_1.to_frame().T],ignore_index=True)   
nameOfFile_csv = 'data\\tables\\walls_report_family.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_wall_new_famname.to_csv(completename_csv,index=False)
#
#
#
# FLOORS
# analyse floors all by category - completed
nameOfFile_txt = 'data\\tables\\floors_report.txt'
completename_txt = os.path.join(data_dir,nameOfFile_txt)
floors_file = open(completename_txt,'w+')
floors_file.write("Analyse floors \n")
floors_file.write('1. Analyse all floors (by category: Floors) \n')
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
                   'Distance_to_nonparallel': [round(min(col1_new),3),round(statistics.mean(col1_new),3),round(max(col1_new),3)],
                    'Distance_to_parallel':[round(min(col2_new),3),round(statistics.mean(col2_new),3),round(max(col2_new),3)] })
floors_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
df_floors_new_cat = pd.concat([df_floors_new_cat,str_1.to_frame().T],ignore_index=True)
nameOfFile_csv = 'data\\tables\\floors_report_category.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_floors_new_cat.to_csv(completename_csv,index=False)

# analyse by room names - completed
floors_file.write('2. Analyse all floors by room names \n')
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
                        'Distance_to_nonparallel': [round(min(col1_new),3),round(statistics.mean(col1_new),3),round(max(col1_new),3)],
                            'Distance_to_parallel':[round(min(col2_new),3),round(statistics.mean(col2_new),3),round(max(col2_new),3)] })
        floors_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
        df_floors_new_roomname = pd.concat([df_floors_new_roomname,str_1.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\floors_report_roomname.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_floors_new_roomname.to_csv(completename_csv,index=False)

# analyse by family names - completed
floors_file.write('3. Analyse all floors by their family name \n')
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
                        'Distance_to_nonparallel': [round(min(col1_new),3),round(statistics.mean(col1_new),3),round(max(col1_new),3)],
                            'Distance_to_parallel':[round(min(col2_new),3),round(statistics.mean(col2_new),3),round(max(col2_new),3)] })
        floors_file.write(str_1.to_frame().T.to_string(index = False) + '\n')
        df_floors_new_famname = pd.concat([df_floors_new_famname,str_1.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\floors_report_family.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_floors_new_famname.to_csv(completename_csv,index=False)
#
#
#
# FURNITURE - OK
# analyse furniture all by category
nameOfFile_txt = 'data\\tables\\furniture_report.txt'
completename_txt = os.path.join(data_dir,nameOfFile_txt)
furniture_file = open(completename_txt,'w+')
furniture_file.write("Analyse furniture \n")
furniture_file.write('1. Analyse all furniture (by category: Furniture) \n')
df_furniture_new_cat = pd.DataFrame()
str_wh = df_furniture.agg({'Distance_to_nearest_mi':['mean'],
                          'Distance_to_nearest_mean':['mean'],
                          'Distance_to_nearest_ma':['mean']}).values[0].tolist()

str_1 = pd.Series({'Category':'Furniture',
                    'Distance_to_nearest':str_wh})
furniture_file.write(str_1.to_frame().T.to_string()  + '\n')
df_furniture_new_cat = pd.concat([df_furniture_new_cat,str_1.to_frame().T],ignore_index=True)
nameOfFile_csv = 'data\\tables\\furniture_report_category.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_furniture_new_cat.to_csv(completename_csv,index=False)

# analyse by room names - completed
furniture_file.write('2. Analyse all furniture by room names \n')
df_elements_groped = df_elements.groupby('Room_name')
df_elements_keys = df_elements_groped.groups.keys()
df_furniture_new_roomname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_furniture_sorted = df_furniture.loc[df_furniture['Element_uniqueId'].isin(uniqueid)]
    if len(df_furniture_sorted)>0:
        str_wh = df_furniture_sorted.agg({'Distance_to_nearest_mi':['mean'],
                          'Distance_to_nearest_mean':['mean'],
                          'Distance_to_nearest_ma':['mean']}).values[0].tolist()
        str_1 = pd.Series({'Room_name': key,
                            'Distance_to_nearest':str_wh})
        furniture_file.write(str_1.to_frame().T.to_string()  + '\n')
        df_furniture_new_roomname = pd.concat([df_furniture_new_roomname,str_1.to_frame().T],ignore_index=True)

nameOfFile_csv = 'data\\tables\\furniture_report_roomname.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_furniture_new_roomname.to_csv(completename_csv,index=False)

# analyse by family names - completed
furniture_file.write('3. Analyse all furniture by their family name \n')
df_elements_groped = df_elements.groupby('Family')
df_elements_keys = df_elements_groped.groups.keys()
df_furniture_new_famname = pd.DataFrame()
for key in df_elements_keys:
    df_elements_gr = df_elements_groped.get_group(key)
    uniqueid = df_elements_gr['Element_uniqueId'].values
    df_furniture_sorted = df_furniture.loc[df_furniture['Element_uniqueId'].isin(uniqueid)]
    if len(df_furniture_sorted)>0:
        str_wh = df_furniture_sorted.agg({'Distance_to_nearest_mi':['mean'],
                                            'Distance_to_nearest_mean':['mean'],
                                            'Distance_to_nearest_ma':['mean']}).values[0].tolist()
        str_1 = pd.Series({'Family': key,
                            'Distance_to_nearest':str_wh})
        furniture_file.write(str_1.to_frame().T.to_string()  + '\n')
        df_furniture_new_famname = pd.concat([df_furniture_new_famname,str_1.to_frame().T],ignore_index=True)


nameOfFile_csv = 'data\\tables\\furniture_report_family.csv'
completename_csv = os.path.join(data_dir,nameOfFile_csv)
df_furniture_new_famname.to_csv(completename_csv,index=False)
t.Commit()