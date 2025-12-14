use finalproject;

-- Delete existing tables --
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS book_authors;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS book_categories;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS patrons;
DROP TABLE IF EXISTS checkouts;
DROP TABLE IF EXISTS reservations;

-- Create Tables ---
CREATE TABLE books (
	bookID INT PRIMARY KEY AUTO_INCREMENT,
    isbn VARCHAR(50),
    title VARCHAR(50),
    pubYear INT,
    totalCopies INT,
    availableCopies INT
);

CREATE TABLE authors (
	authorID INT PRIMARY KEY AUTO_INCREMENT,
    fName VARCHAR(50),
    lName VARCHAR(50),
    birthYear INT
);
	
CREATE TABLE book_authors (
	bookID INT,
    authorID INT
);

CREATE TABLE categories (
	categoryID INT PRIMARY KEY AUTO_INCREMENT,
    categoryName VARCHAR(50),
    descr VARCHAR(200)
);

CREATE TABLE book_categories (
	bookID INT,
    categoryID INT
);

CREATE TABLE staff (
	staffID INT PRIMARY KEY AUTO_INCREMENT,
    fName VARCHAR(50),
    lName VARCHAR(50),
    username VARCHAR(50),
    password VARCHAR(50),
    hireDate DATE
);

CREATE TABLE patrons (
	PatronID INT PRIMARY KEY AUTO_INCREMENT,
	FirstName VARCHAR(50),
	LastName VARCHAR(50),
	Email VARCHAR(50),
	Phone VARCHAR(15),
	JoinDate DATE,
	Status VARCHAR(10)
);

CREATE TABLE checkouts (
	CheckoutID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT,
	PatronID INT,
	StaffID INT,
	CheckoutDate DATE,
	DueDate DATE,
	ReturnDate DATE
);

CREATE TABLE reservations (
	ReservationID INT PRIMARY KEY AUTO_INCREMENT,
	BookID INT,
	PatronID INT,
	ReservationDate DATE,
	Status VARCHAR(10)
);