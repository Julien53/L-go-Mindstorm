import postgesConn as conn

connection = conn.PostGres()
connection.InsertControl(["julius", "123"])
connection.Close()