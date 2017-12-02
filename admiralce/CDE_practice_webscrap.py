import csv
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

list_of_courses = []

for i in range (1, 16):
    if(i == 1):
        url = 'https://www.dentalcare.com/en-us/professional-education/ce-courses?keywords=' 

    url = 'https://www.dentalcare.com/en-us/professional-education/ce-courses?keywords=&currentpage=' + str(i)


    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source

    soup = BeautifulSoup(html, 'lxml')
    bacon = soup.find_all('div', 'course-search-results-tiles')

    # print bacon

    for row in bacon:
        course_info = []

        # course_info.append(row.find('a','btn-link').get_text().encode('utf-8'))

        title =  row.find('span', 'course-tile-title')

        for x in title:
            try: 
                if x.name == 'a':
                    yay = x.get_text().encode('utf-8')
                    course_info.append(yay)
            except: 
                pass

        # print row.find_all('a','btn-link') #.get_text().encode('utf-8')
        course_info.append("N/A")

        start_date = row.find('span','course-tile-online-date').get_text().encode('utf-8')

        end_date = row.find('span', 'course-tile-expiry-date').get_text().encode('utf-8')

        dates = start_date + " - " + end_date

        course_info.append(dates)

        course_info.append(row.find_all('span', 'course-tile-expiry-date')[2].get_text().encode('utf-8'))

        course_info.append(row.find_all('span', 'course-tile-expiry-date')[1].get_text().encode('utf-8'))

        course_info.append(row.find('span', 'course-tile-education-unit').get_text().encode('utf-8'))

        course_info.append(row.find('span', 'course-tile-author').get_text().encode('utf-8'))

        course_info.append(row.find('span', 'course-tile-audience').get_text().encode('utf-8'))

        description =  row.find('span', 'course-tile-shortdescription')

        for x in description:
            try: 
                if x.name == 'p':
                    nice = x.get_text().encode('utf-8')
                    course_info.append(nice)
            except: 
                pass

        course_info.append(row.find('a', 'btn-link')['href'].encode('utf-8'))

        list_of_courses.append(course_info)
    # print list_of_courses

outfile = open("./dentalcare.csv", "wb")
writer = csv.writer(outfile)
writer.writerow(["Title", "Subject", "Dates", "Location", "Cost", "Hours", "Provider", "Type", "Description", "Website"])
writer.writerows(list_of_courses)