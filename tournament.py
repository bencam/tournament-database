#!/usr/bin/env python


'''
The tournament.py file is a module that uses the psycopg2 library to query a PostgreSQL database system.

The module includes seven functions:

1. The connect() function connects to the PostgreSQL database and returns a connection.

2. The deleteMatches() function deletes all match record entries in the database

3. The deletePlayers() function deletes all player entries in the database.

4. The countPlayers() function returns the number of player entries in the database.

5. The registerPlayer(name) function enables a user to add a new player record into the database. The user passes a player's name as a parameter, and the database assigns the player a unique ID.

6. The playerStandings() function returns a list of tuples, with each tuple containing the ID, name, number of wins, and number of matches played for every registered player. The list is sorted by wins (the player with the most number of wins appears at the top of the list).

7. The reportMatch(winner, loser) function enables a user to input the results of each match into the database. The swissPairings() function returns a list indicating how the players should be paired for the next round of matches (according to the Swiss-system tournament method). The list is composed of tuples, with each tuple containing the IDs and names of the paired players.

'''


import psycopg2


def connect():
    """Connect to the PostgreSQL database. Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print("Error: Failed to connect")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM matches"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM players"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    query = "SELECT COUNT(players.id) FROM players"
    c.execute(query)
    count = c.fetchone()[0]     # Posts by Udacity forum mentor 'skh' helped me figure this part out (see: https://discussions.udacity.com/t/p3-commands-work-in-psql-shell-but-not-in-tournament-test-script/45508/6).  # NOQA
    db.commit()
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player. (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    query = "INSERT INTO players (full_name) VALUES (%s)"
    c.execute(query, (name, ))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    query = "SELECT * FROM standings_v"
    c.execute(query)
    standings = c.fetchall()
    db.commit()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    query = "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)"
    c.execute(query, (winner, loser, ))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings. Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    query = "SELECT * FROM pairings_v"
    c.execute(query)
    swiss_pairings = c.fetchall()
    db.commit()
    db.close()
    return swiss_pairings

