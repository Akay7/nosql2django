import feedparser

d = feedparser.parse('https://www.reddit.com/r/news/.rss')

print(d['feed'].keys())
# print(len(d['feed']))

habr = feedparser.parse('https://habrahabr.ru/rss/hubs/all/')

# print(d['feed']['author'].keys())
import ipdb; ipdb.set_trace()