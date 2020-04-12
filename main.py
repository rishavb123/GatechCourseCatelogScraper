from bs4 import BeautifulSoup
import urllib.request
import numpy as np

url1 = input("Enter the first url: ")
url2 = input("Enter the second url: ")
# url1 = "http://catalog.gatech.edu/programs/theory-intelligence-computer-science-bs/#requirementstext"
# url2 = "http://catalog.gatech.edu/programs/mathematics-discrete-bs/"

def scrape(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    odd_rows = soup.select('.odd')
    even_rows = soup.select('.even')
    rows = odd_rows + even_rows
    for row in rows:
        if 'areaheader' in row.get('class'):
            rows.remove(row)
    rows = list(filter(lambda row: row.find('a') is not None and row.find('a').get_text()[-4:].isdigit(), rows))
    
    categories = [row.find('a').getText()[0:-5].replace('or ', '') for row in rows]
    codes = [int(row.find('a').getText()[-4:]) for row in rows]
    names = [row.find_all('td')[1].getText() for row in rows]
    return categories, codes, names

def print_row(data, index):
    categories, codes, names = data
    data = list(zip(categories, codes, names))[index]
    print("%-5s%-10d%s" % data)
    # print(category, str(code) + "\t" + name)

categories, codes, names = data = scrape(url1)
categories2, codes2, names2 = data2 = scrape(url2)

i = 0
while i < len(codes):
    if codes[i] not in codes2:
        del categories[i]
        del codes[i]
        del names[i]
    else:
        i += 1

data = (categories, codes, names)
for i in range(len(categories)):
    print_row(data, i)
print(len(categories), "courses overlapped")