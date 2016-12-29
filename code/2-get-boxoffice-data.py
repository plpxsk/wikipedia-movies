import wikipedia
import bs4
import dill
import logging


# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# get box office data (movie_summary) from list of urls, using bom API object
def my_get_all_movies(url_dict, bom_object):
    i = 0
    for key, val in url_dict.items():
        movie = bom_object.get_movie_summary(key)
        movie.clean_data()
        if i % 50 == 0:
            print i
        i += 1
        yield movie.data


logging.info("dill.load links...")
with open('cache/1-boxoffice-links.dill', 'rb') as f:
  boxoffice_links = dill.load(f)


logging.info("Get 2015 movie titles from Wikipedia page...")
# use HTML structure and style to extract movie titles from
# https://en.wikipedia.org/wiki/2015_in_film#2015_films
page = wikipedia.page("2015_in_film")
soup = bs4.BeautifulSoup(page.html(), "lxml")
film_2015_tables = soup.findAll('table', attrs={'class': 'wikitable'})[4:8]

film_titles = []
for table in film_2015_tables:
  film_titles.append([title.text for title in table.findAll('i')])
film_titles = sum(film_titles, [])
available_films = list(
  set.intersection(set(film_titles), set(boxoffice_links.movie_urls.values())))

# need the movie urls and not titles for API download
available_movie_urls = {key: value for key, value
                        in boxoffice_links.movie_urls.iteritems()
                        if value in available_films}

logging.info("Printing some info: ")
print "Movies with box office data: ", boxoffice_links.total_movies
print "Movies from 2015, per wikipedia: ", len(film_titles)
print "Intersection: ", len(available_films)
print "Final count: ", len(available_movie_urls.items())

logging.info("Downloading box office data for each movie...")
boxoffice_2015_data = [
  item for item in my_get_all_movies(available_movie_urls, boxoffice_links)]

with open('cache/2-boxoffice-2015-data.dill', 'w') as f:
  dill.dump(boxoffice_2015_data, f)
logging.info("DONE!")
