import psycopg2
from psycopg2 import pool

class DataBaseManager():
    
    def create_pool(self, host, port, database, user, password='', min=1, max=5):
        try:
            pool = psycopg2.pool.SimpleConnectionPool(min, max, host = host, port = port, database = database, user = user, password = password)
        
            if(pool):
                print("Connection pool created successfully")
            return pool

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)
    
    def select_data(self, pool, table, query):
        sql = "select {} from {};".format(query, table)

        connection  = pool.getconn()
        cursor = connection.cursor()
        cursor.execute(sql)
        result = [r[0] for r in cursor.fetchall()]
        cursor.close()
        pool.putconn(connection)

        return result

    def insert_data(self, pool, table, data):
        sql = "insert into {} ({}) values {}".format(table, ','.join(list(data.keys())), tuple(data.values()))
        
        connection  = pool.getconn()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        pool.putconn(connection)

    def closer(self, pool):
        if (pool):
            pool.closeall
            print("PostgreSQL connection pool is closed")

#dbm = DataBaseManager()
#pool = dbm.create_pool(controller.local_db_host, controller.local_db_port, "fvid", controller.local_db_user, '')
#select_result = dbm.select_data(pool, "company_keyword_set", 'keyword')
#insert_result = dbm.insert_data(pool, "sample_keyword_trend", result)
#dbm.closer(pool)