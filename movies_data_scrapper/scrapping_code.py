# importing the libraries

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import csv

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read the HTML from the URL and pass on to BeautifulSoup
url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
print("Opening the file connection...")
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Empty list to hold all the http links in the HTML page
movie_links = []

# Find all the href tags and store them in the list movie_links
for atag in soup.find_all('td', {"class": "titleColumn"}):
	movie_links.append(atag.find('a').get('href'))

# The standard web address
standard_url = 'https://www.imdb.com'

# writing the column labels for the csv file  
row = ['movie_name', 'movie_year', 'movie_rating', 'no_ratings', 'movie_length', 'genre1', 'genre2', 'genre3', 'genre4' , 'summary', 'director_name', 'writer1', 'writer2', 'writer3', 'keyword1', 'keyword2', 'keyword3', 'keyword4', "keyword5", 'budget', 'gross_usa', 'production_company', 'cumulative_gross_word', 'movie_length_min', 'sound_mix', 'star1', 'star2', 'star3', 'star4', 'star5', 'release_date_act', 'release_country']
with open('moviestest.csv', 'a', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(row)

# Defining a function to get the required data points from the html page passed as link
def movie_data(link):

	# concatenation of the link with the standard url
	mov_url = standard_url + link		
	mov_html = urllib.request.urlopen(mov_url, context=ctx).read()
	mov_soup = BeautifulSoup(mov_html, 'html.parser')

	# Getting the data from the html page 
	movie_name = mov_soup.find('h1').text[:-8]

	movie_year = mov_soup.find('span', {"id": "titleYear"}).find('a').text[-4:]

	movie_rating = mov_soup.find('div', {"class": "ratingValue"}).find('span').text

	no_ratings = mov_soup.find('span', {"class": "small"}).text	

	movie_length = mov_soup.find('time').text.strip()

	genre = mov_soup.find_all('div', {"class": "see-more inline canwrap"})

	# Making the genres to store in a empty list and inserting null value if index out of range until 3 positions

	genre_list = []

	if ((genre[1].find('h4').text) == 'Genres:'):
		for i in genre[1].find_all('a'):
			genre_list.append((i.text).strip())

		if(len(genre_list) < 2):
			genre_list.insert(1,'null')
			genre_list.insert(2,'null')
			genre_list.insert(3,'null')

		if(len(genre_list) < 3):
			genre_list.insert(2,'null')
			genre_list.insert(3,'null')

		if(len(genre_list) < 4):
			genre_list.insert(3,'null')


	summary = mov_soup.find('div', {"class": "summary_text"}).text.strip()

	keywords = mov_soup.find('div', {"class": "see-more inline canwrap"}).find_all('a')

	# Making the keywords to store in a empty list and inserting null value if index out of range until 4 positions
	keywords_list = []

	for i in keywords:
		keywords_list.append((i.text).strip())

	if(len(keywords_list) < 2):
		keywords_list.insert(1,'null')
		keywords_list.insert(2,'null')
		keywords_list.insert(3,'null')
		keywords_list.insert(4,'null')

	if(len(keywords_list) < 3):
		keywords_list.insert(2,'null')
		keywords_list.insert(3,'null')
		keywords_list.insert(4,'null')

	if(len(keywords_list) < 4):
		keywords_list.insert(3,'null')
		keywords_list.insert(4,'null')

	if(len(keywords_list) < 5):
		keywords_list.insert(4,'null')


	# Assigning all the instances of the class txt-block to a varible in order to iterate 

	div_txt_block = (mov_soup.find_all('div', {"class": "txt-block"}))

	# Assigning dummy values for the varibles before iteration

	production_company = 'notfound'
	budget = gross_usa = cumulative_gross_word = movie_length_min = ''
	budget = ''
	release_date_act = ''
	release_country = ''

	# Empty list to store the technical specs of the sound 
	sound_mix = []

	# Iterating over instances of class txt-block to get the data points present in it 
	for htags in div_txt_block:
		try:		
			item_name = htags.find('h4', {"class": "inline"}).text
			
			# Checking the label for the datapoint required and getting the data only if the condition is satisfied

			if(item_name == 'Budget:'):
				budget = (htags.find('h4',{'class','inline'}).next_sibling).strip()

			if(item_name == 'Production Co:'):
				production_company = (htags.find('a').text).strip()

			if(item_name == 'Gross USA:'):
				gross_usa = (htags.find('h4',{'class','inline'}).next_sibling).strip()

			if(item_name == 'Cumulative Worldwide Gross:'):
				cumulative_gross_word = (htags.find('h4',{'class','inline'}).next_sibling).strip()

			if(item_name == 'Runtime:'):
				movie_length_min = ((htags.find('time').text).replace("min","")).strip()


			if(item_name == 'Sound Mix:'):
				sound_mixsoup = htags.find_all('a')
				for i in sound_mixsoup:
					sound_mix.append(i.text)

			# Filtering the data for the release date which contains country name along with it 

			if(item_name == 'Release Date:'):
				release_date = htags.find('h4',{'class','inline'}).next_sibling
				start = release_date.find( '(' )
				end = release_date.find( ')' )
				if start != -1 and end != -1:
				  	release_country = release_date[start+1:end]
				  	result2 = release_date.replace(release_country,"")
				  	result3 = result2.replace("(","")
				  	result4 = result3.replace(")","")
				  	release_date_act = result4.strip()

		except:
	 		pass

	# Assigning the dummy values for the varible before iteration	
	director_name = 'notfound'

	# Empty list to store the movie stars name 
	stars_list = []

	# Empty list to store the movie writers name
	writer_list = []

	# Iterating over instances of class credit_summary_item to get the data points present in it 
	div_credit_summary = mov_soup.find_all('div', {"class": "credit_summary_item"})

	for tags_list in div_credit_summary:
		try:		
			# Checking the label for the datapoint required and getting the data only if the condition is satisfied

			var_name = tags_list.find('h4', {"class": "inline"}).text

			if(var_name == 'Director:'):
				director_name = tags_list.find('a').text


			if(var_name == 'Stars:'):
				starsmix = tags_list.find_all('a')
				for i in starsmix:
					stars_list.append(i.text)

			if(var_name == 'Writer:' or var_name == 'Writers:'):
				writers = tags_list.find_all('a')
				for i in writers:
					writer_list.append(i.text)
		except:
	 		pass

	# inserting null values for the writers list until position 4 if no value found 

	if(len(writer_list) < 2):
		writer_list.insert(1,'null')
		writer_list.insert(2,'null')

	if(len(writer_list) < 3):
		writer_list.insert(2,'null')

	# inserting null values for the stars list until position 4 if no value found 

	if(len(stars_list) < 2):
		stars_list.insert(1,'null')
		stars_list.insert(2,'null')
		stars_list.insert(3,'null')
		stars_list.insert(4,'null')

	if(len(stars_list) < 3):
		stars_list.insert(2,'null')
		stars_list.insert(3,'null')
		stars_list.insert(4,'null')

	if(len(stars_list) < 4):
		stars_list.insert(3,'null')
		stars_list.insert(4,'null')

	if(len(stars_list) < 5):
		stars_list.insert(4,'null')

	# Writing the data to the csv file 

	row = [movie_name, movie_year, movie_rating, no_ratings, movie_length, genre_list[0], genre_list[1], genre_list[2], genre_list[3] , summary, director_name, writer_list[0], writer_list[1], writer_list[2], keywords_list[0], keywords_list[1], keywords_list[2], keywords_list[3], keywords_list[4], budget, gross_usa, production_company, cumulative_gross_word, movie_length_min, sound_mix, stars_list[0], stars_list[1], stars_list[2], stars_list[3], stars_list[4], release_date_act, release_country]

	with open("moviesimdb.csv", "a", newline="") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)

	# Printing the movie name on the output screen to know if the data has been extracted 
	print(movie_name)

# Empty list to save the exumpted links from the function
exception_links = []

# Calling the function and iterating over the list of links
for link in movie_links:
	try:
		movie_data(link)
	except:
		pass

