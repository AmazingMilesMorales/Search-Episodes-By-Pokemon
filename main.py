import sqlite3

# Local
import sql

def menu():
    print("What Pokemon would you like to look up?")
    choice = input()
    return str(choice)

print("If this is your first time running this program, either type:")
print("* createdb to get a fully updated db from Bulbapedia API (will take a few minutes and might cause an error)")
print("* quickdb to create episodes database from the pokemonEpisodesInfo.p file")

while(True):
    choice = menu()
    if choice == "createdb":
        print("Creating database...")
        sql.createDatabase()
    elif choice == "quickdb":
        print("Creating database quickly...")
        sql.createDatabaseFromSavedFile()
    else:
        choice = choice[:1].upper() + choice[1:]
        sql.getEpisodesByPokemonName(choice)

        
