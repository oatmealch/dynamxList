import requests
from bs4 import BeautifulSoup
from save import saveFile, saveKorean

dynamaxResult = requests.get(
    "https://www.serebii.net/swordshield/dynamaxadventurespokemon.shtml")

dynamaxSoup = BeautifulSoup(dynamaxResult.text, "html.parser")

tables = []
table = dynamaxSoup.find_all("table", {"class": "trainer"})
for table in table:
  tables.append(table)

componentsNotBoss = tables[0].find_all('a')
componentsBoss = tables[1].find_all('a')

dataNotBoss = []
dataBoss = []

for link in componentsNotBoss:
  if 'href' in link.attrs:
    dataNotBoss.append(link.attrs['href'])

for link in componentsBoss:
  if 'href' in link.attrs:
    dataBoss.append(link.attrs['href'])


resultNotBoss = []
resultBoss = []

for word in dataNotBoss:
  if len(word.split('/')) == 4:
    resultNotBoss.append("name: '"+word.split('/')[2]+"'")
  elif len(word.split('/abilitydex/')) == 2:
    resultNotBoss.append("ability: '"+word.split('/')[-1].replace('.shtml','')+"'")
  elif len(word.split('/')) == 3:
   resultNotBoss.append("'"+word.split('/')[-1].replace('.shtml','')+"'")

for word in dataBoss:
  if len(word.split('/')) == 4:
    resultBoss.append("name: '"+word.split('/')[2]+"'")
  elif len(word.split('/abilitydex/')) == 2:
    resultBoss.append("ability: '"+word.split('/')[-1].replace('.shtml','')+"'")
  elif len(word.split('/')) == 3:
   resultBoss.append("'"+word.split('/')[-1].replace('.shtml','')+"'")


mergedNotBoss = []
mergedBoss = []

def mergeDataNotBoss(data) :
  tempList = [0]
  i = 0
  data.append('name: ')
  while i < len(data):
    if 'name:' in data[i]:
      tempList.append('isBoss: false')
      mergedNotBoss.append(tempList)
      tempList = [data[i]]
    else :
      tempList.append(data[i])
    i += 1

def mergeDataBoss(data) :
  tempList = [0]
  i = 0
  data.append('name: ')
  while i < len(data):
    if 'name:' in data[i]:
      tempList.append('isBoss: true')
      mergedBoss.append(tempList)
      tempList = [data[i]]
    else :
      tempList.append(data[i])
    i += 1


cleanedNotBoss = []
cleanedBoss = []

def cleanData(data, newData) :
  j = 0
  while j < len(data):
    if len(data[j]) == 8:
      data[j].insert(2, data[j][1])
      newData.append(data[j])      
    elif len(data[j]) == 9:
      newData.append(data[j])
    j += 1



doneData = []
tableDex = []
namesKorean = []
refinedKorean = []


def finishData(data1, data2, newData):
  newData = data1 + data2
  for element in newData:
    element[1] = 'type01: '+element[1]
    element[2] = 'type02: '+element[2]
    element[4] = 'move01: '+element[4]
    element[5] = 'move02: '+element[5]
    element[6] = 'move03: '+element[6]
    element[7] = 'move04: '+element[7]
    element.append("image: 'https://img.pokemondb.net/sprites/sword-shield/icon/"+str(element[0]).replace("'",'').replace('name: ','')+ ".png'")
  saveFile(newData)



def scrapKorean(doneData):
  for item in doneData:
    dexResult = requests.get("https://www.serebii.net/pokedex-swsh/"+item[0].replace("name: ",'').replace("'",''))
    dexSoup = BeautifulSoup(dexResult.text, "html.parser")
    dataScrapped = dexSoup.find_all("td",{"class":"fooinfo"})
    for table in dataScrapped:
      tableDex.append(str(table.find_all("td")))

def searchingKorean():
  i = 0
  while i < len(tableDex) :
    if '<td><b>Korean</b>: </td>' in tableDex[i]:
      namesKorean.append(tableDex[i])
    i += 1

def finishKorean():
  for item in namesKorean:
    refinedKorean.append(item[item.rfind('<td>')+4:len(item)-6])
  saveKorean(refinedKorean)




def scrapData():
  mergeDataNotBoss(resultNotBoss)
  mergeDataBoss(resultBoss)
  cleanData(mergedNotBoss, cleanedNotBoss)
  cleanData(mergedBoss, cleanedBoss)
  finishData(cleanedNotBoss ,cleanedBoss, doneData)
  scrapKorean(doneData)
  searchingKorean()
  finishKorean()



