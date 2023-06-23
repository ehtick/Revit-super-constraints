
# import numpy as np
# import pandas as pd
import os
from pyrevit.forms import WPFWindow
import csv
from System.Windows.Forms import OpenFileDialog

class ModalForm(WPFWindow):

    def __init__(self,xaml_filename):
        WPFWindow.__init__(self,xaml_filename)
        self.ShowDialog()

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
                    if 'windows' in tail:
                        if 'roomname' in tail:
                            str_1 = "All windows in the room named " + row[0] + " have min distance to edges " + row[4] + " m,"" have mean distance to edges " + row[5] + " m,"+ " have max distance to edges " +  row[6] + " m."
                            str_2 = "All windows in the room named " + row[0] + " have min distance to next windows " +  row[7] + " m."
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                        elif 'category' in tail:
                            str_1 = "All windows have min distance to edges " + row[4] + " m,"" have mean distance to edges " + row[5] + " m,"+ " have max distance to edges " +  row[6] + " m."
                            str_2 = "All windows have min distance to next windows " +  row[7] + " m."
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                        elif 'family' in tail:
                            str_1 = "All windows in the family  " + row[0] + " have min distance to edges " + row[4] + " m,"" have mean distance to edges " + row[5] + " m,"+ " have max distance to edges " +  row[6] + " m."
                            str_2 = "All windows in the family  " + row[0] + " have min distance to next windows " +  row[7] + " m."
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                    if 'doors' in tail:
                        if 'roomname' in tail:
                            str_1 = "All doors in the room named " + row[0] + " have min distance to edges " + row[4] + " m,"" have mean distance to edges " + row[5] + " m,"+ " have max distance to edges " +  row[6] + " m."
                            str_2 = "All doors in the room named " + row[0] + " have min distance to next windows " +  row[7] + " m."
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                        elif 'category' in tail:
                            str_1 = "All doors have min distance to edges " + row[4] + " m,"" have mean distance to edges " + row[5] + " m,"+ " have max distance to edges " +  row[6] + " m."
                            str_2 = "All doors have min distance to next windows " +  row[7] + " m."
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                        elif 'family' in tail:
                            str_1 = "All doors in the family  " + row[0] + " have min distance to edges " + row[4] + " m,"" have mean distance to edges " + row[5] + " m,"+ " have max distance to edges " +  row[6] + " m."
                            str_2 = "All doors in the family  " + row[0] + " have min distance to next windows " +  row[7] + " m."
                            self.lb_trends.Items.Add(str_1)
                            self.lb_trends.Items.Add(str_2)
                    if 'walls' in tail:
                        if 'roomname' in tail:
                            str_1 = "All walls in the room named " + row[0] + " have min distance to parallel walls  " + row[4] + " m,"" have mean distance to parallel walls " + row[5] + " m,"+ " have max distance to parallel walls " +  row[6] + " m."
                            self.lb_trends.Items.Add(str_1)
                        elif 'category' in tail:
                            str_1 = "All walls have min distance to parallel walls  " + row[4] + " m,"" have mean distance to parallel walls " + row[5] + " m,"+ " have max distance to parallel walls " +  row[6] + " m."
                            self.lb_trends.Items.Add(str_1)
                        elif 'family' in tail:
                            str_1 = "All walls in the family  " + row[0] + " have min distance to parallel walls  " + row[4] + " m,"" have mean distance to parallel walls " + row[5] + " m,"+ " have max distance to parallel walls " +  row[6] + " m."
                            self.lb_trends.Items.Add(str_1)
                    if 'floors' in tail:
                        if 'roomname' in tail:
                            str_1 = "All floors in the room named " + row[0] + " have min distance between each other " +  row[2] + " m."
                            self.lb_trends.Items.Add(str_1)
                        elif 'category' in tail:
                            str_1 = "All floors have max distance between each other " + row[1] + " m."
                            self.lb_trends.Items.Add(str_1)
                        elif 'family' in tail:
                            str_1 = "All floors in the family  " + row[0] + " have min distance between each other " +  row[2] + " m."
                            self.lb_trends.Items.Add(str_1)
                    if 'furniture' in tail:
                        if 'roomname' in tail:
                            str_1 = "All furniture in the room named " + row[0] + " have min distance to the room surface " + row[4] + " m,"" have mean to the room surface " + row[5] + " m,"+ " have max to the room surface " +  row[6] + " m."
                            self.lb_trends.Items.Add(str_1)
                        elif 'category' in tail:
                            str_1 = "All furniture have min distance to the room surface " + row[4] + " m,"" have mean distance to the room surface " + row[5] + " m,"+ " have max distance to the room surface " +  row[6] + " m."
                            self.lb_trends.Items.Add(str_1)
                        elif 'family' in tail:
                            str_1 = "All furniture in the family  " + row[0] + " have min distance to the room surface " + row[4] + " m,"" have mean to the room surface " + row[5] + " m,"+ " have max to the room surface " +  row[6] + " m."
                            self.lb_trends.Items.Add(str_1)


    def convert_trend(self,sender,args):
        text = self.lb_trends.SelectedItem
        self.tb_constr.Text = str(text)

    def apply_constraint(self,sender,args):
        if self.check_limit.IsChecked == True:
            str_old = self.tb_constr.Text
            # recognize min and max
            
        pass
        

form = ModalForm("interface.xaml")