#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created Time: Fri 17 Feb 2017 06:47:11 PM CST

import feedparser
from flask import Flask

app = Flask(__name__)

BBC_FEEDS = {'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
             'cnn': "http://rss.cnn.com/rss/edition.rss",
             'fox': "http://feeds.foxnews.com/fornews/latest",
             'iol': "http://www.iol.co.za/cmlink/1.640"}


@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(BBC_FEEDS[publication])
    first_article = feed['entries'][0]
    return """<html>
  <body>
    <h1>Headlines </h1>
    <b>{0}</b> <br/>
    <i>{1}</b> <br/>
    <p>{2}</p> <br/>
  </body>
</html>""".format(first_article.get("title"),
                  first_article.get("published"),
                  first_article.get("summary"))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
