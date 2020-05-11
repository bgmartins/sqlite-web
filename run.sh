#!/bin/sh
rm -rf rep-database.db rep-database.zip
sqlite3 rep-database.db < rep-database.sql
zip rep-database.zip rep-database.db
python3 sqlite_web.py -p 1337 -H localhost
rm -rf rep-database.db

