import psycopg2
from psycopg2 import sql

class DatabaseManager:
    def __init__(self, db_name, db_user, db_password, db_host, db_port, verbose=True):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.conn = None
        self.verbose = verbose

        self.update_data('myapp_control', 'calibration', False)
        self.update_data('myapp_control', 'panel', False)
        self.update_data('myapp_control', 'motor', False)


    def create_connection(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            if self.verbose:
                print("Connection to PostgreSQL DB successful")
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")


    def reset_database(self, table_name):
        if self.conn is None:
            if self.verbose:
                print("Error! Cannot create the database connection.")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table_name)))

            cur.execute(sql.SQL("""
                CREATE TABLE {} (
                    id SERIAL PRIMARY KEY,
                    drink1 INTEGER DEFAULT 0,
                    drink2 INTEGER DEFAULT 0,
                    status BOOLEAN DEFAULT FALSE
                )
            """).format(sql.Identifier(table_name)))
            cur.execute(sql.SQL("INSERT INTO {} DEFAULT VALUES").format(sql.Identifier(table_name)))

            self.conn.commit()
            if self.verbose:
                print("Database reset successfully")
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")
        finally:
            cur.close()


    def read_data(self, table_name):
        if self.conn is None:
            if self.verbose:
                print("Error! Cannot create the database connection.")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            rows = cur.fetchall()
            data = rows

            if self.verbose:
                print(data)
            return data
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")
        finally:
            cur.close()


    def read_single_value(self, table_name, key):
        if self.conn is None:
            if self.verbose:
                print("Error! Cannot create the database connection.")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(sql.SQL("SELECT {} FROM {}").format(sql.Identifier(key), sql.Identifier(table_name)))
            value = cur.fetchone()
            if value:
                value = value[0]
            else:
                value = None

            if self.verbose:
                print(f"Read single value: key={key}, value={value}")
            return value
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")
        finally:
            cur.close()


    def update_data(self, table_name, key, new_value):
        if self.conn is None:
            if self.verbose:
                print("Error! Cannot create the database connection.")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(sql.SQL("UPDATE {} SET {} = %s").format(sql.Identifier(table_name), sql.Identifier(key)), (new_value,))
            self.conn.commit()
            if self.verbose:
                print(f"Data updated successfully: key={key}, new_value={new_value}")
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")
        finally:
            cur.close()


    def insert_data(self, table_name, key, value):
        if self.conn is None:
            if self.verbose:
                print("Error! Cannot create the database connection.")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(sql.SQL("INSERT INTO {} ({}) VALUES (%s)").format(sql.Identifier(table_name), sql.Identifier(key)), (value,))
            self.conn.commit()
            if self.verbose:
                print(f"Data inserted successfully: key={key}, value={value}")
        except Exception as e:
            if self.verbose:
                print(f"The error '{e}' occurred")
        finally:
            cur.close()


    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            if self.verbose:
                print("Connection closed")
