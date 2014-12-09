## TODO:

- [ ] Do a list of keywords we want to convert to hashtags as a json file
- [ ] If a keyword has more children as sub-keywords, those are going to be appended to the tweet, no more than two
- [ ] Create a tweetify method that will take the title and short it plus add "..."
- [ ] If a tweet is more than 140 chars and the last word is a hashtag, delete the hashtag
- [ ] Create a method that will save the new feed in a `.temp` file then compare it to the `db.txt` and only pull the links that are not duplicated, these are the ones that we'll short the links
- [ ] buffer api request part
- [ ] If buffer response with an error, throw error requesting more api calls
- [ ] Figure out how to put config files inside a folder at `~/`
- [ ] Take a screenshot of the website and send it to buffer/twitter (using selenium)
