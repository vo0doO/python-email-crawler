#!/usr/bin/env bash

echo "Выполняется резервное копирование данных..."

cp $EMAIL_CRAWLER_HOME/data/crawler.sqlite $EMAIL_CRAWLER_HOME/backup/last-crawler.sqlite && \
cp $EMAIL_CRAWLER_HOME/data/emails.csv $EMAIL_CRAWLER_HOME/backup/last-emails.csv && \
cp $EMAIL_CRAWLER_HOME/link_for_crawler.txt $EMAIL_CRAWLER_HOME/backup/last-link_for_crawler.txt && \
cp $EMAIL_CRAWLER_HOME/data/domains.csv $EMAIL_CRAWLER_HOME/backup/last-domains.csv && \

echo "Запущен генератор ссылок..." && \

python3.6 $EMAIL_CRAWLER_HOME/get_link_for_crawler.py && \

echo "Ссылки сгенерированны" && \

echo "Запущен кравлер" && \

python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --auto && \

echo "Кравлер отработал, идет процесс генерации csv файлов" && \

python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --emails && \

python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --domains && \

echo "Работа завершена"