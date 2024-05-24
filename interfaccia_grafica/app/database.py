# pip install mysql-connector-python

import mysql.connector

# Connessione al database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="traintrack"
)

# Creazione di un cursore per eseguire query SQL
c = conn.cursor()

# Esempio: eseguire una query per ottenere dati dalla tabella 'persone'
c.execute("SELECT * FROM Turnouts")
rows = c.fetchall()
for row in rows:
    print(row)

# Chiusura del cursore e della connessione
c.close()
conn.close()