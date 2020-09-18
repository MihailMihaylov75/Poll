__author__ = 'Mihail Mihaylov'

import database
from connections import get_connection


class Option:
    """Option class"""
    def __init__(self, option_text, poll_id, _id=None):
        """
        Initialize Option class
        :param option_text: Option string
        :param poll_id: Id of the poll where option to be added
        :param _id: ID of the option
        """
        self.id = _id
        self.text = option_text
        self.poll_id = poll_id

    def __repr__(self):
        """
        String representation of the Option class
        :return: String representation of the Option class
        """
        return f"Option({self.text!r}, {self.poll_id!r}, {self.id!r})"

    def save(self):
        """
        Save option to the poll
        :return:
        """
        with get_connection() as connection:
            new_option_id = database.add_option(connection, self.text, self.poll_id)
            self.id = new_option_id

    def vote(self, username):
        """
        Save the vote to poll
        :param username: Username of the voter
        :return:
        """
        with get_connection() as connection:
            database.add_poll_vote(connection, username, self.id)

    @property
    def votes(self):
        """
        Get all votes for given option
        :return: Array of tuples of votes (user, option)
        """
        with get_connection() as connection:
            votes = database.get_votes_for_option(connection, self.id)
            return votes

    @classmethod
    def get(cls, option_id):
        """
        Get option
        :param option_id: Id of the option
        :return: option
        """
        with get_connection() as connection:
            option = database.get_option(connection, option_id)
            return cls(option[1], option[2], option[0])
