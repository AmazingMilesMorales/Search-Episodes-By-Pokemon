import urllib.request

# Headers used for every API request
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

# NOTE: For the purposes of data storage, every piece of animated media (including movies and shorts) is stored as an "episode"

def getEpisodeInfo(episodeNum):
    print(episodeNum)
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
            "japaneseBroadcastDate": japaneseBroadcastDate,
            "americanBroadcastDate": americanBroadcastDate,
            "pokemonAppearances": pokemonAppearances,
            }

    except Exception as e:
        print(str(e))
        return -1

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
    # Sometimes, info is not on the page. For example: no English titles for Japanese-only episodes.
    except Exception as e:
        return ''
    return info.strip()


def getEveryMainAnimeEpisodeInfo():
    pokemonEpisodesInfo = []
    episodeNum = 1
    while True:
        episodeInfo = getEpisodeInfo(episodeNum)
        if(episodeInfo != -1):
            pokemonEpisodesInfo.append(episodeInfo)
            # Since we are dealing with a 1115+ episodes of content, for testing I'll export it so I don't
            # have to call this over and over again
            '''
            with open("output.txt", "a", encoding="utf-8") as txt_file:
                txt_file.write(str(episodeInfo))
                txt_file.write("\n")
            '''
            episodeNum = episodeNum + 1
        else:
            break
    return getEveryEpisodeInfo

def getEveryEpisodeInfo():
    pokemonEpisodesInfo = getEveryMainAnimeEpisodeInfo()
    # TODO: Movies, Side Stories, Origins, Generations, Twilight Wings, Mystery Dungeon, Animated trailers
    return pokemonEpisodesInfo

getEveryMainAnimeEpisodeInfo()