import psycopg2


class PostGres:

    __connString = "dbname=postgres user=postgres password=admin123 host=10.2.0.193"
    __conn = None
    __cursor = None

    def __init__(self):
        try:
            self.__conn = psycopg2.connect(self.__connString)
            self.__cursor = self.__conn.cursor()
        except Exception as e:
            self.Close()

    def InsertControl(self, control):
        try:
            self.__cursor.execute(
                """
                Insert into login (name, password) values (%s, %s)
                """,
                [control[0], control[1]]
            )
            self.__conn.commit()
        except Exception as e:
            print(e)

    def Close(self):
        if(self.__conn != None and not self.__conn.closed):
            self.__conn.close()
        if(self.__cursor != None and not self.__cursor.closed):
            self.__cursor.close()
        


