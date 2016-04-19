--Create a database called tournament and connect to it
--Note: the drop database line is for ease of use during testing
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;


--Create two tables: players and matches
CREATE TABLE players (
	id			SERIAL PRIMARY KEY,
	full_name 	TEXT
);

CREATE TABLE matches (
	id 			SERIAL PRIMARY KEY,
	winner_id	INTEGER REFERENCES players (id),
	loser_id	INTEGER REFERENCES players (id)
);


--Create views for the playerStandings() function in tournament.py
--The wins_v view lists each players id, name, and number of wins
CREATE VIEW wins_v AS
	SELECT players.id AS id, players.full_name AS name, COUNT(matches.winner_id) AS wins
	FROM players
	LEFT JOIN matches
	ON players.id = matches.winner_id
	GROUP BY players.id
	ORDER BY wins DESC;

--The matches_v view lists the number of matches each player has played
CREATE VIEW matches_v AS
	SELECT players.id AS player_id, COUNT(players.id) AS matches
	FROM players
    JOIN matches
    ON players.id = matches.winner_id or players.id = matches.loser_id
    GROUP BY players.id;

--The standings_v view combines the wins_v and matches_v views with a left join
CREATE VIEW standings_v AS
	SELECT id, name, wins, COALESCE(matches, 0) AS matches
	FROM wins_v
	LEFT JOIN matches_v
	ON wins_v.id = matches_v.player_id
	ORDER BY wins DESC;

--Attribution notes:
--Udacity course developer 'PhilipCoach' helped me understand how to combine two different views in a third view (see: https://discussions.udacity.com/t/views-playerstandings/15415/7)
--Udacity forum user 'Brian_Bradshaw' introduced me to the coalesce function and helped me understand how to use it (see: https://discussions.udacity.com/t/views-playerstandings/15415/12)
--Stack Overflow user 'radar' also helped me understand the coalesce function (see: http://stackoverflow.com/questions/27300552/postgresql-select-case-coalesce)


--Create views for the swissPairings() function in tournament.py
--The row_num_v view simply recreates the standings_v view and adds a row_number column
CREATE VIEW row_num_v AS
	SELECT *, ROW_NUMBER() OVER(ORDER BY standings_v.wins)
	FROM standings_v
	ORDER BY wins DESC;

--The evens_v view lists all players with an even-numbered row_number
CREATE VIEW evens_v AS
	SELECT id, name, wins, ROW_NUMBER() OVER(ORDER BY row_num_v.wins)
	FROM row_num_v
	WHERE row_number % 2 = 0
	ORDER BY wins DESC;

--The odds_v view lists all players with an odd-numbered row_number
CREATE VIEW odds_v AS
	SELECT id, name, wins, ROW_NUMBER() OVER(ORDER BY row_num_v.wins)
	FROM row_num_v
	WHERE row_number % 2 != 0
	ORDER BY wins DESC;

--The pairings_v view combines the evens_v and odds_v views together with a full outer join
CREATE VIEW pairings_v AS
	SELECT evens_v.id AS id1, evens_v.name AS name1, odds_v.id AS id2, odds_v.name AS name2
	FROM evens_v
	FULL OUTER JOIN odds_v
	ON evens_v.row_number = odds_v.row_number;

--Attribution notes: 
--GIS Stack Exchange user 'geographika' helped me understand how to use the row_number() function (see: http://gis.stackexchange.com/questions/12233/in-postgis-is-it-possible-to-create-a-view-with-a-unique-id)
--A blog entry at jooq.org also helped me with the row_number() function (see: https://blog.jooq.org/2014/08/12/the-difference-between-row_number-rank-and-dense_rank/)
--Stack Overflow user 'OMG ponies' helped me understand how to use the modulo function (see: http://stackoverflow.com/questions/3756928/select-row-if-the-value-2-1-mod)