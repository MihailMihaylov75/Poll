__author__ = 'Mihail Mihaylov'

from contextlib import contextmanager

# Create tables into the DB
CREATE_POLLS = "CREATE TABLE IF NOT EXISTS polls (id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"
CREATE_OPTIONS = "CREATE TABLE IF NOT EXISTS options (id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER);"
CREATE_VOTES = "CREATE TABLE IF NOT EXISTS votes (username TEXT, option_id INTEGER, vote_timestamp INTEGER);"

# Selections
SELECT_ALL_POLLS = "SELECT * FROM polls;"
SELECT_POLL = "SELECT * FROM polls WHERE id = %s;"
SELECT_LATEST_POLL = """SELECT * FROM polls
WHERE polls.id = (
    SELECT id FROM polls ORDER BY id DESC LIMIT 1
);"""
SELECT_POLL_OPTIONS = "SELECT * FROM options WHERE poll_id = %s;"
SELECT_OPTION = "SELECT * FROM options WHERE id = %s;"
SELECT_VOTES_FOR_OPTION = "SELECT * FROM votes WHERE option_id = %s;"

# Inserts
INSERT_POLL_RETURN_ID = "INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"
INSERT_OPTION = "INSERT INTO options (option_text, poll_id) VALUES (%s, %s) RETURNING id;"
INSERT_VOTE = "INSERT INTO votes (username, option_id, vote_timestamp) VALUES (%s, %s, %s);"


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables(connection):
    """"Create the needed tables into the DB"""
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_POLLS)
        cursor.execute(CREATE_OPTIONS)
        cursor.execute(CREATE_VOTES)


# polls
def create_poll(connection, title, owner):
    """
    Create poll
    :param connection: connection
    :param title: Title of the poll
    :param owner: Owner of the poll
    :return: poll ID
    """
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_POLL_RETURN_ID, (title, owner))

        poll_id = cursor.fetchone()[0]
        return poll_id


def get_polls(connection):
    """
    Get all created polls
    :param connection: connection
    :return: All created polls
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_POLLS)
        return cursor.fetchall()


def get_poll(connection, poll_id):
    """
    Get poll by ID
    :param connection: connection
    :param poll_id: poll id
    :return:
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL, (poll_id,))
        return cursor.fetchone()


def get_latest_poll(connection):
    """
    Get latest created poll
    :param connection: poll
    :return: Latest created poll
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_LATEST_POLL)
        return cursor.fetchall()


# options
def get_poll_options(connection, poll_id):
    """
    Get option of the given poll
    :param connection: connection
    :param poll_id: poll id
    :return: All options of the poll
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL_OPTIONS, (poll_id,))
        return cursor.fetchall()


def get_option(connection, option_id):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_OPTION, (option_id,))
        return cursor.fetchone()


def add_option(connection, option_text, poll_id):
    """
    Add option to given poll
    :param connection: connection
    :param option_text: Text of the option
    :param poll_id: poll id
    :return:
    """
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_OPTION, (option_text, poll_id))


# votes
def get_votes_for_option(connection, option_id):
    """
    Get votes for given option.
    :param connection: connection
    :param option_id: option ID
    :return: votes for given option
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_VOTES_FOR_OPTION, (option_id,))
        return cursor.fetchall()


def add_poll_vote(connection, username, option_id):
    """
    Vote for given poll
    :param connection: connection
    :param username: Username of the voter
    :param option_id: User option vote
    :return:
    """
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_VOTE, (username, option_id))
