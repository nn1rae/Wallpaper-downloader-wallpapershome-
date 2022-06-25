import string
import random
import requests
from bs4 import BeautifulSoup as bs
dict = string.ascii_uppercase + string.digits + string.ascii_lowercase
fullLink = 'https://wallpapershome.com'
linksToFullPage = []
linksToDownload = []
link = input('Enter a link to download format[https://wallpapershome.com/best-mobile-desktop-wallpapers/]: ') + '?page={0}' 
getMaxPG = bs(requests.get(link[:-9]).content, 'html.parser')
MAXPAGE = int(getMaxPG.select('#content > div.col-right > p > a:nth-child(6)')[0].contents[0])
print('Max page is {0}'.format(MAXPAGE))
#get all of the walpapers from link
for i in range(1, MAXPAGE):
    soup = bs(requests.get(link.format(i)).content, 'html.parser')
    for i in soup.select('#pics-list > p'):
        linksToFullPage.append(i.next['href'])
        print(i.next['href'])
#extract links to download
for preLink in linksToFullPage:
    wlPage = fullLink + preLink
    paP = bs(requests.get(wlPage).content, 'html.parser')
    download__resolutions = paP.find(class_="block-download__resolutions--6")
    linksToDownload.append(fullLink + download__resolutions.contents[0].contents[2]['href'])
    print(fullLink + download__resolutions.contents[0].contents[2]['href'])
    
for l in linksToDownload:
    with open('wallpapers/' + ''.join(random.choice(dict) for _ in range(12)) + '.jpg', 'wb') as wallpaper: #creates a file with a random name
        wallpaper.write(requests.get(l).content)
        print('Done °^° with {0}'.format(l))

