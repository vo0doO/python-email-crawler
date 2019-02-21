Python Email Анализатор
====================

Этот скрипт Python выполняет поиск / поиск по определенным ключевым словам в Google, сканирует веб-страницы по результатам и возвращает все найденные электронные ящики.

Требования
------- 

- sqlalchemy
- urllib2
- python2.7
- python3.6
- requests-html
- bs4

Если у вас нет, просто
------- 
	
	`~$ sudo pip2 install sqlalchemy bs4 && sudo apt install python3.6 && sudo apt install python3-pip && python3.6 -m pip install requests-html` 


Использование
-------
Укажите Shell где искать Crawler, установив значерение переменой EMAIL_CRAWLER_HOME равной пути к папке с Crawler
	
	~$ export EMAIL_CRAWLER_HOME=/home/node/PycharmProjects/python-email-crawler
Начните поиск с ключевого слова и максимума возвращаемых результатов. Мы используем «buy (emf OR geiger OR TDS OR "blood pressure" OR "massaging pad") (monitor OR sensor OR detector) -soeks -Amazon -google -blogger -YouTube -ebay» в качестве примера.
	
	~$ $EMAIL_CRAWLER_HOME/run.sh
	>>>Запущен генератор ссылок...
	>>>Какой будет запрос ?: buy (emf OR geiger OR TDS OR "blood pressure" OR "massaging pad") (monitor OR sensor OR detector) -soeks -Amazon -google -blogger -YouTube -ebay
	>>>Максимум возвращенных ответов ?: 500

По сути в этот момент и дальше происходит следующее просто уже без нашего участия.
	
	~$ cp $EMAIL_CRAWLER_HOME/data/crawler.sqlite $EMAIL_CRAWLER_HOME/backup/last-crawler.sqlite
    ~$ cp $EMAIL_CRAWLER_HOME/data/emails.csv $EMAIL_CRAWLER_HOME/backup/last-emails.csv
    ~$ cp $EMAIL_CRAWLER_HOME/link_for_crawler.txt $EMAIL_CRAWLER_HOME/backup/last-link_for_crawler.txt
    ~$ cp $EMAIL_CRAWLER_HOME/data/domains.csv $EMAIL_CRAWLER_HOME/backup/last-domains.csv
	~$ python3.6 $EMAIL_CRAWLER_HOME/get_link_for_crawler.py
    ~$ python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --auto
    ~$ python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --emails
    ~$ python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --domains

Процесс поиска и сканирования займет много времени, поскольку он извлекает максимальное кол-во результатов поиска сайтов и изображений из Google, доступных в браузере. 

Сканирует 2 уровня начиная с места куда ссылался Google, и 2 уровня начиная с базового url домена. 

С одного захода получается около: 
- 20 000 веб-страниц;
- 2 000 доменов:
- 1 500 email адресов

На последок !
-------
В любой момент уже после завершения процесса запустите эту команду, чтобы востановить список ящиков
	
	python2.7 email_crawler.py --emails

Письма будут сохранены в ./data/emails.csv

И список уникальных доменов
	
	python2.7 email_crawler.py --domains

Домены будут сохранены в ./data/emails.csv

Или если хотите повторить тот же запрос
	
	python2.7 email_crawler.py --auto

А если хотите сгенерировать достоверно полный список уникальных сайтов из раздачи гугл по любому вашему запросу
	
	python3.6 get_link_for_crawler.py
