import dill
import pandas as pd

with open("../cache/2-boxoffice-2015-data.dill", "rb") as f:
  boxoffice = dill.load(f)
with open("../cache/3-edits-users.dill", "rb") as f:
  edits_users = dill.load(f)
with open("../cache/3-views-by-day.dill", "rb") as f:
  views = dill.load(f)

boxoffice_df = pd.DataFrame(boxoffice)

edits_users = [one for one in edits_users if one is not None]
edits_users_df = pd.DataFrame(edits_users)

views_df = pd.concat(views)

boxoffice_df.to_csv("../cache/boxoffice.csv")
edits_users_df.to_csv("../cache/edits_users.csv")
views_df.to_csv("../cache/views.csv")
