import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import threading

dataGlobal = {}

lastValue = 0
currentValue = 0
progress = []

for year in range(2010, 2020):

    html_content = requests.get('https://www.top500.org/lists/top500/{}/06/'.format(year)).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")


    table = soup.findAll("table", {"class": "table-condensed"})
    rows = table[0].findAll('tr')
    header = table[0].findAll('th')
    inmultire = 1
    if str(header[3]) == '<th>Rmax (TFlop/s)</th>':
        inmultire = 1000
    
    data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]

    topName = ''
    for smallName in data[1][1]:
        topName+=smallName
    topName = ' '.join(topName.replace("\n", "").strip().split())

    cores = 0
    rmax = 0
    rpeak = 0

    for index in range(1, 4):
        cores += float(data[index][2][0].replace(',', ''))
        rmax += float(data[index][3][0].replace(',', ''))
        rpeak += float(data[index][4][0].replace(',', ''))

    lastValue = currentValue
    currentValue = inmultire * rmax//3

    if currentValue * lastValue:
        progress.append(currentValue - lastValue)

    dataGlobal[year] = [cores//3, inmultire * rmax//3, inmultire * rpeak//3]


fig, ax = plt.subplots() 
ax.set_ylabel('Rmax (TFlop/s)')
ax.set_xlabel('Year')
rmaxDataGlobal = []
for year in dataGlobal:
    rmaxDataGlobal.append(dataGlobal[year][1])


ax.plot(dataGlobal.keys(), rmaxDataGlobal)

for yearIndex in range(2011, 2020):
    print('Progresul pentru ' + str((yearIndex - 1)) + ' - ' +  str(yearIndex) + ' este: ' + str(progress[yearIndex - 2011]))

plt.show()
