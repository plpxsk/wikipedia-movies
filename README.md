# Predicting movie box office revenue using pre-release wikipedia activity

**Objective**: To predict movie box office revenue (REV) before its release (e.g., 30 days), using wikipedia
activity data (VURET).

This is an exploratory analysis.

The key predictors of box office revenue are:

* VURE: number of Views, Users, adjusted number of users ("Rigor"), and Edits - **30
  days before opening** (or other time *t*), as well as
* T: number of theatres that movie was shown in, on opening day

This project inspired by Mestyan et al: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0071226#s4

In summary, by itself, T is the best predictor. By adding VURE, we may approach
80% R-squared.

Notes:

* 2015 movies
* domestic boxoffice data, per Box Office Mojo
* there is a good chunk of missing data, see below

# Methods

* Scrape a wikipedia page for 2015 movie titles.
* Obtain box office data (REV), and T, using a Box Office Mojo API found on github
* Obtain VURE using wikipedia API (2 separate APIs)
* Combine data with pandas
* Perform linear regression to obtain R-squared

Also, replicate the Mestyan et al data from their source.

# Installation

If you get `bson` errors, fix with:

	pip uninstall bson
	pip uninstall pymongo
	pip install pymongo

(`pymongo` has its own `bson` per https://github.com/py-bson/bson/issues/19)


# Script notes

Use Makefile (run `make help`), or run python scripts from this directory (eg,
`python code/1-get-boxoffice-links.py`)

No script should take more than 5 minutes to run.


# Limitations

Movie titles are different depending on the source (wikipedia vs
BoxOfficeMojo). They were standardized using simple rules, and better results
could be obtained with more effort. 

## Missing data

Some wikipedia articles (movies) have missing data. API returned error: "This
data not yet loaded"

Check `code/*log` files

Some error movies, whether missing or due to imprecise merging:

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
  
# References/Resources

BoxofficemojoAPI from https://github.com/skozilla/BoxOfficeMojo

This project inspired by Mestyan et al: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0071226#s4
