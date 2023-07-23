
import os
from pyrevit.forms import WPFWindow
import csv
import json
import ast
from System.Windows.Forms import OpenFileDialog


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
        return list_trend

    def open_and_load(self,sender,args):
        dialog = OpenFileDialog()
        dialog.Filter = "Csv files (*.csv)|*.csv|All files (*.*)|*.*"
        dialog.Title = 'Select file to represent trends.'
        if dialog.ShowDialog():
            name_file = dialog.FileName
        
        head, tail = os.path.split(name_file)
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
                            # str_1 = "All windows in the room called " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            # str_2 = "All windows in the room called " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All windows in the room called " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All windows in the room called " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All windows in the room called " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next windows."
                            
                            # self.lb_trends.Items.Add(str_1)
                            # self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)

                        elif 'category' in tail:
                            # str_1 = "All windows in the category " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            # str_2 = "All windows in the category " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All windows in the category " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All windows in the category " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All windows in the category " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next windows."
                            
                            # self.lb_trends.Items.Add(str_1)
                            # self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)

                        elif 'family' in tail:
                            # str_1 = "All windows of the family " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            # str_2 = "All windows of the family " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All windows of the family " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All windows of the family " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All windows of the family " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next windows."
                            
                            # self.lb_trends.Items.Add(str_1)
                            # self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)
                    if 'doors' in tail:#completed
                        if 'roomname' in tail:
                            # str_1 = "All doors in the room called " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            # str_2 = "All doors in the room called " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All doors in the room called " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All doors in the room called " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All doors in the room called " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next doors."
                            
                            # self.lb_trends.Items.Add(str_1)
                            # self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)
                            
                        elif 'category' in tail:
                            # str_1 = "All doors in the category " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            # str_2 = "All doors in the category " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All doors in the category " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All doors in the category " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All doors in the category " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next doors."
                            
                            # self.lb_trends.Items.Add(str_1)
                            # self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)

                        elif 'family' in tail:
                            # str_1 = "All doors of the family " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            # str_2 = "All doors of the family " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All doors of the family " + row[0] + " have [min,mean,max] " + row[3]  + " horizontal distances to edges."
                            str_4 = "All doors of the family " + row[0] + " have [min,mean,max] " + row[4]  + " vertical distances to edges."
                            str_5 = "All doors of the family " + row[0] + " have [min,mean,max] " + row[5]  + " distance to next doors."
                            
                            # self.lb_trends.Items.Add(str_1)
                            # self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                            self.lb_trends.Items.Add(str_5)
                    if 'walls' in tail:#completed
                        if 'roomname' in tail:
                            # str_1 = "All walls in the room called " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            # str_2 = "All walls in the room called " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All walls in the room called " + row[0] + " have [min,mean,max] " + row[3]  + " distance to parallel walls."
                            str_4 = "All walls in the room called " + row[0] + " have [min,mean,max] " + row[4]  + " angles to the walls."
                            
                            # self.lb_trends.Items.Add(str_1)
                            # self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                        elif 'category' in tail:
                            # str_1 = "All walls in the category " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            # str_2 = "All walls in the category " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All walls in the category " + row[0] + " have [min,mean,max] " + row[3]  + " distance to parallel walls."
                            str_4 = "All walls in the category " + row[0] + " have [min,mean,max] " + row[4]  + " angles to the walls."
                            
                            # self.lb_trends.Items.Add(str_1)
                            # self.lb_trends.Items.Add(str_2)
                            self.lb_trends.Items.Add(str_3)
                            self.lb_trends.Items.Add(str_4)
                        elif 'family' in tail:
                            # str_1 = "All walls of the family " + row[0] + " have [min,mean,max] " + row[1] + " width."
                            # str_2 = "All walls of the family " + row[0] + " have [min,mean,max] " + row[2]  + " height."
                            str_3 = "All walls of the family " + row[0] + " have [min,mean,max] " + row[3]  + " distance to parallel walls."
                            str_4 = "All walls of the family " + row[0] + " have [min,mean,max] " + row[4]  + " angles to the walls."
                            
                            # self.lb_trends.Items.Add(str_1)
                            # self.lb_trends.Items.Add(str_2)
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
        self.first_limit_p.Items.Add('min')
        self.first_limit_p.Items.Add('mean')
        self.first_limit_p.Items.Add('max')
        self.first_limit_p.Items.Add('inf')
        self.second_limit_p.Items.Add('min')
        self.second_limit_p.Items.Add('mean')
        self.second_limit_p.Items.Add('max')
        self.second_limit_p.Items.Add('inf')
    
    def text_changed_event_handler(self,sender,args):
        print(sender.Text)
    
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
        str_new = self.tb_constr.Text
        transformation = 'This part is not implemented yet.'
        if "windows" in str_new:
            if 'room called' in str_new and 'horizontal' in str_new:
                str_splited = str_new.split("All windows in the room called")[1].split()
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
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Windows'"
                elem_2 = "MATCH (m)-[:DISTANCE_HOR]->(w) "
                constr_all = " SET n.constr_distance_horizontal_min= " + int_val[0] + ", n.constr_distance_horizontal_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_hor_max:"+int_val[1]+",distance_hor_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"

            if 'room called' in str_new and 'vertical' in str_new:
                str_splited = str_new.split("All windows in the room called")[1].split()
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
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Windows'"
                elem_2 = "MATCH (m)-[:DISTANCE_VERT]->(w) "
                constr_all = " SET n.constr_distance_vertical_min= " + int_val[0] + ", n.constr_distance_vertical_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_vert_max:"+int_val[1]+",distance_vert_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"

            if 'room called' in str_new and 'next' in str_new:
                str_splited = str_new.split("All windows in the room called")[1].split()
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
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Windows'"
                elem_2 = "MATCH (m)-[:DISTANCE_NEXT]->(w) "
                constr_all = " SET n.constr_distance_next_min= " + int_val[0] + ", n.constr_distance_next_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_next_max:"+int_val[1]+",distance_next_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'category' in str_new and 'horizontal' in str_new:
                str_splited = str_new.split("All windows in the category")[1].split()
                i = 0
                category = str_splited[i]
                while  str_splited[i+1] != 'have':
                    category = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = str_splited[i+3:i+6]
                values_new = []
                for val in values:
                    val = val.replace('[',"")
                    val = val.replace(']',"")
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (m)-[:DISTANCE_HOR]->(w) "
                trans_1 = " WHERE m.category = 'Windows'"
                elem_2 = ""
                constr_all = " SET n.constr_distance_horizontal_min= " + int_val[0] + ", n.constr_distance_horizontal_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_hor_max:"+int_val[1]+",distance_hor_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'category' in str_new and 'vertical' in str_new:
                str_splited = str_new.split("All windows in the category")[1].split()
                i = 0
                category = str_splited[i]
                while  str_splited[i+1] != 'have':
                    category = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = str_splited[i+3:i+6]
                values_new = []
                for val in values:
                    val = val.replace('[',"")
                    val = val.replace(']',"")
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (m)-[:DISTANCE_VERT]->(w) "
                trans_1 = " WHERE m.category = 'Windows'"
                elem_2 = ""
                constr_all = " SET n.constr_distance_vertical_min= " + int_val[0] + ", n.constr_distance_vertical_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_vert_max:"+int_val[1]+",distance_vert_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'category' in str_new and 'next' in str_new:
                str_splited = str_new.split("All windows in the category")[1].split()
                i = 0
                category = str_splited[i]
                while  str_splited[i+1] != 'have':
                    category = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = str_splited[i+3:i+6]
                values_new = []
                for val in values:
                    val = val.replace('[',"")
                    val = val.replace(']',"")
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (m)-[:DISTANCE_NEXT]->(w) "
                trans_1 = " WHERE m.category = 'Windows'"
                elem_2 = ""
                constr_all = " SET n.constr_distance_next_min= " + int_val[0] + ", n.constr_distance_next_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_next_max:"+int_val[1]+",distance_next_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'family' in str_new and 'horizontal' in str_new:
                str_splited = str_new.split("All windows of the family")[1].split()
                i = 0
                fam_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    fam_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = str_splited[i+3:i+6]
                values_new = []
                for val in values:
                    val = val.replace('[',"")
                    val = val.replace(']',"")
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (m)-[:DISTANCE_HOR]->(w) "
                trans_1 = " WHERE m.family_name = " + '"'+fam_name+'"'
                elem_2 = ""
                constr_all = " SET n.constr_distance_horizontal_min= " + int_val[0] + ", n.constr_distance_horizontal_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_hor_max:"+int_val[1]+",distance_hor_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'family' in str_new and 'vertical' in str_new:
                str_splited = str_new.split("All windows of the family")[1].split()
                i = 0
                fam_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    fam_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = str_splited[i+3:i+6]
                values_new = []
                for val in values:
                    val = val.replace('[',"")
                    val = val.replace(']',"")
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (m)-[:DISTANCE_VERT]->(w) "
                trans_1 = " WHERE m.family_name = " + '"'+fam_name+'"'
                elem_2 = ""
                constr_all = " SET n.constr_distance_vertical_min= " + int_val[0] + ", n.constr_distance_vertical_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_vert_max:"+int_val[1]+",distance_vert_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'family' in str_new and 'next' in str_new:
                str_splited = str_new.split("All windows of the family")[1].split()
                i = 0
                fam_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    fam_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = str_splited[i+3:i+6]
                values_new = []
                for val in values:
                    val = val.replace('[',"")
                    val = val.replace(']',"")
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (m)-[:DISTANCE_NEXT]->(w) "
                trans_1 = " WHERE m.category = " + '"'+fam_name+'"'
                elem_2 = ""
                constr_all = " SET n.constr_distance_next_min= " + int_val[0] + ", n.constr_distance_next_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_next_max:"+int_val[1]+",distance_next_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
        if "doors" in str_new:
            if 'room called' in str_new and 'horizontal' in str_new:
                str_splited = str_new.split("All doors in the room called")[1].split()
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
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Doors'"
                elem_2 = "MATCH (m)-[:DISTANCE_HOR]->(w) "
                constr_all = " SET n.constr_distance_horizontal_min= " + int_val[0] + ", n.constr_distance_horizontal_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_hor_max:"+int_val[1]+",distance_hor_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"

            if 'room called' in str_new and 'vertical' in str_new:
                str_splited = str_new.split("All doors in the room called")[1].split()
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
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Doors'"
                elem_2 = "MATCH (m)-[:DISTANCE_VERT]->(w) "
                constr_all = " SET n.constr_distance_vertical_min= " + int_val[0] + ", n.constr_distance_vertical_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_vert_max:"+int_val[1]+",distance_vert_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'room called' in str_new and 'next' in str_new:
                str_splited = str_new.split("All doors in the room called")[1].split()
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
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Doors'"
                elem_2 = "MATCH (m)-[:DISTANCE_NEXT]->(w) "
                constr_all = " SET n.constr_distance_next_min= " + int_val[0] + ", n.constr_distance_next_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_next_max:"+int_val[1]+",distance_next_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'category' in str_new and 'horizontal' in str_new:
                # do something
                print('This part is not implemented yet.') 
            if 'category' in str_new and 'vertical' in str_new:
                # do something
                print('This part is not implemented yet.') 
            if 'category' in str_new and 'next' in str_new:
                # do something
                print('This part is not implemented yet.') 
            if 'family' in str_new and 'horizontal' in str_new:
                # do something
                print('This part is not implemented yet.') 
            if 'family' in str_new and 'vertical' in str_new:
                # do something
                print('This part is not implemented yet.') 
            if 'family' in str_new and 'next' in str_new:
                # do something
                print('This part is not implemented yet.') 
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
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Walls'"
                elem_2 = "MATCH (m)-[:DISTANCE_PAR]->(w) "
                constr_all = " SET n.constr_distance_to_parall_min= " + int_val[0] + ", n.constr_distance_to_parallel_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_to_parallel_max:"+int_val[1]+",distance_to_parallel_min:"+ int_val[0] + ",constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'room called' in str_new and 'angles' in str_new:
                print('This part is not implemented yet.') 
            if 'category' in str_new and 'parallel' in str_new:
                print('This part is not implemented yet.') 
            if 'category' in str_new and 'angles' in str_new:
                print('This part is not implemented yet.') 
            if 'family' in str_new and 'parallel' in str_new:
                str_splited = str_new.split("All walls of the family")[1].split()
                i = 0
                fam_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    fam_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = str_splited[i+3:i+6]
                values_new = []
                for val in values:
                    val = val.replace('[',"")
                    val = val.replace(']',"")
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (m)-[:DISTANCE_PAR]->(w) "
                trans_1 = " WHERE m.family_name = " + '"'+fam_name+'"'
                elem_2 = ""
                constr_all = " SET n.constr_distance_to_parall_min= " + int_val[0] + ", n.constr_distance_to_parallel_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_to_parallel_max:"+int_val[1]+",distance_to_parallel_min:"+ int_val[0] + ",constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'family' in str_new and 'angles' in str_new:
                print('This part is not implemented yet.') 
        if "floors" in str_new:
            if 'room called' in str_new and 'nonparallel' in str_new:
                str_splited = str_new.split("All floors in the room called")[1].split()
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
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Floors'"
                elem_2 = "MATCH (m)-[:DISTANCE_NONPAR]->(w) "
                constr_all = " SET n.constr_distance_nonparall_min= " + int_val[0] + ", n.constr_distance_nonparall_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_nonparall_max:"+int_val[1]+",distance_nonparall_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'room called' in str_new and 'parallel' in str_new:
                str_splited = str_new.split("All floors in the room called")[1].split()
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
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"' +" AND m.category = 'Floors'"
                elem_2 = "MATCH (m)-[:DISTANCE_PAR]->(w) "
                constr_all = " SET n.constr_distance_parall_min= " + int_val[0] + ", n.constr_distance_parall_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_parall_max:"+int_val[1]+",distance_parall_min:"+ int_val[0] + ", " + "constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'category' in str_new and 'nonparallel' in str_new:
                print('This part is not implemented yet.') 
            if 'category' in str_new and 'parallel' in str_new:
                print('This part is not implemented yet.') 
            if 'family' in str_new and 'nonparallel' in str_new:
                print('This part is not implemented yet.') 
            if 'family' in str_new and 'parallel' in str_new:
                print('This part is not implemented yet.') 
        if 'furniture' in str_new:# completed
            if 'room called' in str_new:
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
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (n)-[:CONTAINS]->(m:Furniture) "
                trans_1 = " WHERE n.room_name = "+ '"'+room_name+'"'
                elem_2 = "MATCH (m)-[:DISTANCE_NEAREST]->(w) "
                constr_all = " SET n.constr_distance_to_nearest_min= " + int_val[0] + ",n.constr_distance_to_nearest_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_to_nearest_max:"+int_val[1]+",distance_to_nearest_min:"+ int_val[0] + ",constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'category' in str_new:
                str_splited = str_new.split("All walls of the family")[1].split()
                i = 0
                fam_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    fam_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = str_splited[i+3:i+6]
                values_new = []
                for val in values:
                    val = val.replace('[',"")
                    val = val.replace(']',"")
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (m:Furniture)-[:DISTANCE_NEAREST]->(w) "
                trans_1 = ""
                elem_2 = ""
                constr_all = " SET n.constr_distance_to_nearest_min= " + int_val[0] + ",n.constr_distance_to_nearest_max=" + int_val[1] + ", n.constr_characteristics=" + '"'+int_val[2]+'"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_to_nearest_max:"+int_val[1]+",distance_to_nearest_min:"+ int_val[0] + ",constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"
            if 'family' in str_new:
                str_splited = str_new.split("All walls of the family")[1].split()
                i = 0
                fam_name = str_splited[i]
                while  str_splited[i+1] != 'have':
                    fam_name = str_splited[i] + ' ' + str_splited[i+1]
                    i = i+1
                values = str_splited[i+3:i+6]
                values_new = []
                for val in values:
                    val = val.replace('[',"")
                    val = val.replace(']',"")
                    val = val.replace(',',"")
                    values_new.append(val)
                values = values_new
                int_val = self.interval_check(values)
                constr_type = self.add_type()
                elem = "MATCH (m)-[:DISTANCE_NEAREST]->(w) "
                trans_1 = " WHERE m.family_name = " + '"'+fam_name+'"'
                elem_2 = ""
                constr_all = " SET n.constr_distance_to_nearest_min= " + int_val[0] + ", n.constr_distance_to_nearest_max=" + int_val[1] + ", n.constr_characteristics= " +'"'+ int_val[2]+ '"'
                constr_create = " MERGE (m)-[k:CONSTRAINTS{distance_to_nearest_max:"+int_val[1]+",distance_to_nearest_min:"+ int_val[0] + ",constraint_type: " + constr_type +"}]->(w) "
                transformation = elem + elem_2 + trans_1 + constr_all + constr_create + " RETURN k,m"

        return transformation

    def apply_constraint(self,sender,args):
        directory = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(directory)))))
        nameOfFile_txt = 'data\\tables\\project_constraints_cypher_transf.txt'
        completename_txt = os.path.join(data_dir,nameOfFile_txt)
        cp_transf = self.cypher_transform()
        if cp_transf != 'This part is not implemented yet.':
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