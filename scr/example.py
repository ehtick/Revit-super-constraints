from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import pandas as pd
class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def load_data(self,filename):
        data = pd.read_csv(filename)
        df = pd.DataFrame(data)
        rooms = df.groupby('Selected_roomI_Id').groups.keys()

        nameOfFile_csv = 'space_elements_furniture.csv'
        completename_csv = 'D:/Bachelor_thesis/super-constraints/data/tables/' + nameOfFile_csv
        data = pd.read_csv(completename_csv)
        df_furn_dist = pd.DataFrame(data)

        # think about how to add name to the node
        # it should be in the table
        for index, row in df.iterrows():
            query_space = self.driver.execute_query("MERGE (s:Space {name: 'Space', id: $id_s})",
                                                    id_s = row['Selected_roomI_Id'],
                                                    database = "neo4j").summary
            query_element = self.driver.execute_query("MERGE (e:Element {name: 'Element', id: $id, family: $family})",
                                                        id = row['ElementId'],
                                                        family = row['Family'],
                                                        database = "neo4j").summary
            query_sum = self.driver.execute_query("""MATCH (e:Element {name: 'Element',id: $id, family: $family})
                                                    MATCH (s:Space {id: $id_s})
                                                    MERGE (s)-[:CONTAINS]->(e)""",
                                                    id_s = row['Selected_roomI_Id'],
                                                    id = row['ElementId'],
                                                    family = row['Family'],
                                                    database = "neo4j").summary
        m = int(len(df_furn_dist.columns)/2)
        for index, row in df_furn_dist.iterrows():
            i = 0
            for n in range(0,m-1):
                query_furn = self.driver.execute_query("""MATCH (furniture: Element {id: $id})
                                                        MATCH (boundElements: Element {id: $near_id})
                                                        MERGE (furniture)-[:NEAR {Distance:$dist}]->(boundElements)""",
                                                        id = row['ElementId'],
                                                        near_id = row['Nearest_elem_id_'f'{i}'],
                                                        dist = row['Distance_to_nearest_'f'{i}'],
                                                        database = "neo4j").summary
                i = i+1
    def load_all_relationships(self):
        query_all = self.driver.execute_query("""MATCH (n)
                                                 MATCH ()-[r]->()
                                                 RETURN n, r""",database="neo4j").summary
        # data = pd.read_csv(filename)
        # df = pd.DataFrame(data)
        # for index, row in df.iterrows():
        #     # query = "create (e:Element {id:" + str(row['ElementId'])+", family:"+str(row['Family'])+"})"
        #     query = "create (e:Element {id:" + str(row['ElementId'])+"})"
        #     with self.driver.session(database="neo4j")  as session:
        #         session.run(query)


    # def load_data(self,filename):
    #     with self.driver.session(database="neo4j") as session:
    #         # Write transactions allow the driver to handle retries and transient errors
    #         result = session.execute_write(
    #             self._load_and_return_data, filename)
      
    # # def create_friendship(self, person1_name, person2_name):
    #     with self.driver.session(database="neo4j") as session:
    #         # Write transactions allow the driver to handle retries and transient errors
    #         result = session.execute_write(
    #             self._create_and_return_friendship, person1_name, person2_name)
    #         for row in result:
    #             print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))
    
    # @staticmethod
    # def _create_and_return_friendship(tx, person1_name, person2_name):
    #     # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
    #     # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
    #     query = (
    #         "CREATE (p1:Person { name: $person1_name }) "
    #         "CREATE (p2:Person { name: $person2_name }) "
    #         "CREATE (p1)-[:KNOWS]->(p2) "
    #         "RETURN p1, p2"
    #     )
    #     result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
    #     try:
    #         return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
    #                 for row in result]
    #     # Capture any errors along with the query and data for traceability
    #     except ServiceUnavailable as exception:
    #         logging.error("{query} raised an error: \n {exception}".format(
    #             query=query, exception=exception))
    #         raise

    # def find_person(self, person_name):
    #     with self.driver.session(database="neo4j") as session:
    #         result = session.execute_read(self._find_and_return_person, person_name)
    #         for row in result:
    #             print("Found person: {row}".format(row=row))

    # @staticmethod
    # def _find_and_return_person(tx, person_name):
    #     query = (
    #         "MATCH (p:Person) "
    #         "WHERE p.name = $person_name "
    #         "RETURN p.name AS name"
    #     )
    #     result = tx.run(query, person_name=person_name)
    #     return [row["name"] for row in result]


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://8e5153b5.databases.neo4j.io"
    user = "neo4j"
    password = "Mmte2MYxy73Y0_pUSmCFy_ZxgHvjUaMTS14m4d8A5d8"
    app = App(uri, user, password)
    app.load_data(r'D:/Bachelor_thesis/super-constraints/data/tables/space_elements.csv')
    app.load_all_relationships()
    # app.create_friendship("Alice", "David")
    # app.find_person("Alice")
    app.close()