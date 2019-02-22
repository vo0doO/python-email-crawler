Python Email Анализатор
====================

Этот скрипт Python выполняет " .. / .. / .. / поиск / поиск " по определенным ключевым словам в Google, сканирует веб-страницы по результатам и возвращает все найденные электронные ящики.
Требования
------------

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

Начните поиск с ключевого слова. Мы используем «buy (emf OR geiger OR TDS OR "blood pressure" OR "massaging pad") (monitor OR sensor OR detector) -soeks -Amazon -google -blogger -YouTube -ebay» в качестве примера.
	
	~$ python3.6 get_link_for_crawler.py
	
	>>>Какой будет запрос ?: buy (emf OR geiger OR TDS OR "blood pressure" OR "massaging pad") (monitor OR sensor OR detector) -soeks -Amazon -google -blogger -YouTube -ebay
	
	>>>Максимум возвращенных ответов ?: 500

Получится файл `link_for_crawler.txt`, его нужно скопировать в кореневую папку программы, если случайно он создался не там, и выполнить следующею команду.
	
	~$ python2.7 email_crawler.py "buy (emf OR geiger OR TDS OR "blood pressure" OR "massaging pad") (monitor OR sensor OR detector) -soeks -Amazon -google -blogger -YouTube -ebay"

Процесс поиска и сканирования займет много времени, поскольку он извлекает до 500 результатов поиска (из Google) и сканирует до 2 уровня начиная с хрен знает какого уровня, и 2 уровня начиная с базового адреса сайта полученного из поисковой выдачи и из выдачи изображений. Это должно ползти около 10000 веб-страниц :)
После завершения процесса запустите эту команду, чтобы получить список ящиков
	
	python2.7 email_crawler.py --emails

Письма будут сохранены в ./data/emails.csv

И список уникальных доменов
	
	python2.7 email_crawler.py --domains

Домены будут сохранены в ./data/emails.csv
