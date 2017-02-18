#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created Time: Fri 17 Feb 2017 06:47:11 PM CST

import feedparser
from flask import Flask, render_template, request

app = Flask(__name__)

RSS_FEEDS = {'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
             'iol': "http://www.iol.co.za/cmlink/1.640"}


@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", articles=feed['entries'])


if __name__ == '__main__':
    app.run(port=5000, debug=True)
