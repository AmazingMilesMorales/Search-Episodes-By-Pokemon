import sqlite3

# Local
import sql

def formatPokemonName(species): 
    species = species[:1].upper() + species[1:] #TODO Fix capitalization, this is not ideal
    return species

print("If this is your first time running this program or if it has been a while, type 'udb' to ensure an updated database. Type 'help' for more commands")
print("Otherwise, what Pokemon would you like to look up?")

choice = input()
firstTimeSearching = True
while(True):
    if not firstTimeSearching:
        print("What Pokemon would you like to look up?")
        choice = input()  

    if choice == "help":
        print("* help for list of commands")
        print("* exit to exit program")
        print("* udb or updatedb to update database with new episodes from and saved to the pokemonMediaInfo.p file (Recommended for first time or if it's been a while since database has been updated)")
        print("* cdb or createdb to create database from scratch using Bulbapedia API and save to pokemonMediaInfo.p (Will take a few minutes and might cause an error, useful if pokemonMediaInfo.p is missing/corrupted)")
        print("* qdb or quickdb to create database from the pokemonMediaInfo.p file (Useful if pokemonanime.db is missing/corrupted)")
    elif choice == "exit":
        print("Exiting program...")
        exit()
    elif choice == "createdb" or choice == "cdb":
        print("Creating database from scratch...")
        sql.createDatabase()
    elif choice == "quickdb" or choice == "qdb":
        print("Creating database quickly...")
        sql.createDatabaseFromSavedFile()
    elif choice == "updatedb" or choice == "udb":
        print("Updating database file...")
        sql.updateDatabaseFromSavedFile()
    else:
        choice = formatPokemonName(choice)
        if choice: sql.getMediaByPokemonName(choice)
        else: print("Error parsing input, maybe you mispelled?")
    firstTimeSearching = False