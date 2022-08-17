"""
A Database class to represent the connection to a web-hosted database that 
stores all user data.
"""

# Import modules
import mysql.connector
import pandas as pd

# Remove warning from pandas regarding mysql module
import warnings
warnings.simplefilter(action="ignore", category=UserWarning)

class Database:
    """Database class."""

    def __init__(self, 
                 host: str, 
                 port: int, 
                 user: str, 
                 password: str, 
                 database: str):
        """Initialization method.
        
        Arguments:
            host
                host address
            port
                port number
            user
                database user
            password
                database password
            database
                database schema
        """

        # Connect to database
        self.connection = mysql.connector.connect(host=host,
                                                  port=port,
                                                  user=user,
                                                  password=password,
                                                  database=database)
        # Cursor to exucute SQL statements to manage database
        self.cursor = self.connection.cursor(named_tuple = True)

    def get_column_names(self, table_name: str) -> list[str]:
        """Return all column names for a given table.
        
        Arguments:
            table_name
                table name
        
        Returns:
            column_names    
                column names
        """

        # SQL query to pass to database
        sql = f"SHOW COLUMNS FROM {table_name}"

        # Read sql query as a pandas dataframe
        result = pd.read_sql_query(sql, self.connection)

        # Parse the column names from the dataframe
        column_names = list(result["Field"])

        return column_names

    def add_data(self, table_name: str, data: list):
        """Add a row of data to a table.
        
        Arguments:
            table_name
                table name
            data
                row of data    
        """

        # Column names for table
        column_names = self.get_column_names(table_name)

        # SQL statement to insert the row of data
        # Format: 
        # INSERT INTO table_name (col1, col2, ...) VALUES (val1, val2, ...)
        sql = f"INSERT INTO {table_name} \
                ({'{}, ' * (len(column_names)-1) + '{}'}) VALUES \
                ({'%s, '*(len(column_names)-1)}%s);".format(*column_names)
        
        self.execute_sql(sql, data)
    
    def update_cell(self, 
                    table_name: str, 
                    id: int, 
                    column_name: str, 
                    new_val):
        """Update a cell in a table with a new value.
        
        Arguments:
            table_name
                table name
            id
                user id
            column_name
                column name
            new_val : any
                new val to be in the cell
        """
        
        # SQL statement to update a cell
        sql = f"UPDATE {table_name} SET {column_name} = '{new_val}' WHERE \
                ID = {id}"
        
        self.execute_sql(sql)
    
    def update_cells(self, 
                     table_name: str, 
                     id: int, 
                     column_names: list[str], 
                     new_vals: list):
        """Update cells in a table with new values.
        
        Arguments:
            table_name
                table name
            id
                user id
            column_names
                columns to update the cells in
            new_vals
                new values to be in the cells
        """
        
        # Format:
        """
        UPDATE table_name
        SET
            col1 = new_val1
            col2 = new_val2
            ...
        WHERE 
            ID = id
        """
    
        sql = f"UPDATE {table_name} SET "
        for i, _ in enumerate(column_names):
            sql += f"{column_names[i]} = '{new_vals[i]}', "
        sql = sql[:-2]
        sql += f" WHERE ID = {id}"

        self.execute_sql(sql)

    def execute_sql(self, sql: str, data=None):
        """Execute a SQL statement.
        
        Arguments:
            sql
                SQL statement
            data
                data if updating cell(s)
        """

        if data is not None:
            self.cursor.execute(sql, data)
            self.connection.commit()
        else:
            self.cursor.execute(sql)
            self.connection.commit()
    
    def get_table(self, table_name: str) -> pd.DataFrame:
        """Return contents of a table.
        
        Arguments:
            table_name
                table name
        
        Returns:
            result
                table as a pandas dataframe
        """

        sql = f"SELECT * FROM {table_name}"

        result = pd.read_sql_query(sql, self.connection)

        return result

        