#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created Time: Fri 17 Feb 2017 06:47:11 PM CST

import datetime
import json
import urllib
import feedparser
from flask import Flask, render_template, request, make_response


app = Flask(__name__)

RSS_FEEDS = {'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
             'iol': "http://www.iol.co.za/cmlink/1.640"}
DEFAULTS = {'publication': 'bbc',
            'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'
            }
WEATHER_URL = ("http://api.openweathermap.org/data/2.5/weather"
               "?q={}&units=metric&appid=415d0e1a6978a16a80908b080bac3ee9")
CURRENCY_URL = ("http://api.fixer.io/latest")


@app.route("/")
def home():
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    city = get_value_with_fallback("city")
    weather = get_weather(city)

    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rates(currency_from, currency_to)

    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather,
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(currencies)
                                             ))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url).read().decode()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   "country": parsed['sys']['country']
                   }
    return weather


def get_rates(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read().decode()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate, parsed.keys())


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


if __name__ == '__main__':
    app.run(port=5000, debug=True)
