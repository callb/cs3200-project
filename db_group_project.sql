-- MBTA SUBWAY 'THE T' STATION DATABASE
-- Created by Benjamin Call and Alexander Fleetwood

CREATE DATABASE IF NOT EXISTS MBTA_Subway;

USE MBTA_Subway;

DROP TABLE IF EXISTS Line;

CREATE TABLE Line
(
	color				ENUM('red', 'orange', 'green', 'blue', 'silver') NOT NULL,
	subline				VARCHAR(30) NOT NULL,
    
	week_open_time		TIME,
    week_close_time		TIME,
	week_rush_service	INT,
    week_midday_service	INT,
    week_even_service	INT,
    week_night_service	INT,

    sat_open_time		TIME,
    sat_close_time		TIME,
    sat_AM_service		INT,
    sat_PM_service		INT,
    sat_even_service	INT,
    sat_night_service	INT,

    sun_open_time		TIME,
    sun_close_time		TIME,
    sun_AM_service		INT,
    sun_PM_service		INT,
    sun_even_service	INT,
    sun_night_service	INT,

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

-- Clears all records
SET SQL_SAFE_UPDATES = 0;
DELETE FROM Line;

-- Inserts records
INSERT INTO Line 
(	color,
	subline,
	week_open_time,
    week_close_time,
	week_rush_service,
    week_midday_service,
    week_even_service,
    week_night_service,
    sat_open_time,
    sat_close_time,
    sat_AM_service,
    sat_PM_service,
    sat_even_service,
    sat_night_service,
    sun_open_time,
    sun_close_time,
    sun_AM_service,
    sun_PM_service,
    sun_even_service,
    sun_night_service
)
VALUES
('red', 'Alewife',
 time_format("05:24AM", "%h:%i%p"),
 time_format("00:15AM", "%h:%i%p"),
 9, 14, 12, 12,
 time_format("05:24AM", "%h:%i%p"),
 time_format("00:15AM", "%h:%i%p"),
 14, 14, 14, 14,
 time_format("06:08AM", "%h:%i%p"),
 time_format("00:15AM", "%h:%i%p"),
 16, 16, 16, 16
 );
 
 SELECT * FROM Line;