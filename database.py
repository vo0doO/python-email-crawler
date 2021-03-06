import os
import urlparse

from sqlalchemy import create_engine, Table, Column, Integer, Unicode, Boolean, MetaData, select


DATABASE_NAME = 'data/crawler.sqlite'
HTML_DIR = 'index.html'


# noinspection PyMethodFirstArgAssignment,PyMethodFirstArgAssignment
class CrawlerDb:

	def __init__(self):
		self.connected = False

	def connect(self):

		self.engine = create_engine('sqlite:///' + DATABASE_NAME)
		self.connection = self.engine.connect()
		self.connected = True if self.connection else False
		self.metadata = MetaData()

		# Define the tables
		self.website_table = Table('website', self.metadata,
								   Column('id', Integer, primary_key=True),
								   Column('url', Unicode, nullable=False),
								   Column('has_crawled', Boolean, default=False),
								   Column('emails', Unicode, nullable=True),
								   )

		# Create the tables
		self.metadata.create_all(self.engine)

	def enqueue(self, url, emails=None):
		if not self.connected:
			return False

		s = select([self.website_table]).where(self.website_table.c.url == url)
		res = self.connection.execute(s)
		result = res.fetchall()
		res.close()
		# If we get a result, then this url is not unique
		if len(result) > 0:
			print 'Duplicated: %s' % url
			return False

		args = [{'url': unicode(url)}]
		if (emails is not None):
			args = [{'url': unicode(url), 'has_crawled': True, 'emails': unicode(",".join(emails))}]
		result = self.connection.execute(self.website_table.insert(), args)
		if result:
			print "URL ADD IN QUEUEN: %s" % str(url)
			return True
		return False

	def dequeue(self):
		if not self.connected:
			return False
		# Get the first thing in the queue
		s = select([self.website_table]).limit(1).where(self.website_table.c.has_crawled == False)
		res = self.connection.execute(s)
		result = res.fetchall()
		res.close()
		# If we get a result
		if len(result) > 0:
			# Remove from the queue ?
			# delres = self.connection.execute(self.queue_table.delete().where(self.queue_table.c.id == result[0][0]))
			# if not delres:
			# 	return False
			# Return the row
			# print result[0].url
			return result[0]
		return False

	def crawled(self, website, new_emails=None):
		if not self.connected:
			return False
		stmt = self.website_table.update() \
			.where(self.website_table.c.id == website.id) \
			.values(has_crawled=True, emails=new_emails)
		self.connection.execute(stmt)

	def url_from_test(self):
		if not self.connected:
			return False

		s = select([self.website_table]).where(self.website_table.c.has_crawled == True)
		res = self.connection.execute(s)
		result = res.fetchall()
		res.close()
		crawled_urls = []
		for i in result:
			crawled_urls.append(i[1])
		return crawled_urls

	def get_all_emails(self):
		if not self.connected:
			return None

		s = select([self.website_table])
		res = self.connection.execute(s)
		results = res.fetchall()
		res.close()
		email_set = set()
		for result in results:
			if (result.emails == None):
				continue
			for email in result.emails.split(','):
				if '.png' in email or '.jpg' in email or '.jpeg' in email:
					continue
				email_set.add(email)

		return email_set

	def get_all_domains(self):
		if not self.connected:
			return None

		s = select([self.website_table])
		res = self.connection.execute(s)
		results = res.fetchall()
		res.close()
		domain_set = set()
		for result in results:
			if (result.url == None):
				continue
			url = urlparse.urlparse(result.url)
			hostname = url.netloc
			# Simplistic assumeption of a domain. If 2nd last name is <4 char, then it has 3 parts eg. just2us.com.sg
			domain_set.add(hostname)

		return domain_set

	def close(self):
		self.connection.close()

	# noinspection PyMethodFirstArgAssignment,PyMethodFirstArgAssignment
	def save_html(filename, html):
		# noinspection PyMethodFirstArgAssignment,PyMethodFirstArgAssignment
		filename = os.path.dirname(os.path.abspath(__file__)) + '/data/index.html'
		file = open(filename, "a+")
		file.writelines(html)
		file.close()

	def test(self):
		c = CrawlerDb()
		c.connect()
		# c.enqueue(['a12222', '11'])
		# c.enqueue(['dddaaaaaa2', '22'])
		c.enqueue('111')
		c.enqueue('222')
		website = c.dequeue()
		c.crawled(website)
		website = c.dequeue()
		c.crawled(website, "a,b")
		print '---'
		c.dequeue()

# CrawlerDb().test()
