__author__ = 'Mihail Mihaylov'

import database
from models.option import Option
from connections import get_connection


class Poll:
    """Poll class"""
    def __init__(self, title, owner, _id):
        """
        Initialize
        :param title: Title of the poll
        :param owner: Owner of the poll
        :param _id: ID of the poll
        """
        self.title = title
        self.owner = owner
        self.id = _id

    def __repr__(self) -> str:
        """
        Representation of the Poll class
        :return: string representation
        """
        return f"Poll({self.title!r}, {self.owner!r}, {self.id!r})"

    def save(self):
        """
        Save new poll into db
        :return:
        """
        with get_connection() as connection:
            new_poll_id = database.create_poll(connection, self.title, self.owner)
            self.id = new_poll_id

    def add_option(self, option_text):
        """
        Add new option to the poll
        :param option_text: Poll option text
        :return:
        """
        Option(option_text, self.id).save()

    @property
    def options(self):
        """
        Get all option of poll
        :return: Options of the poll
        """
        with get_connection() as connection:
            options = database.get_poll_options(connection, self.id)
            return [Option(option[1], option[2], option[0]) for option in options]

    @classmethod
    def get(cls, poll_id):
        """
        Gte poll by ID
        :param poll_id: ID of the poll
        :return: Poll instance
        """
        with get_connection() as connection:
            poll = database.get_poll(connection, poll_id)
            return cls(poll[1], poll[2], poll[0])

    @classmethod
    def all(cls):
        """
        Get all polls
        :return: array of polls
        """
        with get_connection() as connection:
            polls = database.get_polls(connection)
            return [cls(poll[1], poll[2], poll[0]) for poll in polls]

    @classmethod
    def latest(cls):
        """
        Get latest poll
        :return: The latest created poll
        """
        with get_connection() as connection:
            poll = database.get_latest_poll(connection)
            return cls(poll[1], poll[2], poll[0])
