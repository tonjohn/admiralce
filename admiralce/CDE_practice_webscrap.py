import csv
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

url = 'http://www.ada.org/en/ccepr/find-ce-courses#sort=date%20descending' 

browser = webdriver.PhantomJS()
browser.get(url)
html = browser.page_source

# url = 'https://ebusiness.cda.org/ebusiness/speaker/Speakerschedule'

# url ='https://dental.washington.edu/continuing-dental-education/8/' #403 forbidden

# url='http://www.vetstreet.com/cats/'

soup = BeautifulSoup(html, 'lxml')
bacon = soup.find_all('div', 'CoveoResult')

list_of_courses = []
for row in bacon:
    course_info = []
    title = row.find('a','CoveoResultLink').get_text()
    details = row.find_all('span', class_=False)
    course_info.append(title.encode('utf-8'))

    for x in range(0, len(details)):

        if not details[x].get_text() == " To ":
            if details[x].get_text():
                the_goods = details[x].get_text()
                course_info.append(the_goods.encode('utf-8'))
        list_of_courses.append(course_info)
print list_of_courses

outfile = open("./ada.csv", "wb")
writer = csv.writer(outfile)
writer.writerow(["Title", "Subject", "Dates", "Location", "Cost", "Provider", "Type", "Description", "Website"])
writer.writerows(list_of_courses)

# for course in bacon:
#    print course.prettify()



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
