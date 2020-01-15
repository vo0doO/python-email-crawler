<div id="readme" class="readme blob instapaper_body js-code-block-container">
<article class="markdown-body entry-content" itemprop="text"><h1><a id="user-content-python-email-анализатор" class="anchor" aria-hidden="true" href="#python-email-анализатор"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Python Email Анализатор</h1>
<p>Этот скрипт Python выполняет поиск / поиск по определенным ключевым словам в Google, сканирует веб-страницы по результатам и возвращает все найденные электронные ящики.</p>
<h2><a id="user-content-требования" class="anchor" aria-hidden="true" href="#требования"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Требования</h2>
<ul>
<li>sqlalchemy</li>
<li>urllib2</li>
<li>python2.7</li>
<li>python3.6</li>
<li>requests-html</li>
<li>bs4</li>
</ul>
<h2><a id="user-content-Устанавливаем" class="anchor" aria-hidden="true" href="#если-у-вас-нет-просто"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Если у вас нет, просто</h2>
<pre><code>`~$ sudo pip2 install sqlalchemy bs4 &amp;&amp; sudo apt install python3.6 &amp;&amp; sudo apt install python3-pip &amp;&amp; python3.6 -m pip install requests-html` 
</code></pre>
<h2><a id="user-content-использование" class="anchor" aria-hidden="true" href="#использование"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Использование</h2>
<p>Укажите Shell где искать Crawler, установив значерение переменой EMAIL_CRAWLER_HOME равной пути к папке с Crawler</p>
<pre><code>~$ export EMAIL_CRAWLER_HOME=/home/node/PycharmProjects/python-email-crawler
</code></pre>
<p>Начните поиск с ключевого слова и максимума возвращаемых результатов. Мы используем «buy (emf OR geiger OR TDS OR "blood pressure" OR "massaging pad") (monitor OR sensor OR detector) -soeks -Amazon -google -blogger -YouTube -ebay» в качестве примера.</p>
<pre><code>~$ $EMAIL_CRAWLER_HOME/run.sh
&gt;&gt;&gt;Запущен генератор ссылок...
&gt;&gt;&gt;Какой будет запрос ?: buy (emf OR geiger OR TDS OR "blood pressure" OR "massaging pad") (monitor OR sensor OR detector) -soeks -Amazon -google -blogger -YouTube -ebay
&gt;&gt;&gt;Максимум возвращенных ответов ?: 500
</code></pre>
<p>По сути в этот момент и дальше происходит следующее просто уже без нашего участия.</p>
<pre><code>~$ cp $EMAIL_CRAWLER_HOME/data/crawler.sqlite $EMAIL_CRAWLER_HOME/backup/last-crawler.sqlite
~$ cp $EMAIL_CRAWLER_HOME/data/emails.csv $EMAIL_CRAWLER_HOME/backup/last-emails.csv
~$ cp $EMAIL_CRAWLER_HOME/link_for_crawler.txt $EMAIL_CRAWLER_HOME/backup/last-link_for_crawler.txt
~$ cp $EMAIL_CRAWLER_HOME/data/domains.csv $EMAIL_CRAWLER_HOME/backup/last-domains.csv
~$ python3.6 $EMAIL_CRAWLER_HOME/get_link_for_crawler.py
~$ python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --auto
~$ python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --emails
~$ python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --domains
</code></pre>
<p>Процесс поиска и сканирования займет много времени, поскольку он извлекает максимальное кол-во результатов поиска сайтов и изображений из Google, доступных в браузере.</p>
<p>Сканирует 2 уровня начиная с места куда ссылался Google, и 2 уровня начиная с базового url домена.</p>
<p>С одного захода получается около:</p>
<ul>
<li>20 000 веб-страниц;</li>
<li>2 000 доменов:</li>
<li>1 500 email адресов</li>
</ul>
<h2><a id="user-content-на-последок-" class="anchor" aria-hidden="true" href="#на-последок-"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>На последок !</h2>
<p>В любой момент уже после завершения процесса запустите эту команду, чтобы востановить список ящиков</p>
<pre><code>python2.7 email_crawler.py --emails
</code></pre>
<p>Письма будут сохранены в ./data/emails.csv</p>
<p>И список уникальных доменов</p>
<pre><code>python2.7 email_crawler.py --domains
</code></pre>
<p>Домены будут сохранены в ./data/emails.csv</p>
<p>Или если хотите повторить тот же запрос</p>
<pre><code>python2.7 email_crawler.py --auto
</code></pre>
<p>А если хотите сгенерировать достоверно полный список уникальных сайтов из раздачи гугл по любому вашему запросу</p>
<pre><code>python3.6 get_link_for_crawler.py
</code></pre>
</article>
  </div>
