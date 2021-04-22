from sqlalchemy import create_engine

# Windows auth
Server = 'LAPTOP-2OCJA2M7\SQLEXPRESS'
Database = 'test'
Driver = 'ODBC Driver 17 for SQL Server'
Database_con = f'mssql://@{Server}/{Database}?driver={Driver}'

engine = create_engine(Database_con)
con = engine.connect()

if con:
    print('Conexion establecida!')



