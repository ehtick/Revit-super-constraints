
# import numpy as np
# import pandas as pd
import os
from pyrevit.forms import WPFWindow
import csv
import json
import ast
from System.Windows.Forms import OpenFileDialog
from System.Collections.Generic import List

class ModalForm(WPFWindow):

    def __init__(self,xaml_filename):
        WPFWindow.__init__(self,xaml_filename)
        self.ShowDialog()
        self.str_tail = None


    def fill_listbox(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(directory)))))
        name_file = 'data\\tables\\windows_report_roomname.csv'
        complete_name = os.path.join(path,name_file)
        list_trend = []
        with open(complete_name) as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    column_names = {",".join(row)}
                    line_count += 1
                else:
                    str_1 = "All windows in room named " + row[0] + " have min distance to edges " + row[4] + " m,"" have mean distance to edges " + row[5] + " m,"+ " have max distance to edges " +  row[6] + " m."
                    str_2 = "All windows in room named " + row[0] + " have min distance to next windows " +  row[7] + " m."
                    # self.lb_trends.Items.Add(str_1)
                    # self.lb_trends.Items.Add(str_2)
                    list_trend.append(str_1)
                    list_trend.append(str_2)
        return list_trend

    def open_and_load(self,sender,args):
        dialog = OpenFileDialog()
        dialog.Filter = "Csv files (*.csv)|*.csv|All files (*.*)|*.*"
        dialog.Title = 'Select file to represent trends.'
        if dialog.ShowDialog():
            name_file = dialog.FileName
        
        head, tail = os.path.split(name_file)

        # directory = os.path.dirname(os.path.abspath(__file__))
        # path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(directory)))))
        # name_file = 'data\\tables\\windows_report_roomname.csv'
        # complete_name = os.path.join(path,name_file)
        complete_name = name_file
        list_trend = []
        with open(complete_name) as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    column_names = {",".join(row)}
                    line_count += 1
                else:
                    if 'windows' in tail: #completed
                        if 'roomname' in tail:
                            # dis_width = json.loads(row[1])
                            # dis_height = json.loads(row[2])
                            # dis_edges_hor = json.loads(row[3])
                            # dis_edges_vert = json.loads(row[4])
                            # dis_next = json.loads(row[5])
                            str_1 = "All windows in the room called " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            str_2 = "All windows in the room called " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All windows in the room called " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All windows in the room called " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All windows in the room called " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next windows."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)

                        elif 'category' in tail:
                            str_1 = "All windows in the category " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            str_2 = "All windows in the category " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All windows in the category " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All windows in the category " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All windows in the category " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next windows."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)

                        elif 'family' in tail:
                            str_1 = "All windows of the family " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            str_2 = "All windows of the family " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All windows of the family " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All windows of the family " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All windows of the family " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next windows."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)
                    if 'doors' in tail:#completed
                        if 'roomname' in tail:
                            str_1 = "All doors in the room called " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            str_2 = "All doors in the room called " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All doors in the room called " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All doors in the room called " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All doors in the room called " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next doors."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)
                            
                        elif 'category' in tail:
                            str_1 = "All doors in the category " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            str_2 = "All doors in the category " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All doors in the category " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All doors in the category " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All doors in the category " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next doors."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)

                        elif 'family' in tail:
                            str_1 = "All doors of the family " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            str_2 = "All doors of the family " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All doors of the family " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All doors of the family " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All doors of the family " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next doors."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)
                    if 'walls' in tail:#completed
                        if 'roomname' in tail:
                            str_1 = "All walls in the room called " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            str_2 = "All walls in the room called " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All walls in the room called " + row[0] + " have [min,mean,max] " + row[3]  + " distance to parallel walls."
                            str_4 = "All walls in the room called " + row[0] + " have [min,mean,max] " + row[4]  + " angles to the walls."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                        elif 'category' in tail:
                            str_1 = "All walls in the category " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            str_2 = "All walls in the category " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All walls in the category " + row[0] + " have [min,mean,max] " + row[3]  + " distance to parallel walls."
                            str_4 = "All walls in the category " + row[0] + " have [min,mean,max] " + row[4]  + " angles to the walls."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                        elif 'family' in tail:
                            str_1 = "All walls of the family " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            str_2 = "All walls of the family " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All walls of the family " + row[0] + " have [min,mean,max] " + row[3]  + " distance to parallel walls."
                            str_4 = "All walls of the family " + row[0] + " have [min,mean,max] " + row[4]  + " angles to the walls."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                    if 'floors' in tail:#completed
                        if 'roomname' in tail:
                            str_1 = "All floors in the room called " + row[0] + " have [min,mean,max] " + row[1] + " distance to nonparallel floors."
                            str_2 = "All floors in the room called " + row[0] + " have [min,mean,max] " + row[2]  + " distance to paralel floors."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                        elif 'category' in tail:
                            str_1 = "All floors in the category " + row[0] + " have [min,mean,max] " + row[1] + " distance to nonparallel floors."
                            str_2 = "All floors in the category " + row[0] + " have [min,mean,max] " + row[2]  + " distance to paralel floors."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                        elif 'family' in tail:
                            str_1 = "All floors of the family " + row[0] + " have [min,mean,max] " + row[1] + " distance to nonparallel floors."
                            str_2 = "All floors of the family " + row[0] + " have [min,mean,max] " + row[2]  + " distance to paralel floors."
                            
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                    if 'furniture' in tail:#completed
                        if 'roomname' in tail:
                            str_1 = "All furniture in the room called " + row[0] + " have [min,mean,max] " + row[1] + " distances to nearest wall or floor."
                            
                            self.lb_trends.Items.Add(str_1)
                        elif 'category' in tail:
                            str_1 = "All furniture in the category " + row[0] + " have [min,mean,max] " + row[1] + " distances to nearest wall or floor."
                            
                            self.lb_trends.Items.Add(str_1)
                        elif 'family' in tail:
                            str_1 = "All furniture of the family " + row[0] + " have [min,mean,max] " + row[1] + " distances to nearest wall or floor."
                            
                            self.lb_trends.Items.Add(str_1)

    def convert_trend(self,sender,args):
        text = self.lb_trends.SelectedItem
        self.tb_constr.Text = str(text)
        # self.check_interval_closed.IsEnabled = False
        # self.check_interval_hop.IsEnabled = False
        # self.check_req.IsEnabled = False
        # self.check_cons.IsEnabled = False
        self.first_limit_p.Items.Add('min')
        self.first_limit_p.Items.Add('mean')
        self.first_limit_p.Items.Add('max')
        self.first_limit_p.Items.Add('unlimited')
        self.second_limit_p.Items.Add('min')
        self.second_limit_p.Items.Add('mean')
        self.second_limit_p.Items.Add('max')
        self.second_limit_p.Items.Add('unlimited')
    
    def text_changed_event_handler(self,sender,args):
        print(sender.Text)
    
    def all_words_present(self,words,sentence):
        for word in words:
            if word not in sentence:
                return False
        return True

    def recognize_key_words(self,sentence): # not necessary code
        # only works with windows
        elem_words = ['windows','doors','walls','floors','furniture']
        key_words = ['family','category','room named']
        meaning_words_20 = ['edges','vertical','min','max']
        meaning_words_30 = ['edges','horizontal','min','max']
        meaning_words_40 = ['next','min']
        loop_words = [meaning_words_20,meaning_words_30,meaning_words_40]
        sentence_words = []
        for rec in elem_words:
            if rec in sentence:
                sentence_words.append(rec)
                for key in key_words:
                    if key in sentence:
                        sentence_words.append(key)
                        for words in loop_words:
                            if self.all_words_present(words,sentence):
                                sentence_words.append(words)
        return sentence_words
    
    def add_type(self):
        if self.check_interval_closed.IsChecked == True:
            add_word = '"requirements"'
        elif self.check_cons.IsChecked == True:
            add_word = '"conseptual"'
        else:
            add_word = ''
        return add_word
    
    def interval_check(self,values):
        f_val = values[0]
        s_val = values[2]
        int_info = '"closed interval"'
        if self.check_interval_closed.IsChecked == True:
            int_info = '"closed interval"'
            first_int = self.first_limit_p.SelectedItem.ToString()
            second_int = self.second_limit_p.SelectedItem.ToString()
            if first_int == 'min':
                f_val = values[0]
            elif first_int == 'mean':
                f_val = values[1]
            elif first_int == 'max':
                f_val = values[2]
            else:
                f_val = 'inf'    
            if second_int == 'min':
                s_val = values[0]
            elif second_int == 'mean':
                s_val = values[1]
            elif second_int == 'max':
                s_val = values[2]
            else:
                s_val = 'inf'   
        if self.check_interval_hop.IsChecked == True:
            int_info = '"half-open interval"'
            first_int = self.first_limit_p.SelectedItem.ToString()
            second_int = self.second_limit_p.SelectedItem.ToString()
            if first_int == 'min':
                f_val = values[0]
            elif first_int == 'mean':
                f_val = values[1]
            elif first_int == 'max':
                f_val = values[2]
            else:
                f_val = 'inf'    
            if second_int == 'min':
                s_val = values[0]
            elif second_int == 'mean':
                s_val = values[1]
            elif second_int == 'max':
                s_val = values[2]
            else:
                s_val = 'inf'  
        return [f_val,s_val,int_info]

    def cypher_transform(self):
        str_old = self.lb_trends.SelectedItem
        str_new = self.tb_constr.Text
        text_changed = False
        if str_old != str_new:
            text_changed = True
            str_old_arr = str_old.split()
            str_new_arr = str_new.split()
            min_idx = str_new_arr.index('min') + 1
            min_num = str_new_arr[min_idx]
            try:
                max_idx = str_new_arr.index('max') + 1
                max_num = str_new_arr[max_idx]
            except:
                pass
        sentence = self.tb_constr.Text
        constr_type = self.add_type()
        sentence_words = self.recognize_key_words(sentence)

        # find category
        elem_word = sentence_words[0]
        elem = " "
        if "windows" in str_new:
            if 'room called' in str_new and 'horizontal' in str_new:
                # do something
                str_splited = str_new.split("All windows in the room called")[1].split()
                i = 0
                room_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    room_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = json.loads(str_splited[i+3])
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Windows'"
                elem_2 = "MATCH (m)-[:DISTANCE_HOR]->(w) "
                constr_all = " SET n.constr_distance_horizontal_min= " + int_val[0] + ", n.constr_distance_horizontal_max=" + int_val[1] + ", n.constr_characteristics=" + int_val[2]
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_hor_max:"+int_val[1]+",distance_hor_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"

            if 'room called' in str_new and 'vertical' in str_new:
                # do something
                str_splited = str_new.split("All windows in the room called")[1].split()
                i = 0
                room_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    room_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = json.loads(str_splited[i+3])
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Windows'"
                elem_2 = "MATCH (m)-[:DISTANCE_VERT]->(w) "
                constr_all = " SET n.constr_distance_vertical_min= " + int_val[0] + ", n.constr_distance_vertical_max=" + int_val[1] + ", n.constr_characteristics=" + int_val[2]
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_vert_max:"+int_val[1]+",distance_vert_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"

            if 'room called' in str_new and 'next' in str_new:
                # do something
                str_splited = str_new.split("All windows in the room called")[1].split()
                i = 0
                room_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    room_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = json.loads(str_splited[i+3])
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Windows'"
                elem_2 = "MATCH (m)-[:DISTANCE_NEXT]->(w) "
                constr_all = " SET n.constr_distance_next_min= " + int_val[0] + ", n.constr_distance_next_max=" + int_val[1] + ", n.constr_characteristics=" + int_val[2]
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_next_max:"+int_val[1]+",distance_next_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            # if 'category' in str_new and 'horizontal' in str_new:
            #     # do something
            # if 'category' in str_new and 'vertical' in str_new:
            #     # do something
            # if 'category' in str_new and 'next' in str_new:
            #     # do something
            # if 'family' in str_new and 'horizontal' in str_new:
            #     # do something
            # if 'family' in str_new and 'vertical' in str_new:
            #     # do something
            # if 'family' in str_new and 'next' in str_new:
            #     # do something
        if "doors" in str_new:
            if 'room called' in str_new and 'horizontal' in str_new:
                str_splited = str_new.split("All doors in the room called")[1].split()
                i = 0
                room_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    room_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = json.loads(str_splited[i+3])
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Doors'"
                elem_2 = "MATCH (m)-[:DISTANCE_HOR]->(w) "
                constr_all = " SET n.constr_distance_horizontal_min= " + int_val[0] + ", n.constr_distance_horizontal_max=" + int_val[1] + ", n.constr_characteristics=" + int_val[2]
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_hor_max:"+int_val[1]+",distance_hor_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"

            if 'room called' in str_new and 'vertical' in str_new:
                str_splited = str_new.split("All doors in the room called")[1].split()
                i = 0
                room_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    room_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = json.loads(str_splited[i+3])
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Doors'"
                elem_2 = "MATCH (m)-[:DISTANCE_VERT]->(w) "
                constr_all = " SET n.constr_distance_vertical_min= " + int_val[0] + ", n.constr_distance_vertical_max=" + int_val[1] + ", n.constr_characteristics=" + int_val[2]
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_vert_max:"+int_val[1]+",distance_vert_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'room called' in str_new and 'next' in str_new:
                str_splited = str_new.split("All doors in the room called")[1].split()
                i = 0
                room_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    room_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = json.loads(str_splited[i+3])
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Doors'"
                elem_2 = "MATCH (m)-[:DISTANCE_NEXT]->(w) "
                constr_all = " SET n.constr_distance_next_min= " + int_val[0] + ", n.constr_distance_next_max=" + int_val[1] + ", n.constr_characteristics=" + int_val[2]
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_next_max:"+int_val[1]+",distance_next_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            # if 'category' in str_new and 'horizontal' in str_new:
            #     # do something
            # if 'category' in str_new and 'vertical' in str_new:
            #     # do something
            # if 'category' in str_new and 'next' in str_new:
            #     # do something
            # if 'family' in str_new and 'horizontal' in str_new:
            #     # do something
            # if 'family' in str_new and 'vertical' in str_new:
            #     # do something
            # if 'family' in str_new and 'next' in str_new:
            #     # do something
        if "walls" in str_new:
            if 'room called' in str_new and 'parallel' in str_new:
                str_splited = str_new.split("All walls in the room called")[1].split()
                i = 0
                room_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    room_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = str_splited[i+3:i+6]
                values_new = []
                for val in values:
                    val = val.replace('[',"")
                    val = val.replace(']',"")
                    print(val)
                    values_new.append(val)

                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Walls'"
                elem_2 = "MATCH (m)-[:DISTANCE_PAR]->(w) "
                constr_all = " SET n.constr_distance_to_parall_min= " + int_val[0] + "n.constr_distance_to_parallel_max=" + int_val[1] + ", n.constr_characteristics=" + int_val[2]
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_to_parallel_max:"+int_val[1]+",distance_to_parallel_min:"+ int_val[0] + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            # if 'room called' in str_new and 'angles' in str_new:
            #     # do something
            # if 'category' in str_new and 'parallel' in str_new:
            #     # do something
            # if 'category' in str_new and 'angles' in str_new:
            #     # do something
            # if 'family' in str_new and 'parallel' in str_new:
            #     # do something
            # if 'family' in str_new and 'angles' in str_new:
            #     # do something
        # if "floors" in str_new:
        #     if 'room called' in str_new and 'nonparallel' in str_new:
        #         # do something
        #     if 'room called' in str_new and 'parallel' in str_new:
        #         # do something
        #     if 'category' in str_new and 'nonparallel' in str_new:
        #         # do something
        #     if 'category' in str_new and 'parallel' in str_new:
        #         # do something
        #     if 'family' in str_new and 'nonparallel' in str_new:
        #         # do something
        #     if 'family' in str_new and 'parallel' in str_new:
        #         # do something
        # if 'furniture' in str_new:
            # if 'room called' in str_new:
            #     # do something
            # if 'category' in str_new:
            #     # do something
            # if 'family' in str_new:
            #     # do something


        # if elem_word == 'windows' or elem_word == 'doors':
        #     # elem = "MATCH (n:Element)-[:CONTAINS]->(m:Element) "
        #     # find how data was filtered
        #     key_word = sentence_words[1]
        #     if key_word == 'room named':
        #         elem = "MATCH (n:Element)-[:CONTAINS]->(m:Element) "
        #         key_word = 'named'
        #         sent_arr = sentence.split()
        #         named_idx = sent_arr.index(key_word)
        #         trans_1 = sent_arr[named_idx + 1]
        #         ind = 2
        #         while sent_arr[named_idx + ind] != 'have':
        #             trans_1 += " " + sent_arr[named_idx + 2]
        #             ind += 1
        #         cc_1 = trans_1
        #         if elem_word == 'windows':
        #             trans_1 = " WHERE n.room_name = "+ '"'+trans_1+'"' +" AND m.category = 'Windows'"
        #         else:
        #             trans_1 = " WHERE n.room_name = "+ '"'+trans_1+'"' +" AND m.category = 'Doors'"
        #     if key_word == 'category':
        #         elem = "MATCH (n:Element) "
        #         if elem_word == 'windows':
        #             trans_1 = " WHERE n.category = 'Windows'"
        #         if elem_word == 'doors':
        #             trans_1 = " WHERE n.category = 'Doors'"
        #     if key_word == 'family':
        #         key_word = 'family'
        #         sent_arr = sentence.split()
        #         named_idx = sent_arr.index(key_word)
        #         trans_1 = sent_arr[named_idx + 1]
        #         ind = 2
        #         while sent_arr[named_idx + ind] != 'have':
        #             trans_1 += " " + sent_arr[named_idx + 2]
        #             ind += 1
        #         if elem_word == 'windows':
        #             trans_1 = " WHERE n.family_name = "+ '"'+trans_1+'"' +" AND m.category = 'Windows'"
        #         else:
        #             trans_1 = " WHERE n.family_name = "+ '"'+trans_1+'"' +" AND m.category = 'Doors'"
            
            # find what kind of attributes was used
            # attr_words = sentence_words[2]
            # constr_all = " "
            # constr_max = " "
            # constr_min = " "
            # print(attr_words[3])
            # for att in attr_words:
            #     if att == "vertical":
            #         if attr_words[2] == 'min':
            #             min_idx = sent_arr.index('min') + 1
            #             min_num = sent_arr[min_idx]
            #             constr_min = "constr_distance_vertical_min= " + min_num
            #             cc_21 = "'Distance_to_edges_vert_mi' ="+min_num
            #         if attr_words[3] == 'max':
            #             max_idx = sent_arr.index('max') + 1
            #             max_num = sent_arr[max_idx]
            #             # find vertical element that has whis distance
            #             constr_max = "constr_distance_vertical_max= " + max_num
            #             cc_22 = "'Distance_to_edges_vert_ma' = " + max_num
            #         constr_all = " SET n." + constr_min +", n."+ constr_max
            #         elem_2 = "MATCH (m:Element)-[:DISTANCE_VERT]->(w:Element) "
            #         constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_vert_max:"+max_num+",distance_vert_min:"+ min_num + ", " + "constraint_type: " + constr_type +"}]->(w) "
            #         ret_1 = "RETURN k,m"
            #         if text_changed:
            #             cc_2 = cc_21 + "," + cc_22
            #         else:
            #             cc_2 = ""
            #     if att == "horizontal":
            #         if attr_words[2] == 'min':
            #             min_idx = sent_arr.index('min') + 1
            #             min_num = sent_arr[min_idx]
            #             print(min_num)
            #             constr_min = "constr_distance_horizontal_min= " + min_num
            #             cc_21 = "'Distance_to_edges_hor_mi' ="+min_num
            #         if attr_words[3] == 'max':
            #             max_idx = sent_arr.index('max') + 1
            #             max_num = sent_arr[max_idx]
            #             print("test")
            #             # find vertical element that has whis distance
            #             constr_max = "constr_distance_horizontal_max= " + max_num
            #             cc_22 = "'Distance_to_edges_hor_ma' = " + max_num
            #         constr_all = " SET n." + constr_min + ", n." + constr_max
            #         elem_2 = "MATCH (m:Element)-[:DISTANCE_HOR]->(w:Element) "
            #         constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_hor_max:"+max_num+",distance_hor_min:"+ min_num + ", " + "constraint_type: " + constr_type +"}]->(w) "
            #         ret_1 = "RETURN k,m"
            #         if text_changed:
            #             cc_2 = cc_21 + "," + cc_22
            #         else:
            #             cc_2 = ""
            #     if att == "next":
            #         if attr_words[1] == 'min':
            #             min_idx = sent_arr.index('min') + 1
            #             min_num = sent_arr[min_idx]
            #             constr_all = " SET n.constr_distance_next_window_min = " + min_num
            #             constr_create = "MERGE (m)-[k:CONSTRAINTS{distance_next_window_min:"+min_num + ", " + "constraint_type: " + constr_type +"}]->(w)"
            #             if text_changed and elem_word == 'windows':
            #                 cc_2 = "'Distance_to_next_win_min' ="+min_num
            #             else:
            #                 cc_2 = ""
            #             if text_changed and elem_word == 'doors':
            #                 cc_2 = "'Distance_to_next_door_min' ="+min_num
            #             else:
            #                 cc_2 = ""
            
            # transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            # if text_changed:
            #     controll_changes = elem_word + ", " + cc_1 + "," + cc_2
            #     self.write_changes(controll_changes)
        return transformation
    
    def write_changes(self, controll_changes):
        directory = os.path.dirname(os.path.abspath(__file__))
        # data directory for filter categories
        data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(directory)))))
        nameOfFile_txt = 'data\\tables\\windows_controll_changes.txt'
        completename_txt = os.path.join(data_dir,nameOfFile_txt)
        if os.path.exists(completename_txt):
            with open(completename_txt,'a') as f:
                f.write(controll_changes +" \n")
                f.write('\n')
                f.write('\n')
                f.close()
        else:
            with open(completename_txt,'w+') as f:
                f.write(controll_changes +" \n")
                f.write('\n')
                f.write('\n')
                f.close()

    def apply_constraint(self,sender,args):
        directory = os.path.dirname(os.path.abspath(__file__))
        # data directory for filter categories
        data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(directory)))))
        nameOfFile_txt = 'data\\tables\\windows_cypher_transf.txt'
        completename_txt = os.path.join(data_dir,nameOfFile_txt)
        cp_transf = self.cypher_transform()
        # print(cp_transf)
        # print(os.path.exists(completename_txt))
        add_word = self.add_type()
        if os.path.exists(completename_txt):
            with open(completename_txt,'a') as f:
                f.write("Cypher transformation of: " + self.tb_constr.Text + ", "+ add_word +" \n")
                f.write(cp_transf)
                f.write('\n')
                f.write('\n')
                f.close()
        else:
            with open(completename_txt,'w+') as f:
                f.write("Cypher transformation of: " + self.tb_constr.Text +", "+ add_word +" \n")
                f.write(cp_transf)
                f.write('\n')
                f.write('\n')
                f.close()
                    

form = ModalForm("interface.xaml")