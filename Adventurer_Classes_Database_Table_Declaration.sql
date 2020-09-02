-- Drops the adventurer if it exists currently --
DROP DATABASE IF EXISTS adventurer_matches;
-- Creates the "adventurer" database --
CREATE DATABASE adventurer_matches;
-- Make it so all of the following code will affect adventurerMatches
USE adventurer_matches;

CREATE TABLE match_scores (
-- Create a numeric column called "id" which automatically increments and cannot be null --
	id integer auto_increment,
	first_name VARCHAR(50),
	second_name VARCHAR(50),
	final_hp_p1 int,
    final_hp_p2 int,
    hp_difference VARCHAR(50),
	result VARCHAR(50),
    created_at timestamp default current_timestamp,
    primary key (id)
);

insert into match_scores (
first_name, 
second_name, 
final_hp_p1, 
final_hp_p2,
hp_difference, 
result)
values (
'Frodo',
'Smeagol',
50,
0,
50,
'Frodo wins'),
('IronMan',
'Loki',
2,
0,
2,
'IronMan wins');

select * from match_scores;