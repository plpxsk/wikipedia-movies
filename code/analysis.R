library(tidyverse)
library(magrittr)
library(lubridate)

## eg: 2015072700 - remove last 2 positions, and convert to date
to_ymd <- . %>% as.character %>% substr(., 1, nchar(.)-2) %>% ymd
standardize_title <- . %>% tolower %>% gsub(" \\([^()]+\\)", "", .)

boxoffice <- read_csv("../cache/boxoffice.csv") %>% select(-X1)
views <- read_csv("../cache/views.csv") %>% select(-X1)
edits_users <- read_csv("../cache/edits_users.csv") %>% select(-X1)

views$timestamp %<>% to_ymd
boxoffice$title %<>% standardize_title
views$title %<>% standardize_title
edits_users$title %<>% standardize_title

views30 <- views %>%
    group_by(article) %>%
    arrange(timestamp) %>%
    slice(1) %>%
    ungroup

df1 <- left_join(
    views30,
    edits_users %>% select(-end_dt),
    by="title") 

## check some rows
## df1 %>% select(title, timestamp, begin_dt) %>% sample_n(10)
## eg, tangerine
## views %>% filter(article=="Tangerine")

df1 %<>% select(title, views, revisions, users) %>% na.omit

df <- df1 %>%
    left_join(
        .,
        boxoffice %>% select(title, domestic, genre, mpaa_rating, production_budget, runtime),
        by="title")


mod <- lm(domestic ~ views + revisions + users, data=df)
mod %>% summary


