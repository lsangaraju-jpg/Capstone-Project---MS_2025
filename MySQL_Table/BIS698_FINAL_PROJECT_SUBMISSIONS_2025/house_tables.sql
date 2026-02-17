USE BIS698W1700_GRP6;
ALTER TABLE ServiceRegister
  MODIFY COLUMN Phone_number VARCHAR(20)
;
select * from usercredentials;
select * from Invoice_Details;
select * from ServiceRegister;

-- deletion --
DELETE FROM usercredentials WHERE ID in (13);
DELETE FROM Invoice_Details WHERE Invoice_number = 1;
DELETE FROM ServiceRegister WHERE Job_cardnumber = 1;

CREATE TABLE usercredentials (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    user_password VARCHAR(100) NOT NULL,
    Department VARCHAR(100) NOT NULL
);

CREATE TABLE Invoice_Details (
    First_name VARCHAR(20),
    Last_name VARCHAR(20),
    Gender VARCHAR(20),
    BirthDate DATE,
    StreetAddress VARCHAR(40),
    City VARCHAR(20),
    State VARCHAR(5),
    Phonenumber VARCHAR(15), 
    Invoice_number INT,
    Invoice_date DATE,
    House_Number VARCHAR(20),
    Unit_number VARCHAR(20)
);

create table ServiceRegister (

Job_cardnumber int,
First_name varchar(20),
Last_name varchar(20),
Street_address varchar(50),
City varchar(20),
State varchar(10),
Phone_number varchar(15),
Service_date date,
House_number varchar(20),
Unit_number varchar(20),
Purchase_date date,
Service_Type varchar(20)
);

-- user addition --
INSERT INTO usercredentials (Username, user_password, Department)
VALUES ('admin', 'admin123', 'admin');


