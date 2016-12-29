import wikipedia
import datetime
import requests
import logging
import pandas as pd
import dill


# log to file AND console
logging.basicConfig(level=logging.INFO,
                    filename='3-get-wikipedia-data.log')
logging.getLogger().addHandler(logging.StreamHandler())

logging.info("START: " +
             str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


# get # of views for a movie page
def get_views_by_day(title, begin, end,
                     cols=["article", "timestamp", "views"]):
  # available columns:
  # [u'access', u'agent', u'article', u'granularity', u'project', u'timestamp',
  # u'views']
  res = requests.get(VIEWS_URL + title + "/daily/" + begin + "/" + end, )
  logging.debug("Begin: " + str(begin))
  logging.debug("End: " + str(end))
  try:
    df = pd.DataFrame(res.json()["items"])[cols]
    df['title'] = title
    return df
  except:
    pass


def get_edits_users(params):
  edits = 0
  unique_user_ids = set()
  try:
    while True:
      wp_call = requests.get(API_URL, params=params)
      response = wp_call.json()
      logging.debug("Response: " + str(response))
      for page_id in response['query']['pages']:
        edits += len(response['query']['pages'][page_id]['revisions'])
        for rev in response['query']['pages'][page_id]['revisions']:
          if rev['userid'] not in unique_user_ids:
            unique_user_ids.add(rev['userid'])
      # if 'continue' in response:
      #   parameters['continue'] = response['continue']['continue']
      #   parameters['rvcontinue'] = response['continue']['rvcontinue']
      else:
        break
    return {'title': API_BASE_PARAMETERS['titles'],
            'revisions': edits,
            'users': len(unique_user_ids),
            'days_back': DAYS_BACK,
            'begin_dt': API_BASE_PARAMETERS['rvstart'],
            'end_dt': API_BASE_PARAMETERS['rvend']}
  except:
    pass


def datetime_to_str1(dt):
  return str(dt).split(" ")[0].replace("-", "")


def datetime_to_str2_begin(dt):
  return str(dt + datetime.timedelta(-DAYS_BACK)).split(" ")[0] + "T12:00:00Z"


def datetime_to_str2_release(dt):
  return str(dt).split(" ")[0] + "T23:59:00Z"


logging.debug("Loading boxoffice data...")
with open("cache/2-boxoffice-2015-data.dill", "rb") as f:
  boxoffice_data = dill.load(f)

VIEWS_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/"  # noqa
API_URL = "http://en.wikipedia.org/w/api.php"

DAYS_BACK = 30                  # days before movie release

API_BASE_PARAMETERS = {
  'action': 'query',
  'format': 'json',
  # 'formatversion': '2',
  'continue': '',
  # 'titles': title,
  'prop': 'revisions',
  'rvprop': 'ids|userid',
  'rvlimit': 'max',
  # the next 3 for a timerange
  # 'rvstart':'2016-10-20T12:00:00Z',
  # 'rvend':'2016-11-20T23:59:00Z',
  'rvdir': 'newer'}


edits_users = []
views_by_day = []

logging.debug("Downloading movie data...")
for i in range(len(boxoffice_data)):
  movie = boxoffice_data[i]['title']
  logging.debug("Release date: " + str(boxoffice_data[i]['release_date']))
  if movie is None:
    logging.error("No movie title found in boxoffice_data.")
    continue
  if boxoffice_data[i]['release_date'] is None:
    logging.error("Movie release date error in boxoffice_data.")
    continue
  release_date_str1 = datetime_to_str1(boxoffice_data[i]['release_date'])
  begin_date_str1 = datetime_to_str1(boxoffice_data[i]['release_date'] +
                                     datetime.timedelta(-DAYS_BACK))

  # TODO: movie suggestion matching can be improved
  title = wikipedia.suggest(movie)
  if wikipedia.suggest(movie) is None:
    title = wikipedia.search(movie)[0]

  logging.info("Found movie, title: " + str(movie) + ", " + str(title))
  logging.debug("Getting views...")
  views_by_day.append(get_views_by_day(title, begin_date_str1,
                                       release_date_str1))

  logging.debug("Getting edits, users...")
  API_BASE_PARAMETERS['titles'] = title
  API_BASE_PARAMETERS['rvstart'] = datetime_to_str2_begin(
    boxoffice_data[i]['release_date'])
  API_BASE_PARAMETERS['rvend'] = datetime_to_str2_release(
    boxoffice_data[i]['release_date'])
  edits_users.append(get_edits_users(API_BASE_PARAMETERS))
  logging.debug("DONE.")

logging.debug("Remove nones in edits_users...")
edits_users = [one for one in edits_users if one is not None]

logging.debug("Saving with dill...")
with open('cache/3-edits-users.dill', 'w') as f:
  dill.dump(edits_users, f)

with open('cache/3-views-by-day.dill', 'w') as f:
  dill.dump(views_by_day, f)

logging.info("END: " +
             str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
logging.info("DONE.")
