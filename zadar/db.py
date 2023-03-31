import sqlite3

import click
from flask import current_app, g

# This function returns a connection to the database, 
# creating one if it doesn't exist yet. It uses the 
# Flask g object to store the connection, which is a 
# context-global object that is available during a 
# request and is automatically cleared at the end of
# the request.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row
    
    return g.db

# This function closes the database connection, if 
# it exists. It is used as a cleanup function that 
# is called at the end of a request, to ensure that 
# the connection is properly closed and doesn't 
# remain open.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# This function initializes the database by executing
# the SQL commands in the schema.sql file, which is 
# assumed to be located in the instance folder of the
# Flask application. The get_db() function is used to
# get a database connection, and the SQL commands are
# executed using the executescript() method of the 
# connection object.
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# This function is a Flask command that calls init_db()
# to initialize the database and prints a message to 
# indicate that the operation was successful. It uses 
# the Click library to define a command line interface
# for the Flask application, allowing the user to run
# the command flask init-db to initialize the database.
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

# The init_app() function is used to initialize a Flask 
# application by registering two commands and a cleanup 
# function. It can be called in the main application code 
# to initialize the Flask application object with the 
# necessary configuration and commands for database 
# initialization.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)