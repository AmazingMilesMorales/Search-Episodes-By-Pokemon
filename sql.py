import sqlite3

# Local
import episode
import pokemonSpecies

def manipulateTable(command):
    connection = sqlite3.connect('pokemonanime.db')
    db = connection.cursor()
    db.execute(command)
    connection.commit()
    connection.close()