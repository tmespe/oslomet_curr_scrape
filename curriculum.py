# scrape curriculums from universty site
import requests
from bs4 import BeautifulSoup
from time import sleep
from copy import deepcopy
from tqdm import tqdm
import json

url = ['https://student.oslomet.no/studier']


def get_table_rows(urls, selector='table tr'):
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            rows = soup.select(selector)
        except TypeError:
            pass
        return rows
        #sleep(5)


def rows_to_links(rows, selector='td:nth-of-type(1)', attribute='href'):
    links = []
    # print(selector)
    #print(rows, '_________end rows_________')
    for row in rows:
        d = dict()
        # print('___________________')
        # print(row)
        # print('___________________')
        try:
            d['name'] = row.select_one(selector).text.strip()
            d['url'] = row.select_one(selector + ' a')[attribute]
            links.append(d)
        except AttributeError:
            pass
    return links




def courses_from_studyprograms(studyprograms, selector):
    # print(selector)
    courses = []
    print(studyprograms)
    for url in tqdm(studyprograms):
        #print("____________", url)
        #print(url[0]['url'])
        courses.append(rows_to_links(get_table_rows([url['url']]), selector))
        # sleep(5)
    return courses


studyprograms = rows_to_links(get_table_rows(url))
print(studyprograms)
courses = courses_from_studyprograms(studyprograms, '.course-cell')


with open('student.oslomet.json', 'w') as f:
    json.dump(courses, f)


#with open('student.oslomet.json', 'r') as f:
#    courses = json.load(f)

print(courses)

#print(courses)
#curriculums = courses_from_studyprograms(courses, 'dl > dd:nth-of-type(8)')


'''

print(courses[0:10])


def get_curriculum_page(courses):
    for course in courses:
         r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            curriculums = soup.select('table tr')
        except TypeError:
            pass
        return rows


 with open('student.oslomet.json', 'w') as f:
    json.dump(courses, f)

'''
