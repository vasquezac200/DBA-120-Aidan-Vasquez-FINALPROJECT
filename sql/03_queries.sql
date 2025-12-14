use finalproject;

-- Advanced Queries --
SELECT books.bookID, books.title, CONCAT(authors.fName, " ", authors.lName) AS 'author', books.pubyear
FROM book_authors
INNER JOIN books ON book_authors.bookID = books.bookID
INNER JOIN authors ON book_authors.authorID = authors.authorID;

SELECT books.bookID, books.title, books.pubyear, categories.categoryName, categories.descr AS 'desc'
FROM book_categories
INNER JOIN books ON book_categories.bookID = books.bookID
INNER JOIN categories ON book_categories.categoryID = categories.categoryID;

SELECT reservations.ReservationID, books.title AS 'Book Title', CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'Patron Name', reservations.ReservationDate, reservations.Status
FROM reservations
INNER JOIN books ON reservations.BookID = books.bookID
INNER JOIN patrons ON reservations.PatronID = patrons.PatronID;


SELECT AVG(totalCopies) AS "Average Total Copies"
FROM books;

SELECT MAX(totalCopies) AS "Most Copies" , MIN(totalCopies) AS "Least Copies"
FROM books;
-- Most Popular Books ---
SELECT books.title AS "Book", COUNT(checkouts.checkoutID) AS "Number of Checkouts" 
FROM checkouts 
INNER JOIN books ON checkouts.BookID = books.bookID
GROUP BY books.title
ORDER BY COUNT(checkouts.checkoutID) DESC;

-- Overdue Books --
SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
FROM checkouts
INNER JOIN books ON checkouts.BookID = books.bookID
INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID
WHERE checkouts.ReturnDate > checkouts.DueDate;

-- Monthly/yearly circulation statistics --
SELECT CONCAT(MONTH(c.CheckoutDate), "/", YEAR(c.CheckoutDate)) AS "Month", COUNT(*) AS "Total Checkouts", SUM(CASE WHEN c.ReturnDate IS NOT NULL THEN 1 ELSE 0 END) AS "Total Returns", SUM(CASE WHEN c.ReturnDate IS NULL THEN 1 ELSE 0 END) AS "Books Currently Checked Out"
FROM checkouts c
LEFT JOIN books b ON b.bookID = c.BookId 
GROUP BY CONCAT(MONTH(CheckoutDate), "/", YEAR(CheckoutDate))

