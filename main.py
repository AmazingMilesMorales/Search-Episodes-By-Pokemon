import sqlite3

# Local
import sql

def menu():
    print("What Pokemon would you like to look up? If this is your first time running this program, type createdb")
    choice = input()
    return str(choice)

while(True):
    choice = menu()
    if choice == "createdb":
        print("Creating database...")
        sql.createDatabase()
    else:
        choice = choice[:1].upper() + choice[1:]
        sql.getEpisodesByPokemonName(choice)
        break

        
