import logging.config
import re
import traceback
import urllib2
import urlparse
from urllib import urlencode
from bs4 import BeautifulSoup
from database import CrawlerDb
from settings import LOGGING, EMAILS_FILENAME, DOMAINS_FILENAME, ADDONS_INFO_FILENAME
import socket
socket.setdefaulttimeout(1.0)

# Debugging
# import pdb;pdb.set_trace()

# Logging
logging.config.dictConfig(LOGGING)
logger = logging.getLogger("crawler_logger")
google_adurl_regex = re.compile('adurl=(.*?)"')
google_url_regex = re.compile('url\?q=(.*?)&amp;sa=')
email_regex = re.compile('([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})', re.IGNORECASE)
url_regex = re.compile('<a\s.*?href=[\'"](.*?)[\'"].*?>')
# belowUrl_regexWillMeetWith <<Castrophic Backtracking>>!
# http://stackoverflow.com/questions/8010005/python-re-infinite-execution
# url_regex = re.compile('<a\s(?:.*?\s)*?href=[\'"](.*?)[\'"].*?>')

db = CrawlerDb()
db.connect()


def crawl(keywords, MAX_SEARCH_RESULTS, NICE_LINKS):

	logger.info("-" * 40)
	logger.info("Keywords to Google for: %s" % keywords.decode('utf-8'))
	logger.info("-" * 40)

	query = {"q": keywords}
	# Step 0: up nice link
	for url in NICE_LINKS:
		db.enqueue(unicode(url))
	# Step. 0.1: up links of image search in db.
	url = 'http://www.google.com/search?' + urlencode(query) + '&source=lnms&tbm=isch&sa=X&ved=0'
	search_url_anal(url)


	# Step 1: GooglePageScan
	# eg http://www.google.com/search?q=singapore+web+development&start=0
	# Next page: https://www.google.com/search?q=singapore+web+development&start=10
	# Google search results are paginated by 10 URLs each. There are also adurls
	for page_index in range(0, MAX_SEARCH_RESULTS, 10):
		url = 'http://www.google.com/search?' + urlencode(query) + '&start=' + str(page_index)
		search_url_anal(url)

	# Step 2: Crawl each of the search result
	# We search till level 2 deep
	while (True):
		# Dequeue an uncrawled webpage from db
		uncrawled = db.dequeue()
		if (uncrawled == False):
			break
		email_set = find_emails_2_level_deep(uncrawled.url)
		if (len(email_set) > 0):
			db.crawled(uncrawled, ",".join(list(email_set)))
		else:
			db.crawled(uncrawled, None)


def search_url_anal(url):
	"""
	Url of search result parse and add or not in quen
	:param url: url of google search result
	:return:
	"""
	try:
		data = retrieve_html(url)
		soup = BeautifulSoup(data, 'html.parser')
		links_soup = [link.get("href").replace('/url?q=', '') for link in soup.find_all('a')]
		for url in google_url_regex.findall(data):
			netloc = urlparse.urlsplit(url).netloc
			if netloc != "":
				if not netloc.startswith("http://") or not netloc.startswith("https://"):
					if url.startswith("http://"):
						netloc = "http://" + netloc
					elif url.startswith("https://"):
						netloc = "https://" + netloc
					else:
						netloc = "http://" + netloc
						url = "http://" + netloc
				if 'google' not in netloc:
					if 'blogger' not in netloc:
						if 'youtube' not in netloc:
							db.enqueue(unicode(netloc))
							db.enqueue(unicode(url))

		for url in google_adurl_regex.findall(data):
			netloc = urlparse.urlsplit(url).netloc
			if netloc != "":
				if not netloc.startswith("http://") or not netloc.startswith("https://"):
					if url.startswith("http://"):
						netloc = "http://" + netloc
					elif url.startswith("https://"):
						netloc = "https://" + netloc
					else:
						netloc = "http://" + netloc
						url = "http://" + netloc
				if 'google' not in netloc:
					if 'blogger' not in netloc:
						if 'youtube' not in netloc:
							db.enqueue(unicode(netloc))
							db.enqueue(unicode(url))

		for url in links_soup:
			netloc = urlparse.urlsplit(url).netloc
			if netloc != "":
				if not netloc.startswith("http://") or not netloc.startswith("https://"):
					if url.startswith("http://"):
						netloc = "http://" + netloc
					elif url.startswith("https://"):
						netloc = "https://" + netloc
					else:
						netloc = "http://" + netloc
						url = "http://" + netloc
				if 'google' not in netloc:
					if 'blogger' not in netloc:
						if 'youtube' not in netloc:
							db.enqueue(unicode(netloc))
							db.enqueue(unicode(url))

	except Exception as e:
		logger.error("ERROR %s" % e)


def retrieve_html(url):
	"""
	Crawl a website, and returns the whole html as an ascii string.

	On any error, return.
	"""

	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Just-Crawling 0.1')
	request = None
	status = 0

	try:
		logger.info("Crawling %s" % url)
		request = urllib2.urlopen(req)
	except urllib2.URLError, e:
		logger.error("Exception at url: %s\n%s" % (url, e))
	except urllib2.HTTPError, e:
		status = e.code
	except Exception, e:
		return
	if status == 0:
		status = 200

	try:
		data = request.read()
	except Exception, e:
		return

	db.save_html(data)
	return str(data)


def find_emails_2_level_deep(url):
	"""
	Find the email at level 1.
	If there is an email, good. Return that email
	Else, find in level 2. Store all results in database directly, and return None
	"""
	"""
	try:
		html = retrieve_html(url)
	except Exception, e:
		logger.error("ERROR CONNECION: %s" % e)
		logger.info("Start http test...")
		if urlparse.urlparse(url).scheme == 'http':
			connect = httplib.HTTPConnection(urlparse.urlparse(url).netloc)
			connect.request('GET', "")
			r1 = connect.getresponse()
			if r1.getheader('Location') == "".join([urlparse.urlparse(url).scheme, "://", urlparse.urlparse(url).netloc, '/']):
				logger.info("Url %s is good !" % str(url))
			else:
				url = r1.getheader('Location')
		elif urlparse.urlparse(url).scheme == 'https':
			connect = httplib.HTTPSConnection(urlparse.urlparse(url).netloc)
			connect.request('GET', "")
			r1 = connect.getresponse()
			if r1.getheader('Location') == "".join(
					[urlparse.urlparse(url).scheme, "://", urlparse.urlparse(url).netloc, '/']):
				logger.info("Url %s is good !" % str(url))
			else:
				url = r1.getheader('Location')
		else:
			logger.warning("WTF ??? URL SCHEME NOT HTTP AND NOT HTTP !?!?!?!?")
	except Exception, e:
		logger.error("HTTP TEST ERROR: %s" % e)
		"""
	html = retrieve_html(url)

	email_set = find_emails_in_html(html)

	if (len(email_set) > 0):
		# If there is a email, we stop at level 1.
		return email_set

	else:
		# No email at level 1. Crawl level 2
		logger.info('No email at level 1.. proceeding to crawl level 2')

		link_set = find_links_in_html_with_same_hostname(url, html)
		tested_links = db.url_from_test()
		link_set = set(link_set).difference(set(tested_links))
		link_set = set(link_set).difference(set(map(lambda x: x.replace('http', 'https'), tested_links)))
		link_set = list(link_set)
		for link in link_set:
			if "http://www.harveynorman.co.nz/store-finder.html" in str(link):
				link_set.remove(link)
			elif "https://stores.harveynorman.co.nz" in str(link):
				link_set.remove(link)
		for link in link_set:
			# Crawl them right away!
			# Enqueue them too
			html = retrieve_html(link)
			if (html == None):
				continue
			email_set = find_emails_in_html(html)
			db.enqueue(link, list(email_set))
		# We return an empty set
		return set()


def find_emails_in_html(html):
	if (html == None):
		return set()
	email_set = set()
	for email in email_regex.findall(html):
		email_set.add(email)
	return email_set


def find_links_in_html_with_same_hostname(url, html):
	"""
	Find all the links with same hostname as url
	"""
	if (html == None):
		return set()
	url = urlparse.urlparse(url)
	links = url_regex.findall(html)
	soup = BeautifulSoup(html, 'html.parser')
	try:
		links_soup = [link.get("href").replace('/url?q=', '') for link in soup.find_all('a')]
	except Exception, e:
		logger.error("Error in link %s" % e)
		links_soup = [link.get("href") for link in soup.find_all('a')]
	if len(links) and len(links_soup) != 0:
		links.__add__(list(set(links_soup).difference(set(links))))
	else:
		logger.warning("In url 0 links !")
	link_set = set()
	for link in links:
		if link == None:
			continue
		try:
			link = str(link)
			if link.startswith("/") and not link.startswith("//"):
				link_set.add('http://' + url.netloc + link)
			elif link.startswith("http") or link.startswith("https"):
				if (link.find(url.netloc)):
					link_set.add(link)
			elif link.startswith("#"):
				continue
			else:
				link_set.add(urlparse.urljoin(url.geturl(), link))
		except Exception, e:
			pass

	return link_set


if __name__ == "__main__":
	import sys

	try:
		arg = sys.argv[1].lower()
		if (arg == '--emails') or (arg == '-e'):
			# Get all the emails and save in a CSV
			logger.info("=" * 40)
			logger.info("Processing...")
			emails = db.get_all_emails()
			logger.info("There are %d emails" % len(emails))
			file = open(EMAILS_FILENAME, "w+")
			file.writelines("\n".join(emails))
			file.close()
			logger.info("All emails saved to ./data/emails.csv")
			logger.info("=" * 40)
		elif (arg == '--domains') or (arg == '-d'):
			# Get all the domains and save in a CSV
			logger.info("=" * 40)
			logger.info("Processing...")
			domains = db.get_all_domains()
			logger.info("There are %d domains" % len(domains))
			file = open(DOMAINS_FILENAME, "w+")
			file.writelines("\n".join(domains))
			file.close()
			logger.info("All domains saved to ./data/domains.csv")
			logger.info("=" * 40)
		# OPEN, READ FILE GET AND SEND FROM CRAWL
		elif (arg == '--auto') or (arg == '-a'):
			logger.info("=" * 40)
			logger.info("Processing...")
			logger.info("There are automatic starts...")
			CAHE = []
			KEYWORDS = ""
			MAX_SEARCH_RESULTS = ""
			NICE_LINKS = []
			with open(ADDONS_INFO_FILENAME, 'r') as f:
				lines = f.readlines()
				for line in lines:
					CAHE.append(line)
			KEYWORDS = CAHE[0].split("||")[0]
			logger.info('Crawl up your search keywords: %s' % KEYWORDS)
			MAX_SEARCH_RESULTS = CAHE[0].split("||")[-1]
			logger.info('Crawl up your max result: %s' % MAX_SEARCH_RESULTS)
			MAX_SEARCH_RESULTS = int(MAX_SEARCH_RESULTS)
			for ln in CAHE[1:-1]:
				NICE_LINKS.append('http://' + str(ln).replace('\n', ''))
			logger.info('Crawl up %s nice links !' % str(len(set(NICE_LINKS))))
			logger.info("All addon integration complete")
			logger.info("=" * 40)
			crawl(KEYWORDS, MAX_SEARCH_RESULTS, NICE_LINKS)
		else:
			# Crawl the supplied keywords!
			crawl(arg, MAX_SEARCH_RESULTS=None, NICE_LINKS=None)

	except KeyboardInterrupt:
		logger.error("Stopping (KeyboardInterrupt)")
		sys.exit()
	except Exception, e:
		logger.error("EXCEPTION: %s " % e)
		traceback.print_exc()