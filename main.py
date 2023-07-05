import requests
import psycopg2
from bs4 import BeautifulSoup

links = ['http://books.toscrape.com/catalogue/category/books/mystery_3/index.html',
         'http://books.toscrape.com/catalogue/category/books/philosophy_7/index.html',
         ]
list=[]
def get_book_data(url):
    html_txt = requests.get(url).text
    soup = BeautifulSoup(html_txt, 'html.parser')
    genre=soup.find('ul',class_='breadcrumb').find_all('li')[2].text.strip()
    page = soup.find('article', class_='product_page')
    title = page.h1.string[0:150]
    rating_content = soup.find('div', class_='col-sm-6 product_main').find_all('p')[2]
    rating_number = rating_content['class'][1]
    if rating_number == 'One':
        rating = 1
    elif rating_number == 'Two':
        rating = 2
    elif rating_number == 'Three':
        rating = 3
    elif rating_number == 'Four':
        rating = 4
    else:
        rating = 5
    description = page.find_all('p')[3].string[0:500]
    table_contents = page.find('table').find_all('td')
    upc = table_contents[0].string
    p_type = table_contents[1].string
    price_e = table_contents[2].string[1:]
    price_i = table_contents[3].string[1:]
    tax = table_contents[4].string[1:]
    temp = table_contents[5].string
    review_no = table_contents[6].string
    avail = 0
    for ch in temp:
        if ch.isnumeric():
            avail = avail * 10 + int(ch)
    print(title)
    tup=(title,rating,description,upc,p_type,price_e,price_i,tax,avail,review_no,genre)
    list.append(tup)

def scrape_from_page(url):
    html_txt = requests.get(url).text
    soup = BeautifulSoup(html_txt, 'html.parser')
    box = soup.find_all('article', class_='product_pod')
    for i in box:
        if i.h3.a['href'][0] != '.':
            link = 'http://books.toscrape.com/' + i.h3.a['href']
        else:
            link = 'http://books.toscrape.com/catalogue/' + i.h3.a['href'][9:]
        get_book_data(link)









for url in links:
    scrape_from_page(url)
    html_txt = requests.get(url).text
    soup = BeautifulSoup(html_txt, 'html.parser')
    next_link = soup.find('li', class_='next')
    while (next_link != None):
        next_link = next_link.a['href']
        ind = url.rindex('/')  # returns 6 if in complex case
        if ind == 6:
            next_link = url + '/' + next_link
        else:
            next_link = url[0:ind] + '/' + next_link
        scrape_from_page(next_link)
        url = next_link
        html_txt = requests.get(url).text
        soup = BeautifulSoup(html_txt, 'html.parser')
        next_link = soup.find('li', class_='next')

conn = psycopg2.connect(database="clone", user = "postgres", password = "password", host = "127.0.0.1", port = "5433")
cur=conn.cursor()
cur.execute('DROP TABLE IF EXISTS books')
create_comm='''CREATE TABLE IF NOT EXISTS  books(
                title varchar(150),
                rating varchar(2),
                description varchar(501),
                upc varchar(25),
                product_type varchar(10),
                tax_excluded varchar(10),
                tax_included varchar(10),
                tax varchar(10),
                availability varchar(3),
                no_of_review varchar(5),
                genre varchar(20))'''
cur.execute(create_comm)

insert_comm='insert into books (title,rating,description,upc,product_type,tax_excluded,tax_included,tax,availability,no_of_review,genre) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
for data in list:
    cur.execute(insert_comm, data)

conn.commit()
cur.close()
conn.close()








# for link in links:
#     page_val = requests.get(link).text
#     extract = BeautifulSoup(page_val, 'html.parser')
#     nex_val=extract.find('li',class_='next')
#     print(nex_val,link)


# boxes=soup.find_all('tr',class_='css-1cxc880')
#
# for box in boxes:
#     count=box.find('td',class_='css-w6jew4').text
#     name=box.find('p',class_='chakra-text css-rkws3').text
#     code=box.find('span',class_='chakra-text css-1jj7b1a').text
#     current=box.find('p',class_='chakra-text css-5a8n3t').text
#     print(f'{count} : {name}({code}) - \ncurrent price : {current}\n')
