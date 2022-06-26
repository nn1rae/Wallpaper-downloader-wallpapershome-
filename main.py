import string
import random
import requests
from bs4 import BeautifulSoup as bs
from alive_progress import alive_bar
from colorama import init, Fore

init()
dict = string.ascii_uppercase + string.digits + string.ascii_lowercase
fullLink = 'https://wallpapershome.com'
linksToFullPage = []
linksToDownload = []
while True:
    print(Fore.CYAN)
    link = input('Enter a link to download: ') + '?page={0}' 
    if fullLink in link:
        break
    else:
        print(Fore.RED)
        print('Link not walid')

getMaxPG = bs(requests.get(link[:-9]).content, 'html.parser')
MAXPAGE = int(getMaxPG.select('#content > div.col-right > p > a:nth-child(6)')[0].contents[0])


print(Fore.GREEN)
#get all of the walpapers from link
with alive_bar(MAXPAGE, dual_line=True, title='PAGE_LINKS',bar='solid', spinner= 'twirls', ctrl_c=False) as bar:
    for i in range(MAXPAGE):
        bar.text = f'-> Getting page {i} link, please wait...'
        soup = bs(requests.get(link.format(i)).content, 'html.parser')
        for i in soup.select('#pics-list > p'):
            linksToFullPage.append(i.next['href'])
        bar()
print(Fore.BLUE)        
#extract links to download
with alive_bar(len(linksToFullPage), dual_line=True, title='Extracting links to download', bar= 'solid', spinner= 'twirls', ctrl_c=False) as bar:
    for preLink in linksToFullPage:
        wlPage = fullLink + preLink
        paP = bs(requests.get(wlPage).content, 'html.parser')
        download__resolutions = paP.find(class_="block-download__resolutions--6")
        linksToDownload.append(fullLink + download__resolutions.contents[0].contents[2]['href'])

        bar.text = '-> Got link {} link, continue...'.format(fullLink + download__resolutions.contents[0].contents[2]['href'])
        bar()
print(Fore.YELLOW) 
with alive_bar(len(linksToDownload), dual_line=True, title='Downloading wallpapers', spinner= 'twirl', ctrl_c=False, bar= 'solid') as bar:
    for l in linksToDownload:
        with open('wallpapers/' + ''.join(random.choice(dict) for _ in range(12)) + '.jpg', 'wb') as wallpaper: #creates a file with a random name
            wallpaper.write(requests.get(l).content)
            bar.text = 'Downloading {}'.format(l)
        bar()

print(Fore.GREEN + 'Finished downloading')
