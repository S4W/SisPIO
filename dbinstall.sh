#! /bin/bash
sudo apt-get -y install python-psycopg2 postgresql
sudo rm -v -f databases/*
sudo -u postgres dropdb "SisPIO"
sudo -u postgres dropuser "SisPIO"
sudo -u postgres createuser -PE -s "SisPIO"
sudo -u postgres createdb -O "SisPIO" -E UTF8 "SisPIO"
