#!/usr/bin/env bash

echo "Запущен генератор ссылок..."

python3.6 $EMAIL_CRAWLER_HOME/get_link_for_crawler.py && \

echo "Ссылки сгенерированны" && \

echo "Запущен кравлер" && \

python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --auto && \

echo "Кравлер отработал, идет процесс генерации csv файлов" && \

python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --emails && \

python2.7 $EMAIL_CRAWLER_HOME/email_crawler.py --domains && \

echo "Работа завершена"