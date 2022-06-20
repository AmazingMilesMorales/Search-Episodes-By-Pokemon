import sqlite3

# Local
import sql

def formatPokemonName(species):
    appendableShortOptions = ['-udb', '-cdb', '-qdb']
    appendableLongOptions = ['createdb', 'updatedb', 'quickdb', 'exit']
    # TODO: Replace with regex
    for option in appendableShortOptions:
        species = species.replace(' ' + option, '')
        species = species.replace(option, '')
    for option in appendableLongOptions:
        species = species.replace('-- ' + option, '')
        species = species.replace('- ' + option, '')
        species = species.replace(' ' + option, '')
        species = species.replace(option, '')
    
    species = species[:1].upper() + species[1:] #TODO Fix capitalization, this is not ideal
    return species

print("You can append with the following options:")
print("* -udb or updatedb to update episodes database with new episodes from and saved to the pokemonMediaInfo.p file (Recommended for first time or if it's been a while since database has been updated)")
print("* -cdb or createdb to get a fully updated database from scratch using Bulbapedia API and save to pokemonMediaInfo.p (Will take a few minutes and might cause an error, useful if pokemonMediaInfo.p is missing/corrupted)")
print("* -qdb or quickdb to create episodes database from the pokemonMediaInfo.p file (Useful if pokemonanime.db is missing/corrupted)")
print("* exit to exit program")
print("Otherwise, what Pokemon would you like to look up?")

choice = input()
firstTimeSearching = True
while(True):
    if not firstTimeSearching:
        print("What Pokemon would you like to look up?")
        choice = input()  

    if "createdb" in choice or "-cdb" in choice:
        print("Creating database from scratch...")
        sql.createDatabase()
    elif "quickdb" in choice or "-qdb" in choice:
        print("Creating database quickly...")
        sql.createDatabaseFromSavedFile()
    elif"updatedb" in choice or "-udb" in choice:
        print("Updating database file...")
        sql.updateDatabaseFromSavedFile()
    elif "exit" in choice:
        print("Exiting program...")
        exit()

    # Regardless, search for that Pokemon!!    
    choice = formatPokemonName(choice)
    sql.getMediaByPokemonName(choice)
    firstTimeSearching = False