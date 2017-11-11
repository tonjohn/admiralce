import csv
import requests
from BeautifulSoup import BeautifulSoup

url = 'http://www.ada.org/en/ccepr/find-ce-courses#sort=date%20descending' 

# url = 'https://ebusiness.cda.org/ebusiness/speaker/Speakerschedule'

# url ='https://dental.washington.edu/continuing-dental-education/8/' #403 forbidden

# url='http://www.vetstreet.com/cats/'
# soup = BeautifulSoup(requests.get(url).text)

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)

print soup
# table = soup.find('table', attrs={'id':"MainContentAreaPlaceHolder_C001_grdSpeakerdetails"})
# print table


# table = soup.find('tbody', attrs={'class': "stripe"})

# list_of_rows = []
# for row in table.findAll("tr")[1:]:
#     list_of_cells = []
#     for cell in row.findAll('td'):
#         text = cell.text.replace('&nbsp', '')
#         list_of_cells.append(text)
#     list_of_rows.append(list_of_cells)

# outfile = open("./inmates2.csv", "wb")
# writer = csv.writer(outfile)
# writer.writerow(["Last", "First", "Middle", "Gender", "Race", "Age", "City", "State"])
# writer.writerows(list_of_rows)