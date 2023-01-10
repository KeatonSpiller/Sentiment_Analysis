# Changelog
This file contains the notable changes to the project

Version 1.0.0 (01-10-2022)
## New
    - Automated tweet preperation and processing of incoming long-term and short-term 
        financial analyst tweets using Tweepy's (api.user_timeline())
        This method is limited to ~ 3k tweets per user eg.(JimCramer has 123k tweets 
        and I downloaded 2950)
    - Added probability of words spoken per tweet (set sum of probability column == 1)
    - Added merged columns of long-term and short term financial analysts to index funds 
        including ( id, created_at, user, url, text, frequency, probability     
        favorite_count, retweet, count, SandP500, NASDAQ, Dow_JONES, RUSSEL )
    - Added a Linear Model to predict retweet_count as a placeholder for future stock
        market prediction

## Changes 
    - Specified the dataframe Datetime for integar string and datetime variables, 
        deciding to use UTC for Universal time zone
        {'id': 'int64',
        'created_at': 'datetime64[ns, UTC]',
        'user':'object',
        'favorite_count': 'int64',
        'retweet_count': 'int64',
        'url': 'object',
        'text': 'object'}
    - Removal of whitespace, and stop/filler words from dictionary of all words 
        spoken in twitter messages with regex and pandas filtering

## Deprecated
    - older versions of the spreadsheets have ' and misaligned spaces

## Removed
    - Binary target y created from day to day increase or decrease in index fund
        value
    - Removed some of the twitter csv files github unable to push files
        547.84 MB; this exceeds GitHub's file size limit of 100.00 MB
## Fixes
    - Fixed misnamed csv files

## Security
    - may need to sensor the twitter data in future versions
