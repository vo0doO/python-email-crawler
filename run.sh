#!/usr/bin/env bash

echo "Запущен генератор ссылок..."

python3.6 $HOME/PycharmProjects/python-email-crawler/get_link_for_crawler.py && \

echo "Ссылки сгенерированны" && \

echo "Запущен кравлер" && \

python2.7 $HOME/PycharmProjects/python-email-crawler/email_crawler.py && \

echo "Кравлер отработал, идет процесс генерации csv файлов" && \

python2.7 $HOME/PycharmProjects/python-email-crawler/email_crawler.py --emails && \

python2.7 $HOME/PycharmProjects/python-email-crawler/email_crawler.py --domains && \

echo "Работа завершена"