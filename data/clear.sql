DROP database Medical;

CREATE database Medical;

USE Medical;

CREATE TABLE patients(
        year INT(20),
        name VARCHAR(50),
        illness VARCHAR(50),
        age INT(20));  

-- LOAD DATA LOCAL INFILE '/opt/cryptdb/data/medical.csv' INTO TABLE patients
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 LINES;

-- SELECT * FROM patients;