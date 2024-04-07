import psycopg2

try:
    connection = psycopg2.connect(user="admin",
                                  password="adminpass",
                                  host="127.0.0.1",
                                  port="5433",
                                  database="main")
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Você está conectado ao - ", record, "\n")

except (Exception, psycopg2.Error) as error:
    print("Erro ao conectar ao PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Conexão ao PostgreSQL fechada")
