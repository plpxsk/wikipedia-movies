# Predicting movie box office revenue using pre-release wikipedia activity

Predict global box office revenue (REV) before release, using wikipedia
activity data (VURET).

Specifically:
* VURE: number of views, users, adjusted number of users ("rigor"), and edits, 30
  days before opening (or other time T), as well as
* T: number of theatres that movie was shown in, on opening day

This project inspired by Mestyan et al: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0071226#s4

In summary, by itself, T is the best predictor. By adding VURE, we may approach
80% R-squared.

## Importantly

* Using domestic boxoffice data, per Box Office Mojo
* There is a good chunk of missing data, see below




# Methods

* Scrape a wikipedia page for 2015 movie titles.
* Obtain box office data (REV), and T, using a Box Office Mojo API found on github
* Obtain VURE using wikipedia API
* Combine data with pandas
* Perform linear regression to obtain R-squared


Also, replicate the Mestyan et al data.

# Installation

If you get `bson` errors, fix with:

	pip uninstall bson
	pip uninstall pymongo
	pip install pymongo

(`pymongo` has its own `bson` per https://github.com/py-bson/bson/issues/19)


# Script notes

3-*.py takes 5 minutes


# Missing data

Some wikipedia articles (movies) have missing data. API returned error: "This
data not yet loaded"

Check `code/*log` files

Some error movies:

  * Focus (2001 vs 2015)
  * The Letters (2015), the letter 2012
  * Hot Pursuit (2015), hot pursuit 2010
  * Our Brand Is Crisis (2006), our brand is crisis 2016
  * ? Hotel Transylvania 2 (2015), Hotel Transylvania (franchise)
  * ? Aferim! (2016), Gopo Awards
  * ETC!
  
some movies don't have all the views data going back... eg Tangerine: pagevies
data only goes back 10 days...
I'm using what is available
  
# References

BoxofficemojoAPI from https://github.com/skozilla/BoxOfficeMojo
