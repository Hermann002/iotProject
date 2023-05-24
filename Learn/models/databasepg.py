import psycopg2

def connect():
    """ Connect to the PostgreSQL database server """
    # try:
    # read connection parameters

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(
    host="digishop.postgres.database.azure.com",
    database="iot_database",
    user="digipos",
    password="postgres12@")
    
    # create a cursor
    cur = conn.cursor()
    
# execute a statement
    cur.execute('SELECT idcapteur, temperature, humidity FROM capteur')

    # display the PostgreSQL database server version
    db_version = cur.fetchall()
    
# close the communication with the PostgreSQL
    cur.close()
    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)

    return db_version