-- MBTA SUBWAY 'THE T' STATION DATABASE
-- Created by Benjamin Call and Alexander Fleetwood

CREATE DATABASE IF NOT EXISTS MBTA_Subway;

USE MBTA_Subway;

DROP TABLE IF EXISTS Station;

CREATE TABLE Station
(
	color				ENUM('Red', 'Orange', 'Green-B', 'Green-C', 'Green-D', 'Green-E', 'Blue') NOT NULL,
	subline				VARCHAR(30) NOT NULL,
    direction			VARCHAR(30) NOT NULL,
    -- direction is not needed for uniqueness, just a use field for the application
    station_name		VARCHAR(30) NOT NULL,
    arrival_time_one	TIME 		DEFAULT NULL,
    arrival_time_two	TIME 		DEFAULT NULL,
    arrival_time_three	TIME 		DEFAULT NULL,
    
    CONSTRAINT line_pk
		PRIMARY KEY(color, subline, station_name)
);

DROP TABLE IF EXISTS Track;

DROP TABLE IF EXISTS User;
CREATE TABLE User
(
	name	VARCHAR(30),
    username VARCHAR(30) PRIMARY KEY,
    password VARCHAR(30)
);

CREATE TABLE Track
(
	user 					VARCHAR(30)		NOT NULL,
	first_color				ENUM('Red', 'Orange', 'Green-B', 'Green-C', 'Green-D', 'Green-E', 'Blue') NOT NULL,
	first_subline			VARCHAR(30) 	NOT NULL,
	first_station			VARCHAR(30)		NOT NULL,
    -- direction is not needed for uniqueness, just a use field for the application
	dest_color				ENUM('Red', 'Orange', 'Green-B', 'Green-C', 'Green-D', 'Green-E', 'Blue') NOT NULL,
	dest_subline			VARCHAR(30) 	NOT NULL,
    dest_station			VARCHAR(30)		NOT NULL,

    CONSTRAINT track_pk
		PRIMARY KEY (user, first_color, first_subline, first_station, dest_color, dest_subline, dest_station),
	CONSTRAINT first_station_fk
		FOREIGN KEY (first_color, first_subline, first_station) REFERENCES Station(color, subline, station_name),
	CONSTRAINT second_station_fk
		FOREIGN KEY (dest_color, dest_subline, dest_station) 	REFERENCES Station(color, subline, station_name),
	CONSTRAINT user_fk
		FOREIGN KEY (user)										REFERENCES User(username)
);

SELECT * FROM Station;
