use finalproject;

-- Basic CRUD Operations --
INSERT INTO authors VALUES (16, "Jennifer", "Gonzalez", 1979);
INSERT INTO books (isbn, title, pubYear, totalCopies, availableCopies) VALUES (389021812, "The Lost Man", 2025, 21, 21);

SELECT bookID, title, pubYear 
FROM books
WHERE pubYear > 2010;

SELECT authorID, fName, lName, birthYear
FROM authors
WHERE birthYear >= 1970
ORDER BY birthYear asc;

SELECT bookID, title, pubYear 
FROM books
WHERE pubYear < 2010;


SELECT bookID, title, totalCopies 
FROM books
WHERE totalCopies < 20;

SELECT bookID, title, totalCopies, availableCopies
FROM books
WHERE availableCopies < 15;

UPDATE reservations
SET Status = "Active"
WHERE ReservationID = 12;

UPDATE books
SET availableCopies = 5
WHERE bookID = 12;

UPDATE authors
SET birthYear = 1971
WHERE authorID = 5;

UPDATE books
SET availableCopies = 5
WHERE bookID = 12;

UPDATE books
SET title = "Rise of the Lost Empire"
WHERE bookID = 17;

DELETE FROM books
WHERE bookID = 16;

DELETE FROM books
WHERE bookID = 14;

SET SQL_SAFE_UPDATES = 0;

DELETE FROM reservations
WHERE Status = "Cancelled";

DELETE FROM patrons
WHERE Status = "Inactive";

DELETE FROM authors
WHERE authorID = 12;

DELETE FROM books
WHERE bookID = 22;

SET SQL_SAFE_UPDATES = 1;