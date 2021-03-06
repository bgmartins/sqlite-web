Extraction scripts and a web-based SQLite database browser written in Python.

Project dependencies:

* [flask](http://flask.pocoo.org)
* [pandas](https://pandas.pydata.org)
* [peewee](http://docs.peewee-orm.com)
* [pygments](http://pygments.org)
* [regex](https://pypi.org/project/regex/)
* [openpyxl](https://pypi.org/project/openpyxl/)

### Usage

```sh
$ sqlite_web /path/to/database.db
```

### Screenshots

The index page for the database browser shows some basic information about the database, including the number of tables and indexes, as well as its size on disk:

![](http://media.charlesleifer.com/blog/photos/s1415479324.32.png)

The `structure` tab displays information about the structure of the table, including columns, indexes, and foreign keys (if any exist). From this page you can also create, rename or drop columns and indexes.

![](http://media.charlesleifer.com/blog/photos/s1415479418.23.png)

The `content` tab displays all the table data. Links in the table header can be used to sort the data:

![](http://media.charlesleifer.com/blog/photos/s1415479502.61.png)

The `query` tab allows you to execute arbitrary SQL queries on a table. The query results are displayed in a table and can be exported to either JSON or CSV:

![](http://media.charlesleifer.com/blog/photos/s1415487149.3.png)

The `import` tab supports importing CSV and JSON files into a table. There is an option to automatically create columns for any unrecognized keys in the import file:

![](http://media.charlesleifer.com/blog/photos/s1415479625.44.png)

### Command-line options

The syntax for invoking sqlite-web is:

```console

$ sqlite_web [options] /path/to/database-file.db
```

The following options are available:

* ``-p``, ``--port``: default is 8080
* ``-H``, ``--host``: default is 127.0.0.1
* ``-d``, ``--debug``: default is false
* ``-x``, ``--no-browser``: do not open a web-browser when sqlite-web starts.
* ``-P``, ``--password``: prompt for password to access sqlite-web.
  Alternatively, the password can be stored in the "SQLITE_WEB_PASSWORD"
  environment variable, in which case the application will not prompt for a
  password, but will use the value from the environment.
* ``-r``, ``--read-only``: open database in read-only mode.
* ``-u``, ``--url-prefix``: URL prefix for application, e.g. "/sqlite-web".
