#! python3
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import pandas as pd
from Autodesk.Revit.UI import (TaskDialog, TaskDialogCommonButtons,
                               TaskDialogCommandLinkId, TaskDialogResult)


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def load_data(self,filename):
        # delete all previos data
        # ask user if he will update or delete all data
        title = "Update or delete"
        dialog = TaskDialog(title)
        dialog.MainInstruction = "Do you want delete previous nodes and relationships?"
        dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
        result = dialog.Show()
        if result == TaskDialogResult.Yes:
            self.driver.execute_query("MATCH (n) DETACH DELETE n")
        
        data = pd.read_csv(filename)
        df = pd.DataFrame(data)
        rooms = df.groupby('Room_Id').groups.keys()

        nameOfFile_csv = 'space_elements_furniture.csv'
        completename_csv = 'D:/Bachelor_thesis/super-constraints/data/tables/' + nameOfFile_csv
        data = pd.read_csv(completename_csv)
        df_furn_dist = pd.DataFrame(data)

        # think about how to add name to the node
        # it should be in the table
        for index, row in df.iterrows():
            query_space = self.driver.execute_query("MERGE (s:Space {name: 'Space', id: $id_s})",id_s = row['Room_Id'], database = "neo4j").summary
            # query_element = self.driver.execute_query("MERGE (e:Element {name: 'Element', id: $id, family: $family})",
            #                                             id = row['ElementId'],
            #                                             family = row['Family'],
            #                                             database = "neo4j").summary
            # query_sum = self.driver.execute_query("""MATCH (e:Element {name: 'Element',id: $id, family: $family})
            #                                         MATCH (s:Space {id: $id_s})
            #                                         MERGE (s)-[:CONTAINS]->(e)""",
            #                                         id_s = row['Selected_roomI_Id'],
            #                                         id = row['ElementId'],
            #                                         family = row['Family'],
            #                                         database = "neo4j").summary
    #     m = int(len(df_furn_dist.columns)/2)
    #     for index, row in df_furn_dist.iterrows():
    #         i = 0
    #         for n in range(0,m-1):
    #             query_furn = self.driver.execute_query("""MATCH (furniture: Element {id: $id})
    #                                                     MATCH (boundElements: Element {id: $near_id})
    #                                                     MERGE (furniture)-[:NEAR {Distance:$dist}]->(boundElements)""",
    #                                                     id = row['ElementId'],
    #                                                     near_id = row['Nearest_elem_id_'f'{i}'],
    #                                                     dist = row['Distance_to_nearest_'f'{i}'],
    #                                                     database = "neo4j").summary
    #             i = i+1
    # def load_all_relationships(self):
    #     query_all = self.driver.execute_query("""MATCH (n)
    #                                              MATCH ()-[r]->()
    #                                              RETURN n, r""",database="neo4j").summary


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://8e5153b5.databases.neo4j.io"
    user = "neo4j"
    password = "Mmte2MYxy73Y0_pUSmCFy_ZxgHvjUaMTS14m4d8A5d8"
    app = App(uri, user, password)
    app.load_data(r'D:/Bachelor_thesis/super-constraints/data/tables/space_elements.csv')
    # app.load_all_relationships()
    # app.create_friendship("Alice", "David")
    # app.find_person("Alice")
    app.close()