from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import time

def read_url(page):
	'''Opens and read the url to get the html structure of the page.'''

	url = f"https://www.bookdepository.com/wishlists/WCR55G?page={page}"
	read_page = urlopen(url)
	return(read_page)

def get_html(read_page):
	'''Reads the page to get its HTML structure'''

	html = read_page.read().decode("utf-8") #decode turns the bytes obtain from .read() to a string type.
	return(html)

def convert_to_soup(html):
	'''Extracts the entire HTML structure of the page in the URL.'''

	soup = BeautifulSoup(html, "html.parser")
	return(soup)

def extract_book_info(soup):
	'''Extract the title and author of the books within the soup object and convert it to a string.'''

	book_details= soup.find_all("div", class_="book-item")
	book_info = []
	for item in book_details:
		book_info.append(" By ".join([
			item.find(attrs={"itemprop": "name"})['content'],
			item.find(attrs={"itemprop": "contributor"})['content']
		]))
	return(book_info)

def save_book_info(info):
	'''Saving the book info into a CSV by rows.'''

	file = open('booklist.csv', 'a')
	file =  csv.writer(file)
	for book in info:
		file.writerow([book])

for page in range(1, 88):
	read_page = read_url(page)
	html_struct = get_html(read_page)
	soup = convert_to_soup(html_struct)
	info = extract_book_info(soup)
	save_book_info(info)
	time.sleep(10)
	

""" The codes below are equivalent
new_list = []
for title in [authors_strings, book_strings]:
    new_list.append(title)
author_with_titles = [title for title in [book_strings, authors_strings]] """


""" book_titles = soup.find_all("meta", attrs={"itemprop": "name"})
	book_authors = soup.find_all("meta", attrs={"itemprop": "contributor"})
	book_strings = [titles['content'] for titles in book_titles]
	authors_strings = [author['content'] for author in book_authors]
	convert_to_zip = zip(book_strings, authors_strings) """
