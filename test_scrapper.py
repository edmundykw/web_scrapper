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

	html = read_page.read().decode("utf-8") #decode turns the bytes obtained from .read() to a string type.
	return(html)

def convert_to_soup(html):
	'''Extracts the entire HTML structure of the page in the URL.'''

	soup = BeautifulSoup(html, "html.parser")
	return(soup)

def extract_book_info(soup):
	'''Extract the title and author of the books within the soup object and convert it to a string.'''

	book_details = soup.find_all("div", class_="book-item")
	book_info = []
	for item in book_details:
		book_info.append(" By ".join([
			item.find(attrs={"itemprop": "name"})['content'],
			item.find(attrs={"itemprop": "contributor"})['content']]))
	return(book_info)

def save_book_info(info):
	'''Saving the book info into a CSV by rows.'''

	with open('list.csv', 'a') as f:
		writer =  csv.writer(f)
		for book in info:
			writer.writerow([book])

for page in range(1, 88):
	read_page = read_url(page)
	html_struct = get_html(read_page)
	soup = convert_to_soup(html_struct)
	info = extract_book_info(soup)
	save_book_info(info)
	time.sleep(10)
