import urllib.request
try:
    # Go through every episode
    for x in range(1,1062):

        
        url = 'https://bulbapedia.bulbagarden.net/w/api.php?action=parse&format=php&page=EP' + str(x) + '&redirects=1&prop=wikitext'
        # There is one URL page that does not lead to the expected page, so I handled this one time error here:       
        if x == 375:
            url = 'https://bulbapedia.bulbagarden.net/w/api.php?action=parse&format=php&page=AG101&redirects=1&prop=wikitext'
        
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())

        # Remove backslash that messes up reading the file in other programs
        # Also replace "* {{p|" with "POKETIME", since * causes dangling meta character error in the Java file

        respData = respData.replace("\\","")
        respData = respData.replace("* {{p|","POKETIME")
        respData = respData.replace("*{{p|","POKETIME")
        
        # create new file
        if x == 1:
            f = open("D:/projects/apicallresults.txt", "w")
            f.write(str(respData))
            f.close()
        # append file
        else:
            f = open("D:/projects/apicallresults.txt", "a")
            f.write(str(respData))
            f.close()

        #print(str(respData))
except Exception as e:
    print(str(e))
