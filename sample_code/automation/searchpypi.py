#! python3
# Open several Google search results.

import bs4
import requests
import sys
import webbrowser

print('Searching...')  # display text while downloading the search result page
res = requests.get('http://pypi.org/search/?q=' + ' '.join(sys.argv[1:]))
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, features='html.parser')
linkElems = soup.select('.package-snippet')
numOpen = min(5, len(linkElems))
for i in range(numOpen):
    urlToOpen = 'http://pypi.org' + linkElems[i].get('href')
    print('Opening', urlToOpen)
    webbrowser.open(urlToOpen)
