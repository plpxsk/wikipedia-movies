library(tidyverse)
library(magrittr)

read_tsv_append_column <- function(filename){
    ## append id from filename
    df <- read_tsv(filename)
    df$id <- strsplit(filename, "/")[[1]] %>% tail(1) %>% as.integer
    df
}
    
fix_names <- . %>% gsub(" ", "_", .) %>%
    gsub("\\(", "", .) %>%
    gsub("\\)", "", .) %>%
    tolower


sample_of_312 <- read_tsv("../data/wikipredict_data_pack/sample_of_312/sample_of_312")
names(sample_of_312) %<>% fix_names

predictors_files <- list.files(path="../data/wikipredict_data_pack/sample_of_312/wikipedia_predictors",
                               full.names=TRUE)
predictors <- lapply(predictors_files, read_tsv_append_column) %>% bind_rows
names(predictors) %<>% fix_names


## EXPLORE
qplot(sample_of_312$Number_of_theaters)

MOVIE <- "The_King%27s_Speech"
ID1 <- 117
df <- left_join(
    ##sample_of_312 %>% filter(wp_page_title==MOVIE),
    sample_of_312 %>% filter(id==ID1),
    predictors,
    by="id"
    )



## REGRESSIONS
DAYS <- -30

day_subset <- predictors %>% filter(day_movie_time==DAYS)

df <- sample_of_312 %>% select(id, title, first_weekend_revenue_usd,
                               number_of_theaters) %>%
    left_join(., day_subset, by="id") %>%
    select(-day_movie_time)


mod <- lm(first_weekend_revenue_usd ~ number_of_theaters, data=df)
mod %>% summary

mod <- lm(first_weekend_revenue_usd ~ number_of_theaters + views + users + rigor + edits,
          data=df)
mod %>% summary



