import dill
from boxofficemojoAPI import boxofficemojo as bom


boxoffice_links = bom.BoxOfficeMojo()
boxoffice_links.crawl_for_urls()

print "Total movies: ", boxoffice_links.total_movies

with open('cache/1-boxoffice-links.dill', 'w') as f:
    dill.dump(boxoffice_links, f)
