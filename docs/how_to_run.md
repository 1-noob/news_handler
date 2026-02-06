## Requirements
+ A MongoDB database on MongoDB Compass :
    (For step by step instructions refer (this link)https://www.geeksforgeeks.org/mongodb/create-database-using-mongodb-compass/)

    The database must have following attributes:
    + `_id` : hash (primary key)
    + `Article_title` : String
    + `Category` : String
    + `URL` : String
    + `Status` : Number (default 0)
    + `Rating` : Number (default 1)

+ A config file based on config template. (Rename config_template.py to config.py and fill out the paths with paths on your device)

+ Some files:
    + `backup.json` : It acts like a backup for database. Host it on Github in a repository (in same or different location) so that you dont loose access to it.
    + `new_articles.json` & `review.json` (store them under `article_cache` subdirectory)


## Configuration
Project relies on a config.py file for storing paths and settings like:
+ Database settings
+ Backup files 
+ RSS feed source
+ Regex rules etc.

Copy the template given in the [template](https://github.com/1-noob/news_handler/blob/main/config_template.py) and then use your one file paths and MongoDB parameters

## Running the Pipeline
### 1. Run rss_feed_monitor
`python -m subroutines.rss_feed_monitor`

This fetches new articles from the news source and the output is nummber of articles discovered

### 2. Article synchronisation
`python -m subroutines.article_synchronisation
`

This applies skip rules(that tells us what articles to be skipped) and then prepares other data by applying regex based classification rules to segregate it into `new_articles.json` for successfully classified articles and `review.json` for articles that could not be classified using the rules and so user needs to classify it manually

### 3. Manual review process
Launches the CLI based manual review interface

`python -m subroutines.review_processor
`

You will be asked to 
+ Insert the article in the DB with a predefined category
+ Insert the article with a __Manually inserted__ category for the articles not fitting into any of the existing categories
+ Discard the Article

### 4. Push the commits to backup

`python -m subroutines.git_handler
`