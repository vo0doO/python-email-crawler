from requests_html import HTMLSession
from urllib.parse import urlsplit
import os
import logging
from urllib.parse import urlencode
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

logging.makeLogRecord(LOGGING2)
logger = logging.getLogger('voodoo_logger')


def link_getter(query):
	link_a = []
	query = input('Каков будет Ваш запрос... ? ')
	query = query.replace(" ", "+").replace("(", "%28").replace(")", "%29").replace("\"", "%22")
	max_res = input('А сколько максимум будет выдано результатов ? ')
	max_int = int(max_res)
	for i in range(0, max_int, 10):
		url = f"https://www.google.com/search?q={query}&start={i}"
		session = HTMLSession()
		r = session.get(url)
		print("=" * 40)
		print('Page: %s' % url)
		print("Processing...")
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
	try:
		if sys.argv[1] is not None:
			arg = sys.argv[1].lower()
			link_getter()
		else:
			link_getter(None)
	except:
		link_getter(None)