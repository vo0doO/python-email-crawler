import requests_html
from urllib.parse import urlsplit
import os


def link_getter(query):
	link_a = []
	qq = { "q": query}
	max_res = int(raw_input('Max result ? '))
	for i in range(0, max_res, 10):
		url = 'https://www.google.com/search?q={query}&start={i}&sa=N&filter=0'
		session = requests_html.HTMLSession()
		r = session.get(url)
		for link in r.html.absolute_links:
			if 'google' not in link:
				if 'blogger' not in link:
					if 'youtube' not in link:
						link = urlsplit(link).netloc
						if link not in link_a:
							link_a.append(link)
							print(link)
	with open(os.path.dirname(os.path.abspath(__file__)) + '/link_for_crawler.txt', 'w') as f:
		for ln in set(link_a):
			print(ln)
			f.write(ln + "\n")

if __name__ == "__main__":
	import sys
	arg = sys.argv[1].lower()
	link_getter(arg)