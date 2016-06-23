-- MBTA SUBWAY 'THE T' STATION DATABASE
-- Created by Benjamin Call and Alexander Fleetwood

CREATE DATABASE IF NOT EXISTS MBTA_Subway;

USE MBTA_Subway;

DROP TABLE IF EXISTS Line;

CREATE TABLE Line
(
	color				ENUM('Red', 'Orange', 'Green', 'Blue', 'Silver') NOT NULL,
	subline				VARCHAR(30) NOT NULL,
    direction			VARCHAR(30) NOT NULL,
    -- direction is not needed for uniqueness, just a use field for the application

    CONSTRAINT line_pk
		PRIMARY KEY(color, subline)
);

DROP TABLE IF EXISTS Station;

CREATE TABLE Station
(
	station_name	VARCHAR(30)		PRIMARY KEY		NOT NULL,
    address			VARCHAR(100),

    first_line		ENUM('red', 'orange', 'green', 'blue', 'silver') NOT NULL 		REFERENCES Line(color),
    first_subline	VARCHAR(30)										 NOT NULL		REFERENCES Line(subline),

	second_line		ENUM('red', 'orange', 'green', 'blue', 'silver') DEFAULT NULL   REFERENCES Line(color),
    second_subline	VARCHAR(30)										 DEFAULT NULL	REFERENCES Line(subline),

	third_line		ENUM('red', 'orange', 'green', 'blue', 'silver') DEFAULT NULL   REFERENCES Line(color),
    third_subline	VARCHAR(30)										 DEFAULT NULL	REFERENCES Line(subline),

    CONSTRAINT first_line_fk
		FOREIGN KEY (first_line, first_subline) 	REFERENCES Line(color, subline),
	CONSTRAINT second_line_fk
		FOREIGN KEY (second_line, second_subline) 	REFERENCES Line(color, subline),
	CONSTRAINT third_line_fk
		FOREIGN KEY (third_line, third_subline) 	REFERENCES Line(color, subline)
);

DROP TABLE IF EXISTS Track;

CREATE TABLE Track
(
	first_station	VARCHAR(30)		NOT NULL	REFERENCES Station(station_name),
    second_station	VARCHAR(30)		NOT NULL 	REFERENCES Station(station_name),

    CONSTRAINT track_pk
		PRIMARY KEY (first_station, second_station),
	CONSTRAINT first_station_fk
		FOREIGN KEY (first_station) 	REFERENCES Station(station_name),
	CONSTRAINT second_station_fk
		FOREIGN KEY (second_station) 	REFERENCES Station(station_name)
);

 SELECT * FROM Line;