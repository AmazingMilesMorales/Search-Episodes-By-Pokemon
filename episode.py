import urllib.request
import sys

# Headers used for every API request
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

# NOTE: For the purposes of data storage, every piece of animated media (including movies and shorts) is stored as an "episode"

def getEpisodeInfo(episodeNum):
    try:
        # Get wikitext of each episode
        url = 'https://bulbapedia.bulbagarden.net/w/api.php?action=parse&format=php&page=EP' + str(episodeNum) + '&redirects=1&prop=wikitext'
        # There is one URL page that does not lead to the expected page, so I handled this one time error here:       
        if episodeNum == 375:
            url = 'https://bulbapedia.bulbagarden.net/w/api.php?action=parse&format=php&page=AG101&redirects=1&prop=wikitext'
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        episodePageText = str(resp.read().decode('UTF-8'))
        

        # Page does not exist
        if episodePageText.startswith("a:1:{s:5:\"error\""):
            print("Error getting episode number " + str(episodeNum) + ". Stopping here.")
            return -1

        episodeCode = getInfoFromEpisodePageText(episodePageText, "epcode")
        englishEpisodeTitle = getInfoFromEpisodePageText(episodePageText, "title_en")
        japaneseEpisodeTitle = getInfoFromEpisodePageText(episodePageText, "title_ja")
        japaneseEpisodeTitleTranslated = getInfoFromEpisodePageText(episodePageText, "title_ja_trans")
        japaneseBroadcastDate = getInfoFromEpisodePageText(episodePageText, "broadcast_jp")
        americanBroadcastDate = getInfoFromEpisodePageText(episodePageText, "broadcast_us")

        pokemonAppearances = getPokemonAppearancesFromEpisodePageText(episodePageText)

        return {
            "id": episodeNum,
            "type": "main_anime",
            "episodeNum": episodeNum,
            "episodeCode": episodeCode,            
            "englishEpisodeTitle": englishEpisodeTitle,
            "japaneseEpisodeTitle": japaneseEpisodeTitle,
            "japaneseEpisodeTitleTranslated": japaneseEpisodeTitleTranslated,
            "japaneseBroadcastDate": japaneseBroadcastDate,
            "americanBroadcastDate": americanBroadcastDate,
            "pokemonAppearances": pokemonAppearances,
            }

    except Exception as e:
        print(str(e))
        return -503

def getPokemonAppearancesFromEpisodePageText(episodePageText):
    pokemon = []
    pokemonSection = []
    if "===Pokémon===" in episodePageText:
        pokemonSection = episodePageText.split("===Pokémon===")[1].split("==")[0].splitlines()
    elif "=== Pokémon ===" in episodePageText:
        pokemonSection = episodePageText.split("=== Pokémon ===")[1].split("==")[0].splitlines()
    else:
        raise Exception('Pokémon section not found on page')

    for line in pokemonSection:
        if line.startswith("* {{p|"):
            pokemon.append(line.split("* {{p|")[1].split("}}")[0])

    # Remove duplicates before returning (such as multiple Pikachus in one episode)
    # return list(dict.fromkeys(pokemon))
    return pokemon

def getInfoFromEpisodePageText(episodePageText, string):
    try:
        info = episodePageText.split(string+"=")[1].split("|")[0]
        # Sometimes instead of actual info, the wikitext will contain a warning to not put bad information
        if "<!--" in info:
            return ''
    # Sometimes, info is not on the page. For example: no English titles for Japanese-only episodes.
    except Exception as e:
        return ''
    return info.strip()


def getEveryMainAnimeEpisodeInfo(episodeNum=1):
    pokemonEpisodesInfo = []
    while True:
        episodeInfo = getEpisodeInfo(episodeNum)
        if episodeInfo == -1: break
        if episodeInfo == -503:
            print("An error occured while fetching episodes. Please try again.")
            exit()
        if episodeInfo != -1:
            pokemonEpisodesInfo.append(episodeInfo)
            print("Getting episode info from Bulbapedia API for Episode " + str(episodeNum))
            episodeNum = episodeNum + 1
        else:
            break
    return pokemonEpisodesInfo

def getAllMediaInfo(startingEpisodeNum=1):
    pokemonEpisodesInfo = getEveryMainAnimeEpisodeInfo(startingEpisodeNum)
    # TODO: Movies, Side Stories, Origins, Generations, Twilight Wings, Mystery Dungeon, Animated trailers
    return pokemonEpisodesInfo