from requests_html import HTMLSession
from urllib.parse import urlsplit
from urllib.parse import urlencode
import time
import logging

LOGGING2 = {						# dictConfig for output stream and file logging
	'version': 1,
	'disable_existing_loggers': False,

	'formatters': {
		'console': {
			'format': '[%(asctime)s] %(levelname)s::%(module)s - %(message)s',
		},
		'file': {
			'format': '[%(asctime)s] %(levelname)s::(P:%(process)d T:%(thread)d)::%(module)s - %(message)s',
		},
	},

	'handlers': {
		'console': {
			'class': 'ColorStreamHandler.ColorStreamHandler',
			'formatter':'console',
			'level': 'DEBUG',
			'use_colors': True,
		},
		'file': {
			'class': 'logging.handlers.TimedRotatingFileHandler',
			'formatter':'file',
			'level': 'INFO',
			'when': 'midnight',
			'filename': 'logs/pycrawler.log',
			'interval': 1,
			'backupCount': 0,
			'encoding': None,
			'delay': False,
			'utc': False,
		},
	},

	'loggers': {
		'voodoo_logger': {
			'handlers': ['console', 'file'],
			'level': 'DEBUG' if True else 'INFO',
			'propagate': True,
		},
	}
}
ADDONS_INFO_FILENAME = 'link_for_crawler.txt'

logging.makeLogRecord(LOGGING2)
logger = logging.getLogger('voodoo_logger')


def link_getter(query, max_res):
	link_a = []
	query_url = query.replace(" ", "+").replace("(", "%28").replace(")", "%29").replace("\"", "%22")
	max_int = int(max_res)
	for i in range(0, max_int, 10):
		url = f"https://www.google.com/search?q={query_url}&start={i}"
		session = HTMLSession()
		print("=" * 40)
		print('Search from page: %s' % url)
		print("Processing...")
		r = session.get(url)
		for link in r.html.absolute_links:
			if 'google' not in link:
				if 'blogger' not in link:
					if 'youtube' not in link:
						link = urlsplit(link).netloc
						if link not in set(link_a):
							link_a.append(link)
							print(f"New domain: {link} !!!")
							print("I'm search next >>> ")
							time.sleep(0.035)
	with open(ADDONS_INFO_FILENAME, 'w') as f:
		f.write(str(query)+'||'+str(max_res) + "\n")
		for ln in set(link_a):
			print(ln)
			f.write(ln + "\n")


if __name__ == "__main__":
	query = input('Каков будет Ваш запрос... ? ')
	max_res = input('А сколько максимум будет выдано результатов ? ')
	link_getter(query, max_res)
