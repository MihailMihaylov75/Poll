__author__ = 'Mihail Mihaylov'

import random

from connections import get_connection
import database

from models.poll import Poll
from models.option import Option


MENU_PROMPT = """-- Menu --

1) Create new poll
2) List open polls
3) Vote on a poll
4) Show poll votes
5) Select a random winner from a poll option
6) Exit

Enter your choice: """
NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "


def prompt_create_poll():
    """Allow the user to create a poll"""
    poll_title = input("Enter poll title: ")
    poll_owner = input("Enter poll owner: ")
    poll = Poll(poll_title, poll_owner)
    poll.save()

    new_option = input(NEW_OPTION_PROMPT)
    while new_option:
        poll.add_option(new_option)
        new_option = input(NEW_OPTION_PROMPT)


def list_open_polls():
    """Lists all opened polls"""
    for poll in Poll.all():
        print(f"{poll.id}: {poll.title} (created by {poll.owner})")


def prompt_vote_poll():
    """Allow the user to vote for a poll"""
    poll_id = int(input("Enter poll would you like to vote on: "))
    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter option you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")
    Option.get(option_id).vote(username)


def _print_poll_options(options):
    """Print all options to vote for a poll"""
    for option in options:
        print(f"{option.id}: {option.text}")


def show_poll_votes():
    """Shows all votes for chosen poll"""
    poll_id = int(input("Enter poll you would like to see votes for: "))
    poll = Poll.get(poll_id)
    options = poll.options
    votes_per_option = [len(option.votes) for option in options]
    total_votes = sum(votes_per_option)

    try:
        for option, votes in zip(options, votes_per_option):
            percentage = votes / total_votes * 100
            print(f"{option.text} for {votes} ({percentage:.2f}% of total)")
    except ZeroDivisionError:
        print("No votes yet cast for this poll.")


def randomize_poll_winner():
    """Get random winner of selected poll"""
    poll_id = int(input("Enter poll you'd like to pick a winner for: "))
    poll = Poll.get(poll_id)
    _print_poll_options(poll.options)

    option_id = int(input("Enter which is the winning option, we'll pick a random winner from voters: "))
    votes = Option.get(option_id).votes
    winner = random.choice(votes)
    print(f"The randomly selected winner is {winner[0]}.")


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner
}


def menu():
    """User menu"""

    with get_connection() as connection:
        database.create_tables(connection)

    selection = input(MENU_PROMPT)
    while selection != "6":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")
        else:
            selection = input(MENU_PROMPT)


menu()
