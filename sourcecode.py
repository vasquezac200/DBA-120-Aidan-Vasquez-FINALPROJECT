import mysql.connector
import time
import datetime
import getpass


def loginPrompt():
            username = input("Enter Username: ")
            password = getpass.getpass("Enter Password: ")

            staff_dbcursor = cnx.cursor()
            matchLogin = False

            staff_dbcursor.execute("SELECT staffID, username, password FROM staff WHERE username = %s AND password = %s", (username, password))

            row = staff_dbcursor.fetchone()

            if row:
                    matchLogin = 1
                    userID = row[0]
                    mainMenu(userID)
                    return True, userID
                    
            else:
                   print("Incorrect Username or Pa0ssword")
                   return False, None
 
def mainMenu(userID):
        staff_dbcursor = cnx.cursor()
        staff_dbcursor.execute("SELECT * FROM staff WHERE staffID = %s", (userID,))
        row = staff_dbcursor.fetchone()

        if row:
            print(f"Welcome {row[1]}!\n")
            print("""---Main Menu---\n""")
            print("""1. Book Management
2. Patron Management
3. Checkout Operations
4. Return Operations
5. Reservation Management
6. Reports and Analytics
0. Logout\n""")
            
            options = int(input("Select Options from 0-7: "))
            if options == 1: bookmgt(userID)
            elif options == 2: patronmgt(userID)
            elif options == 3: chkoutOper(userID)
            elif options == 4: returnOper(userID)
            elif options == 5: resmgt(userID)
            elif options == 6: reptAng(userID)
            elif options == 0: 
                   print("Now Logging Out...") 
                   time.sleep(1)
                   loginPrompt()
            else: 
                   print("Invalid Selection")
                   mainMenu(userID)

def bookmgt(userID):
        while True:
                staff_dbcursor = cnx.cursor()
                staff_dbcursor.execute("SELECT * FROM staff WHERE staffID = %s", (userID,))
                staff_row = staff_dbcursor.fetchone()


                def addbook():
                        isbn = input("Enter ISBN: ")
                        title = input("Enter Title of Book: ")
                        pubYear = input("Enter Year of Book: ")
                        totalCopies = input("Enter the Total Amount of Copies of the Book: ")
                        availableCopies = input("Enter the Total Available Copies of the Book: ")

                        query = """
                                INSERT INTO books (isbn, title, pubYear, totalCopies, availableCopies)
                                VALUES (%s, %s, %s, %s, %s)
                        """

                        with cnx.cursor() as bookADD_dbcursor:
                                bookADD_dbcursor.execute(query, (isbn, title, pubYear, totalCopies, availableCopies))
                        
                        cnx.commit()
                        print("Book added successfully.")



                def editbook():
                        showAllBooks()
                        editBookOption = input("Which book do you want to edit? (Enter by ID): ")
                        editTypeOption = input("What needs to be edited? (ISBN, Title, Year, TotalCopies, or AvailableCopies): ")
                        if editTypeOption == "ISBN" or editTypeOption == "Title" or editTypeOption == "Year" or editTypeOption == "TotalCopies" or editTypeOption == "AvailableCopies":
                                if editTypeOption == "ISBN": editTypeOption = "isbn"
                                elif editTypeOption == "Title": editTypeOption = "title"
                                elif editTypeOption == "Year": editTypeOption = "pubYear"
                                elif editTypeOption == "TotalCopies": editTypeOption = "totalCopies"
                                elif editTypeOption == "AvailableCopies": editTypeOption = "availableCopies"
                                       
                                editBook = input("Enter New Data: ")
                                bookEDIT_dbcursor = cnx.cursor()
                                query = f"UPDATE books SET {editTypeOption} = %s WHERE bookID = %s"
                                bookEDIT_dbcursor.execute(query, (editBook, editBookOption, ))
                                cnx.commit()
                                print(f"Book with ID {editBookOption} changed successfully.")
                        else: 
                               print("Invalid Option")
                        

                def deletebook():
                        showAllBooks()
                        deleteOption = input("Which book do you want to delete? (Enter by ID): ")
                        bookDEL_dbcursor = cnx.cursor()
                        bookDEL_dbcursor.execute("DELETE FROM books WHERE bookID = %s", (deleteOption, ))
                        cnx.commit()
                        print(f"Book with ID {deleteOption} deleted successfully.")




                def searchbook():
                        addCommandOptions = input("Search by 'Title' or 'Year': ")
                        if addCommandOptions == "Title": 
                                title = input("Enter Title of Book: ")
                                formattedTitle = "%" + title + "%"
                                bookSEARCH_dbcursor = cnx.cursor()
                                bookSEARCH_dbcursor.execute("SELECT * FROM books WHERE title LIKE  %s", (formattedTitle, ))
                                book_rows = bookSEARCH_dbcursor.fetchall()
                                
                                print(f'{"ID:":<5} {"ISBN:":<15} {"Title:":<40} {"Year:":<6} {"Total Copies:":<15} {"Available Copies:":<15}')
                                for book_row in book_rows:
                                        print(f'{book_row[0]:<5} {book_row[1]:<15} {book_row[2]:<40} {book_row[3]:<6} {book_row[4]:<15} {book_row[5]:<15}')
                        elif addCommandOptions == "Year":
                                pubYear = input("Enter Year of Book: ")
                                bookSEARCH_dbcursor = cnx.cursor()
                                bookSEARCH_dbcursor.execute("SELECT * FROM books WHERE pubYear = %s", (pubYear, ))
                                book_rows = bookSEARCH_dbcursor.fetchall()
                                
                                print(f'{"ID:":<5} {"ISBN:":<15} {"Title:":<40} {"Year:":<6} {"Total Copies:":<15} {"Available Copies:":<15}')
                                for book_row in book_rows:
                                        print(f'{book_row[0]:<5} {book_row[1]:<15} {book_row[2]:<40} {book_row[3]:<6} {book_row[4]:<15} {book_row[5]:<15}')
                                
                        else:
                                print("Invalid Input!")

                def viewAllBooks():
                        showAllBooks()


                        

                print("""== Book Management ==\n
1. Add Book
2. Edit Book
3. Delete Book
4. Search Books
5. View All Books
0. Back to Main Menu""")

                commandOptions = int(input("What do you want to do?: "))
                if commandOptions == 1: addbook()
                if commandOptions == 2: editbook()
                if commandOptions == 3: deletebook()
                if commandOptions == 4: searchbook()
                if commandOptions == 5: viewAllBooks()
                elif commandOptions == 0:
                        print("Now Exiting...") 
                        time.sleep(1)
                        mainMenu(userID)
        

def patronmgt(userID):
       while True:
                staff_dbcursor = cnx.cursor()
                staff_dbcursor.execute("SELECT * FROM staff WHERE staffID = %s", (userID,))
                staff_row = staff_dbcursor.fetchone()


                def addpatron():
                        fName = input("Enter First Name: ")
                        lName = input("Enter Last Name: ")
                        email = input("Enter Email: ")
                        phone = input("Enter Phone: ")
                        joinDate = input("Enter Join Date (Using YYYY-MM-DD): ")

                        query = """
                                INSERT INTO patrons (FirstName, LastName, Email, Phone, JoinDate, Status)
                                VALUES (%s, %s, %s, %s, %s, "Active")
                        """

                        with cnx.cursor() as patronADD_dbcursor:
                                patronADD_dbcursor.execute(query, (fName, lName, email, phone, joinDate))
                        
                        cnx.commit()
                        print("Patron added successfully.")



                def editpatron():
                        showAllPatrons()
                        editPatronOption = input("Which patron do you want to edit? (Enter by ID): ")
                        editTypeOption = input("What needs to be edited? (FirstName, LastName, Email, Phone, JoinDate, or Status): ")
                        if editTypeOption == "FirstName" or editTypeOption == "LastName" or editTypeOption == "Email" or editTypeOption == "Phone" or editTypeOption == "JoinDate" or editTypeOption == "Status":
                                       
                                editPatron = input("Enter New Data: ")
                                patronEDIT_dbcursor = cnx.cursor()
                                query = f"UPDATE patrons SET {editTypeOption} = %s WHERE PatronID = %s"
                                patronEDIT_dbcursor.execute(query, (editPatron, editPatronOption, ))
                                cnx.commit()
                                print(f"Patron with ID {editPatronOption} changed successfully.")
                        else: 
                               print("Invalid Option")
                        

                def deletepatron():
                        showAllPatrons()
                        deleteOption = input("Which book do you want to delete? (Enter by ID): ")
                        patronDEL_dbcursor = cnx.cursor()
                        patronDEL_dbcursor.execute("DELETE FROM patrons WHERE PatronID = %s", (deleteOption, ))
                        cnx.commit()
                        print(f"Patron with ID {deleteOption} deleted successfully.")




                def searchpatron():
                        addCommandOptions = input("Search by 'Name', 'Email', 'Phone', or 'Join Date': ")
                        if addCommandOptions == "Name": 
                                name = input("Enter Name of Patron: ")
                                formattedName = "%" + name + "%"
                                patronSEARCH_dbcursor = cnx.cursor()
                                patronSEARCH_dbcursor.execute("SELECT * FROM patrons WHERE FirstName LIKE %s OR LastName LIKE  %s", (formattedName, formattedName, ))
                                patron_row = patronSEARCH_dbcursor.fetchall()
                                
                                print(f'{"PatronID:":<10} {"First Name:":<20} {"Last Name:":<20} {"Email:":<35} {"Phone:":<15}')
                                for patrons_row in patron_row:
                                        print(f'{patrons_row[0]:<10} {patrons_row[1]:<20} {patrons_row[2]:<20} {patrons_row[3]:<35} {patrons_row[4]:<15}')

                        elif addCommandOptions == "Email":
                                email = input("Enter Email of Patron: ")
                                formattedEmail = "%" + email + "%"
                                patronSEARCH_dbcursor = cnx.cursor()
                                patronSEARCH_dbcursor.execute("SELECT * FROM patrons WHERE Email LIKE %s", (formattedEmail, ))
                                patron_row = patronSEARCH_dbcursor.fetchall()
                                
                                print(f'{"PatronID:":<10} {"First Name:":<20} {"Last Name:":<20} {"Email:":<35} {"Phone:":<15}')
                                for patrons_row in patron_row:
                                        print(f'{patrons_row[0]:<10} {patrons_row[1]:<20} {patrons_row[2]:<20} {patrons_row[3]:<35} {patrons_row[4]:<15}')

                        elif addCommandOptions == "Phone":
                                phone = input("Enter Phone of Patron: ")
                                formattedPhone = "%" + phone + "%"
                                patronSEARCH_dbcursor = cnx.cursor()
                                patronSEARCH_dbcursor.execute("SELECT * FROM patrons WHERE Phone LIKE %s", (formattedPhone, ))
                                patron_row = patronSEARCH_dbcursor.fetchall()

                                print(f'{"PatronID:":<10} {"First Name:":<20} {"Last Name:":<20} {"Email:":<35} {"Phone:":<15}')
                                for patrons_row in patron_row:
                                        print(f'{patrons_row[0]:<10} {patrons_row[1]:<20} {patrons_row[2]:<20} {patrons_row[3]:<35} {patrons_row[4]:<15}')

                        elif addCommandOptions == "Join Date":
                                jd = input("Enter Join Date of Patron (Using YYYY-MM-DD): ")
                                patronSEARCH_dbcursor = cnx.cursor()
                                patronSEARCH_dbcursor.execute("SELECT * FROM patrons WHERE JoinDate = %s", (jd, ))
                                patron_row = patronSEARCH_dbcursor.fetchall()
                                
                                print(f'{"PatronID:":<10} {"First Name:":<20} {"Last Name:":<20} {"Email:":<35} {"Phone:":<15}')
                                for patrons_row in patron_row:
                                        print(f'{patrons_row[0]:<10} {patrons_row[1]:<20} {patrons_row[2]:<20} {patrons_row[3]:<35} {patrons_row[4]:<15}')
                        else:
                                print("Invalid Input!")

                def viewAllPatrons():
                       showAllPatrons()
   
                        

                print("""== Patron Management ==\n
1. Add Patron
2. Edit Patron
3. Delete Patron
4. Search Patron
5. View All Patrons
0. Back to Main Menu""")

                commandOptions = int(input("What do you want to do?: "))
                if commandOptions == 1: addpatron()
                if commandOptions == 2: editpatron()
                if commandOptions == 3: deletepatron()
                if commandOptions == 4: searchpatron()
                if commandOptions == 5: viewAllPatrons()
                elif commandOptions == 0:
                        print("Now Exiting...") 
                        time.sleep(1)
                        mainMenu(userID)


def chkoutOper(userID):
        while True:
                checkout_dbcursor = cnx.cursor()
                checkout_dbcursor.execute("SELECT * FROM checkouts WHERE StaffID = %s", (userID,))
                rows = checkout_dbcursor.fetchall()

                

                

                def addChkout():
                       showAllBooks()
                       book = input("Enter Book ID: ")
                       showAllPatrons()
                       patron = input("Enter Patron ID: ")
                       dueDate = input("Enter Due Date (Using YYYY-MM-DD): ")
                       remainCopies = 0


                       today = datetime.date.today()
                       today_str = today.strftime("%Y-%m-%d")

                       if not dueDate:
                        print("Due Date is required.")
                        return

                       
                       query = """
                                INSERT INTO checkouts (BookID, PatronID, StaffID, CheckoutDate, DueDate)
                                VALUES (%s, %s, %s, %s, %s)
                        """
                       
                       with cnx.cursor() as checkoutADD_dbcursor:
                                checkoutADD_dbcursor.execute(query, (book, patron, userID, today_str, dueDate))
                                checkoutADD_dbcursor.close()
                                
                       cnx.commit()

                       books_dbcursor = cnx.cursor()
                       books_dbcursor.execute("SELECT bookID, availableCopies FROM books")
                       books_rows = books_dbcursor.fetchall()
                       for book_row in books_rows:
                                if book_row[0] == int(book):
                                        remainCopies = book_row[1] - 1
                                        updateBooks_dbcursor = cnx.cursor()
                                        updateBooks_dbcursor.execute("UPDATE books SET availableCopies = %s WHERE bookID = %s", (remainCopies, book))
                                        updateBooks_dbcursor.close()
                                        cnx.commit()
                       
                       print("Checkout added successfully.")

                def editChkout():
                        showAllCheckouts()
                        editChkOption = input("Which book do you want to edit? (Enter by ID): ")
                        editTypeOption = input("What needs to be edited? (BookID, PatronID, StaffID, CheckoutDate, DueDate, ReturnDate): ")
                        if editTypeOption == "BookID" or editTypeOption == "PatronID" or editTypeOption == "StaffID" or editTypeOption == "CheckoutDate" or editTypeOption == "DueDate" or editTypeOption == "ReturnDate":       
                                editChk = input("Enter New Data: ")
                                
                                if not editChk and editTypeOption == "ReturnDate":
                                       editChk = None

                                chkEDIT_dbcursor = cnx.cursor()
                                query = f"UPDATE checkouts SET {editTypeOption} = %s WHERE CheckoutID = %s"
                                chkEDIT_dbcursor.execute(query, (editChk, editChkOption, ))
                                cnx.commit()
                                print(f"Checkout with ID {editChkOption} changed successfully.")
                        else: 
                               print("Invalid Option")

                def deleteChkout():
                        showAllCheckouts()
                        deleteOption = input("Which checkout do you want to delete? (Enter by ID): ")
                        chkoutDEL_dbcursor = cnx.cursor()

                        for book_row in books_rows:
                                book = book_row[2]
                                if book_row[0] == int(book):
                                        remainCopies = book_row[1] + 1
                                        updateBooks_dbcursor = cnx.cursor()
                                        updateBooks_dbcursor.execute("UPDATE books SET availableCopies = %s WHERE bookID = %s", (remainCopies, book))
                                        updateBooks_dbcursor.close()
                                        cnx.commit()

                        chkoutDEL_dbcursor.execute("DELETE FROM checkouts WHERE CheckoutID = %s", (deleteOption, ))
                        cnx.commit()

                        books_dbcursor = cnx.cursor()
                        books_dbcursor.execute("SELECT books.bookID, books.availableCopies, checkouts.BookID FROM books INNER JOIN checkouts ON books.bookID = checkouts.BookID WHERE checkouts.CheckoutID = %s", (deleteOption, ))
                        books_rows = books_dbcursor.fetchall()

                        print(f"Checkout with ID {deleteOption} deleted successfully.")

                def searchChkout():
                        addCommandOptions = input("Search by 'Book', 'Patron', 'CheckoutDate', DueDate or 'ReturnDate': ")
                        if addCommandOptions == "Book": 
                                title = input("Enter Title of Book: ")
                                formattedTitle = "%" + title + "%"
                                checkoutSEARCH_dbcursor = cnx.cursor()
                                checkoutSEARCH_dbcursor.execute("""SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
                                     FROM checkouts
                                     INNER JOIN books ON checkouts.BookID = books.bookID
                                     INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID
                                     WHERE books.title LIKE  %s""", (formattedTitle, ))
                                checkout_rows = checkoutSEARCH_dbcursor.fetchall()
                                print(f'{"CheckoutID:":<12} {"BookID:":<10} {"BookName:":<40} {"PatronID:":<10} {"PatronName:":<20} {"StaffID:":<10} {"Checkout Date:":<15} {"Due Date:":<15}  {"Return Date:":<15}')
                                for row in checkout_rows:
                                        chk_date = row[6].strftime('%Y-%m-%d') if hasattr(row[6], 'strftime') else str(row[6])
                                        due_date = row[7].strftime('%Y-%m-%d') if hasattr(row[7], 'strftime') else str(row[7])
                                        return_date = row[8].strftime('%Y-%m-%d') if hasattr(row[8], 'strftime') else str(row[8])
                                        print(f'{row[0]:<12} {row[1]:<10} {row[2]:<40} {row[3]:<10} {row[4]:<20} {row[5]:<10} {chk_date:<15} {due_date:<15} {return_date:<15}')

                        elif addCommandOptions == "Patron":
                                title = input("Enter Name of Patron: ")
                                formattedTitle = "%" + title + "%"
                                checkoutSEARCH_dbcursor = cnx.cursor()
                                checkoutSEARCH_dbcursor.execute("""SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
                                     FROM checkouts
                                     INNER JOIN books ON checkouts.BookID = books.bookID
                                     INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID
                                     WHERE patrons.FirstName LIKE %s OR patrons.LastName LIKE %s""", (formattedTitle, formattedTitle, ))
                                checkout_rows = checkoutSEARCH_dbcursor.fetchall()
                                print(f'{"CheckoutID:":<12} {"BookID:":<10} {"BookName:":<40} {"PatronID:":<10} {"PatronName:":<20} {"StaffID:":<10} {"Checkout Date:":<15} {"Due Date:":<15}  {"Return Date:":<15}')
                                for row in checkout_rows:
                                        chk_date = row[6].strftime('%Y-%m-%d') if hasattr(row[6], 'strftime') else str(row[6])
                                        due_date = row[7].strftime('%Y-%m-%d') if hasattr(row[7], 'strftime') else str(row[7])
                                        return_date = row[8].strftime('%Y-%m-%d') if hasattr(row[8], 'strftime') else str(row[8])
                                        print(f'{row[0]:<12} {row[1]:<10} {row[2]:<40} {row[3]:<10} {row[4]:<20} {row[5]:<10} {chk_date:<15} {due_date:<15} {return_date:<15}')

                        elif addCommandOptions == "CheckoutDate":
                                date = input("Enter Checkout Date (Using YYYY-MM-DD): ")
                                checkoutSEARCH_dbcursor = cnx.cursor()
                                checkoutSEARCH_dbcursor.execute("""SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
                                     FROM checkouts
                                     INNER JOIN books ON checkouts.BookID = books.bookID
                                     INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID
                                     WHERE DATE(checkouts.CheckoutDate) = %s""", (date, ))
                                checkout_rows = checkoutSEARCH_dbcursor.fetchall()
                                print(f'{"CheckoutID:":<12} {"BookID:":<10} {"BookName:":<40} {"PatronID:":<10} {"PatronName:":<20} {"StaffID:":<10} {"Checkout Date:":<15} {"Due Date:":<15}  {"Return Date:":<15}')
                                for row in checkout_rows:
                                        chk_date = row[6].strftime('%Y-%m-%d') if hasattr(row[6], 'strftime') else str(row[6])
                                        due_date = row[7].strftime('%Y-%m-%d') if hasattr(row[7], 'strftime') else str(row[7])
                                        return_date = row[8].strftime('%Y-%m-%d') if hasattr(row[8], 'strftime') else str(row[8])
                                        print(f'{row[0]:<12} {row[1]:<10} {row[2]:<40} {row[3]:<10} {row[4]:<20} {row[5]:<10} {chk_date:<15} {due_date:<15} {return_date:<15}')       

                        elif addCommandOptions == "DueDate":
                                date = input("Enter Due Date (Using YYYY-MM-DD): ")
                                checkoutSEARCH_dbcursor = cnx.cursor()
                                checkoutSEARCH_dbcursor.execute("""SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
                                     FROM checkouts
                                     INNER JOIN books ON checkouts.BookID = books.bookID
                                     INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID
                                     WHERE DATE(checkouts.DueDate) = %s""", (date, ))
                                checkout_rows = checkoutSEARCH_dbcursor.fetchall()
                                print(f'{"CheckoutID:":<12} {"BookID:":<10} {"BookName:":<40} {"PatronID:":<10} {"PatronName:":<20} {"StaffID:":<10} {"Checkout Date:":<15} {"Due Date:":<15}  {"Return Date:":<15}')
                                for row in checkout_rows:
                                        chk_date = row[6].strftime('%Y-%m-%d') if hasattr(row[6], 'strftime') else str(row[6])
                                        due_date = row[7].strftime('%Y-%m-%d') if hasattr(row[7], 'strftime') else str(row[7])
                                        return_date = row[8].strftime('%Y-%m-%d') if hasattr(row[8], 'strftime') else str(row[8])
                                        print(f'{row[0]:<12} {row[1]:<10} {row[2]:<40} {row[3]:<10} {row[4]:<20} {row[5]:<10} {chk_date:<15} {due_date:<15} {return_date:<15}')       

                        elif addCommandOptions == "ReturnDate":
                                date = input("Enter Return Date (Using YYYY-MM-DD): ")
                                checkoutSEARCH_dbcursor = cnx.cursor()
                                checkoutSEARCH_dbcursor.execute("""SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
                                     FROM checkouts
                                     INNER JOIN books ON checkouts.BookID = books.bookID
                                     INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID
                                     WHERE DATE(checkouts.ReturnDate) = %s""", (date, ))
                                checkout_rows = checkoutSEARCH_dbcursor.fetchall()
                                print(f'{"CheckoutID:":<12} {"BookID:":<10} {"BookName:":<40} {"PatronID:":<10} {"PatronName:":<20} {"StaffID:":<10} {"Checkout Date:":<15} {"Due Date:":<15}  {"Return Date:":<15}')
                                for row in checkout_rows:
                                        chk_date = row[6].strftime('%Y-%m-%d') if hasattr(row[6], 'strftime') else str(row[6])
                                        due_date = row[7].strftime('%Y-%m-%d') if hasattr(row[7], 'strftime') else str(row[7])
                                        return_date = row[8].strftime('%Y-%m-%d') if hasattr(row[8], 'strftime') else str(row[8])
                                        print(f'{row[0]:<12} {row[1]:<10} {row[2]:<40} {row[3]:<10} {row[4]:<20} {row[5]:<10} {chk_date:<15} {due_date:<15} {return_date:<15}')       
                        else:
                                print("Invalid Input!")

                def viewAllChkout():
                       showAllCheckouts()
                        
                        
                        
                

                print("""== Checkout Operations ==
1. Add Checkout
2. Edit Checkout
3. Delete Checkout
4. Search Checkout
5. View All Checkouts
0. Back to Main Menu""")

                commandOptions = int(input("What do you want to do?: "))
                if commandOptions == 1: addChkout()
                elif commandOptions == 2: editChkout()
                elif commandOptions == 3: deleteChkout()
                elif commandOptions == 4: searchChkout()
                elif commandOptions == 5: viewAllChkout()
                elif commandOptions == 0:
                        print("Now Exiting...")
                        time.sleep(1)
                        mainMenu(userID)

def returnOper(userID):
       while True:
                checkout_dbcursor = cnx.cursor()
                checkout_dbcursor.execute("SELECT * FROM checkouts WHERE StaffID = %s", (userID,))
                rows = checkout_dbcursor.fetchall()
                checkoutsALL_dbcursor = cnx.cursor()
                checkoutsALL_dbcursor.execute("""SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
                                                FROM checkouts
                                                INNER JOIN books ON checkouts.BookID = books.bookID
                                                INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID
                                                WHERE checkouts.ReturnDate IS NULL""")
                print(f'{"CheckoutID:":<12} {"BookID:":<10} {"BookName:":<40} {"PatronID:":<10} {"PatronName:":<20} {"StaffID:":<10} {"Checkout Date:":<15} {"Due Date:":<15}  {"Return Date:":<15}')
                for row in checkoutsALL_dbcursor:
                                chk_date = row[6].strftime('%Y-%m-%d') if hasattr(row[6], 'strftime') else str(row[6])
                                due_date = row[7].strftime('%Y-%m-%d') if hasattr(row[7], 'strftime') else str(row[7])
                                return_date = row[8].strftime('%Y-%m-%d') if hasattr(row[8], 'strftime') else str(row[8])
                                print(f'{row[0]:<12} {row[1]:<10} {row[2]:<40} {row[3]:<10} {row[4]:<20} {row[5]:<10} {chk_date:<15} {due_date:<15} {return_date:<15}')
                editChkOption = input("Enter CheckoutID that is being returned: ")
                editChk = input("Enter Return Date or Leave Blank for Today's Date (Using YYYY-MM-DD): ")

                if not editChk:
                       today = datetime.date.today()
                       editChk = today.strftime("%Y-%m-%d")

                chkEDIT_dbcursor = cnx.cursor()
                query = f"UPDATE checkouts SET ReturnDate = %s WHERE CheckoutID = %s"
                chkEDIT_dbcursor.execute(query, (editChk, editChkOption, ))
                cnx.commit()

                books_dbcursor = cnx.cursor()
                books_dbcursor.execute("SELECT books.bookID, books.availableCopies FROM books INNER JOIN checkouts ON books.bookID = checkouts.BookID WHERE checkouts.CheckoutID = %s", (editChkOption, ))
                books_rows = books_dbcursor.fetchall()

                for book_row in books_rows:
                                book = book_row[0]
                                if book_row[0] == int(book):
                                        remainCopies = book_row[1] + 1
                                        updateBooks_dbcursor = cnx.cursor()
                                        updateBooks_dbcursor.execute("UPDATE books SET availableCopies = %s WHERE bookID = %s", (remainCopies, book))
                                        updateBooks_dbcursor.close()
                                        cnx.commit()

                print(f"Checkout with ID {editChkOption} returned successfully.")
                mainMenu(userID)
                

def resmgt(userID):
    while True:
        staff_dbcursor = cnx.cursor()
        staff_dbcursor.execute("SELECT * FROM staff WHERE staffID = %s", (userID,))
        staff_row = staff_dbcursor.fetchone()

        def addres():
            bookID = input("Enter Book ID: ")
            patronID = input("Enter Patron ID: ")
            todayDate = input("Enter Today's Date (Using YYYY-MM-DD): ")

            query = """
                INSERT INTO reservations (BookID, PatronID, ReservationDate, Status)
                VALUES (%s, %s, %s, "Active")
            """

            with cnx.cursor() as resADD_dbcursor:
                resADD_dbcursor.execute(query, (bookID, patronID, todayDate, ))

            cnx.commit()
            print("Reservation added successfully.")

        def editres():
            resALL_dbcursor = cnx.cursor()
            resALL_dbcursor.execute("SELECT * FROM reservations")
            print(f'{"ReservationID:":<20} {"Book:":<40} {"Patron:":<25} {"Reservation Date:":>20} {"Status:":^25}')
            for res_row in resALL_dbcursor.fetchall():
                        res_date = res_row[3].strftime('%Y-%m-%d') if hasattr(res_row[3], 'strftime') else str(res_row[3])
                        print(f'{res_row[0]:<20} {res_row[1]:<40} {res_row[2]:<25} {res_date:>20} {res_row[4]:^25}')

            editResOption = input("Which reservations do you want to edit? (Enter by Reservation ID): ")
            editTypeOption = input("What needs to be edited? (BookID, PatronID, ReservationDate, Status): ")

            if editTypeOption in ["BookID", "PatronID", "ReservationDate", "Status"]:
                new_value = input("Enter New Data: ")
                resEDIT_dbcursor = cnx.cursor()
                query = f"UPDATE reservations SET {editTypeOption} = %s WHERE ReservationID = %s"
                resEDIT_dbcursor.execute(query, (new_value, editResOption))
                cnx.commit()
                print(f"Reservation with ID {editResOption} changed successfully.")
            else:
                print("Invalid Option")

        def deleteres():
            resALL_dbcursor = cnx.cursor()
            resALL_dbcursor.execute("""SELECT reservations.ReservationID, books.title AS 'Book Title', CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'Patron Name', reservations.ReservationDate, reservations.Status 
                                    FROM reservations
                                    INNER JOIN books ON reservations.BookID = books.bookID
                                    INNER JOIN patrons ON reservations.PatronID = patrons.PatronID;""")
            print(f'{"ReservationID:":<20} {"Book:":<40} {"Patron:":<25} {"Reservation Date:":>20} {"Status:":^25}')
            for res_row in resALL_dbcursor.fetchall():
                        res_date = res_row[3].strftime('%Y-%m-%d') if hasattr(res_row[3], 'strftime') else str(res_row[3])
                        print(f'{res_row[0]:<20} {res_row[1]:<40} {res_row[2]:<25} {res_date:>20} {res_row[4]:^25}')

            deleteOption = input("Which reservations do you want to delete? (Enter by ID): ")
            resDEL_dbcursor = cnx.cursor()
            resDEL_dbcursor.execute("DELETE FROM reservations WHERE ReservationID = %s", (deleteOption,))
            cnx.commit()
            print(f"Reservations with ID {deleteOption} deleted successfully.")

        def searchres():
            addCommandOptions = input("Search by 'Book', 'Patron', or 'ReservationDate'?: ")

            if addCommandOptions == "Book":
                name = input("Enter Book Name: ")
                formattedName = "%" + name + "%"
                resSEARCH_dbcursor = cnx.cursor()
                resSEARCH_dbcursor.execute("""SELECT reservations.ReservationID, books.title AS 'Book Title', CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'Patron Name', reservations.ReservationDate, reservations.Status 
                                    FROM reservations
                                    INNER JOIN books ON reservations.BookID = books.bookID
                                    INNER JOIN patrons ON reservations.PatronID = patrons.PatronID 
                                    WHERE books.title LIKE %s""",
                                        (formattedName, ))
                print(f'{"ReservationID:":<20} {"Book:":<40} {"Patron:":<25} {"Reservation Date:":>20} {"Status:":^25}')
                for res_row in resSEARCH_dbcursor.fetchall():
                        res_date = res_row[3].strftime('%Y-%m-%d') if hasattr(res_row[3], 'strftime') else str(res_row[3])
                        print(f'{res_row[0]:<20} {res_row[1]:<40} {res_row[2]:<25} {res_date:>20} {res_row[4]:^25}')

            elif addCommandOptions == "Patron":
                name = input("Enter Patron Name: ")
                formattedName = "%" + name + "%"
                resSEARCH_dbcursor = cnx.cursor()
                resSEARCH_dbcursor.execute("""SELECT reservations.ReservationID, books.title AS 'Book Title', CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'Patron Name', reservations.ReservationDate, reservations.Status 
                                    FROM reservations
                                    INNER JOIN books ON reservations.BookID = books.bookID
                                    INNER JOIN patrons ON reservations.PatronID = patrons.PatronID 
                                    WHERE patrons.FirstName LIKE %s OR patrons.LastName LIKE %s""",
                                        (formattedName, formattedName ))
                print(f'{"ReservationID:":<20} {"Book:":<40} {"Patron:":<25} {"Reservation Date:":>20} {"Status:":^25}')
                for res_row in resSEARCH_dbcursor.fetchall():
                        res_date = res_row[3].strftime('%Y-%m-%d') if hasattr(res_row[3], 'strftime') else str(res_row[3])
                        print(f'{res_row[0]:<20} {res_row[1]:<40} {res_row[2]:<25} {res_date:>20} {res_row[4]:^25}')

            elif addCommandOptions == "ReservationDate":
                rd = input("Enter Reservation Date (Using YYYY-MM-DD): ")
                resSEARCH_dbcursor = cnx.cursor()
                resSEARCH_dbcursor.execute("""SELECT reservations.ReservationID, books.title AS 'Book Title', CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'Patron Name', reservations.ReservationDate, reservations.Status 
                                    FROM reservations
                                    INNER JOIN books ON reservations.BookID = books.bookID
                                    INNER JOIN patrons ON reservations.PatronID = patrons.PatronID 
                                    WHERE reservations.ReservationDate = %s""",
                                        (rd, ))
                print(f'{"ReservationID:":<20} {"Book:":<40} {"Patron:":<25} {"Reservation Date:":>20} {"Status:":^25}')
                for res_row in resSEARCH_dbcursor.fetchall():
                        res_date = res_row[3].strftime('%Y-%m-%d') if hasattr(res_row[3], 'strftime') else str(res_row[3])
                        print(f'{res_row[0]:<20} {res_row[1]:<40} {res_row[2]:<25} {res_date:>20} {res_row[4]:^25}')

            else:
                print("Invalid Input!")

        def viewAllRes():
            resALL_dbcursor = cnx.cursor()
            resALL_dbcursor.execute("""SELECT reservations.ReservationID, books.title AS 'Book Title', CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'Patron Name', reservations.ReservationDate, reservations.Status 
                                    FROM reservations
                                    INNER JOIN books ON reservations.BookID = books.bookID
                                    INNER JOIN patrons ON reservations.PatronID = patrons.PatronID;""")
            print(f'{"ReservationID:":<20} {"Book:":<40} {"Patron:":<25} {"Reservation Date:":>20} {"Status:":^25}')
            for res_row in resALL_dbcursor:
                res_date = res_row[3].strftime('%Y-%m-%d') if hasattr(res_row[3], 'strftime') else str(res_row[3])
                print(f'{res_row[0]:<20} {res_row[1]:<40} {res_row[2]:<25} {res_date:>20} {res_row[4]:^25}')

        print("""== Reservation Management ==

1. Add Reservation
2. Edit Reservation
3. Delete Reservation
4. Search Reservation
5. View All Reservations
0. Back to Main Menu""")

        commandOptions = int(input("What do you want to do?: "))
        if commandOptions == 1: addres()
        elif commandOptions == 2: editres()
        elif commandOptions == 3: deleteres()
        elif commandOptions == 4: searchres()
        elif commandOptions == 5: viewAllRes()
        elif commandOptions == 0:
            print("Now Exiting...")
            time.sleep(1)
            mainMenu(userID)
                
def reptAng(userID):

        def popularBooks():
               popularBooks_dbcursor = cnx.cursor()
               popularBooks_dbcursor.execute("""SELECT books.title AS "Book", COUNT(checkouts.checkoutID) AS "Number of Checkouts" 
                                                FROM checkouts 
                                                INNER JOIN books ON checkouts.BookID = books.bookID
                                                GROUP BY books.title
                                                ORDER BY COUNT(checkouts.checkoutID) DESC;""")
               print("== Popular Books ==")
               print(f'{"Book:":<40} {"Number of Checkouts:":<10}')
               for row in popularBooks_dbcursor:
                      print(f'{row[0]:<40} {row[1]:<10}')
               reptAng(userID)
        def overDueBooks():
                today = datetime.date.today()
                overDueBooks_dbcursor = cnx.cursor()
                overDueBooks_dbcursor.execute("""SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
                                                FROM checkouts
                                                INNER JOIN books ON checkouts.BookID = books.bookID
                                                INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID
                                                WHERE (checkouts.ReturnDate IS NULL AND %s > checkouts.DueDate) OR (checkouts.ReturnDate IS NOT NULL AND checkouts.ReturnDate > checkouts.DueDate);""", (today,))
                print("== Overdue Books ==")
                print(f'{"CheckoutID:":<12} {"BookID:":<10} {"BookName:":<40} {"PatronID:":<10} {"PatronName:":<20} {"StaffID:":<10} {"Checkout Date:":<15} {"Due Date:":<15}  {"Return Date:":<15}')
                for row in overDueBooks_dbcursor:
                                chk_date = row[6].strftime('%Y-%m-%d') if hasattr(row[6], 'strftime') else str(row[6])
                                due_date = row[7].strftime('%Y-%m-%d') if hasattr(row[7], 'strftime') else str(row[7])
                                return_date = row[8].strftime('%Y-%m-%d') if hasattr(row[8], 'strftime') else str(row[8])
                                print(f'{row[0]:<12} {row[1]:<10} {row[2]:<40} {row[3]:<10} {row[4]:<20} {row[5]:<10} {chk_date:<15} {due_date:<15} {return_date:<15}')
                reptAng(userID)

        def patronActSum():
                print("""== Patron Activity Summary ==
1. Select patron by ID
2. Search patron by last name
3. Return to main menu""")
                commandOptions = int(input("What do you want to select the patron with?: "))
                if commandOptions == 1:
                        id = input("Enter ID of Patron: ")
                        patronSEARCH_dbcursor = cnx.cursor()
                        patronSEARCH_dbcursor.execute("SELECT * FROM patrons WHERE PatronID = %s", (id, ))
                        patron_row = patronSEARCH_dbcursor.fetchall()
                        
                        print(f'{"PatronID:":<10} {"First Name:":<20} {"Last Name:":<20} {"Email:":<35} {"Phone:":<15}')
                        for patrons_row in patron_row:
                                print(f'{patrons_row[0]:<10} {patrons_row[1]:<20} {patrons_row[2]:<20} {patrons_row[3]:<35} {patrons_row[4]:<15}')
                        print("\n\n== Books Checked Out by Patron ==")
                        patronCHKOUT_dbcursor = cnx.cursor()
                        patronCHKOUT_dbcursor.execute("""SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
                                                        FROM checkouts
                                                        INNER JOIN books ON checkouts.BookID = books.bookID
                                                        INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID
                                                        WHERE patrons.PatronID = %s;""", (id, ))
                        print(f'{"CheckoutID:":<12} {"BookID:":<10} {"BookName:":<40} {"PatronID:":<10} {"PatronName:":<20} {"Checkout Date:":<15} {"Due Date:":<15}  {"Return Date:":<15} {"Status:":<10}')
                        for row in patronCHKOUT_dbcursor:
                                chk_date = row[6].strftime('%Y-%m-%d') if hasattr(row[6], 'strftime') else str(row[6])
                                due_date = row[7].strftime('%Y-%m-%d') if hasattr(row[7], 'strftime') else str(row[7])
                                return_date = row[8].strftime('%Y-%m-%d') if hasattr(row[8], 'strftime') else str(row[8])
                                today = datetime.date.today()
                                if row[8] is None and today > row[7]:
                                        status = "Overdue"
                                elif row[8] is None:
                                        status = "Checked Out"
                                elif row[8] > row[7]:
                                        status = "Overdue"
                                else:
                                        status = "Returned"
                                print(f'{row[0]:<12} {row[1]:<10} {row[2]:<40} {row[3]:<10} {row[4]:<20} {chk_date:<15} {due_date:<15} {return_date:<15} {status:<10}')
                        reptAng(userID)
                                
                elif commandOptions == 2:
                        name = input("Enter Last Name of Patron: ")
                        formattedName = "%" + name + "%"
                        patronSEARCH_dbcursor = cnx.cursor()
                        patronSEARCH_dbcursor.execute("SELECT * FROM patrons WHERE LastName LIKE %s", (formattedName, ))
                        patron_row = patronSEARCH_dbcursor.fetchall()
                        
                        print(f'{"PatronID:":<10} {"First Name:":<20} {"Last Name:":<20} {"Email:":<35} {"Phone:":<15}')
                        for patrons_row in patron_row:
                                print(f'{patrons_row[0]:<10} {patrons_row[1]:<20} {patrons_row[2]:<20} {patrons_row[3]:<35} {patrons_row[4]:<15}')
                        print("\n== Books Checked Out by Patron ==")
                        patronCHKOUT_dbcursor = cnx.cursor()
                        patronCHKOUT_dbcursor.execute("""SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
                                                        FROM checkouts
                                                        INNER JOIN books ON checkouts.BookID = books.bookID
                                                        INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID
                                                        WHERE patrons.LastName LIKE %s;""", (formattedName, ))
                        print(f'{"CheckoutID:":<12} {"BookID:":<10} {"BookName:":<40} {"PatronID:":<10} {"PatronName:":<20} {"Checkout Date:":<15} {"Due Date:":<15}  {"Return Date:":<15} {"Status:":<10}')
                        for row in patronCHKOUT_dbcursor:
                                chk_date = row[6].strftime('%Y-%m-%d') if hasattr(row[6], 'strftime') else str(row[6])
                                due_date = row[7].strftime('%Y-%m-%d') if hasattr(row[7], 'strftime') else str(row[7])
                                return_date = row[8].strftime('%Y-%m-%d') if hasattr(row[8], 'strftime') else str(row[8])
                                today = datetime.date.today()
                                if row[8] is None and today > row[7]:
                                        status = "Overdue"
                                elif row[8] is None:
                                        status = "Checked Out"
                                elif row[8] > row[7]:
                                        status = "Overdue"
                                else:
                                        status = "Returned"
                                print(f'{row[0]:<12} {row[1]:<10} {row[2]:<40} {row[3]:<10} {row[4]:<20} {chk_date:<15} {due_date:<15} {return_date:<15} {status:<10}')
                        reptAng(userID)
                else:
                        print("Returning to Main Menu...")
                        time.sleep(1)
                        mainMenu(userID)
        def libInvtStatus():
                bookINV_dbcursor = cnx.cursor()
                bookINV_dbcursor.execute("SELECT * FROM books")
                print(f'{"ID:":<5} {"Title:":<40} {"Total:":<15} {"Available:":<15} {"Checked Out:":<15} {"Status:":<15}') 
                for book_row in bookINV_dbcursor:
                        if book_row[5] == 0:
                                status = "Out of Stock"
                        elif book_row[5] < 5:
                                status = "Low Stock"
                        else:
                                status = "Available"
                        print(f'{book_row[0]:<5} {book_row[2]:<40} {book_row[4]:<15} {book_row[5]:<15} {book_row[4] - book_row[5]:<15} {status:<15}')
                reptAng(userID)

        def mycircStatus():
                bookCIRC_dbcursor = cnx.cursor()
                bookCIRC_dbcursor.execute("""SELECT CONCAT(MONTH(c.CheckoutDate), "/", YEAR(c.CheckoutDate)) AS "Month", COUNT(*) AS "Total Checkouts", SUM(CASE WHEN c.ReturnDate IS NOT NULL THEN 1 ELSE 0 END) AS "Total Returns", SUM(CASE WHEN c.ReturnDate IS NULL THEN 1 ELSE 0 END) AS "Books Currently Checked Out"
                                                FROM checkouts c
                                                LEFT JOIN books b ON b.bookID = c.BookId 
                                                GROUP BY CONCAT(MONTH(CheckoutDate), "/", YEAR(CheckoutDate))""")
                print(f'{"Month:":<10} {"Total Checkouts:":<20} {"Total Returns:":<15} {"Books Currently Checked Out:":<30}')
                for row in bookCIRC_dbcursor:
                        print(f'{row[0]:<10} {row[1]:<20} {row[2]:<15} {row[3]:<30}')
                reptAng(userID)
                       
                       
        print("""== Reports and Analytics ==\n
1. Most popular books (ordered by checkout frequency)
2. Overdue books report
3. Patron activity summary (books checked out, returned, overdue)
4. Library inventory status (available vs. out of stock)
5. Monthly/yearly circulation statistics\n""")

        commandOptions = int(input("What do you want to view?: "))
        if commandOptions == 1: popularBooks()
        elif commandOptions == 2: overDueBooks()
        elif commandOptions == 3: patronActSum()
        elif commandOptions == 4: libInvtStatus()
        elif commandOptions == 5: mycircStatus()
        elif commandOptions == 0:
                print("Now Exiting...") 
                time.sleep(1)
                mainMenu(userID)

def showAllBooks():
        bookALL_dbcursor = cnx.cursor()
        bookALL_dbcursor.execute("SELECT * FROM books")
        print(f'{"ID:":<5} {"ISBN:":<15} {"Title:":<40} {"Year:":<6} {"Total Copies:":<15} {"Available Copies:":<15}')
        for book_row in bookALL_dbcursor:
                print(f'{book_row[0]:<5} {book_row[1]:<15} {book_row[2]:<40} {book_row[3]:<6} {book_row[4]:<15} {book_row[5]:<15}')

       
def showAllPatrons():
        patronALL_dbcursor = cnx.cursor()
        patronALL_dbcursor.execute("SELECT * FROM patrons")
        print(f'{"PatronID:":<10} {"First Name:":<20} {"Last Name:":<20} {"Email:":<35} {"Phone:":<15}')
        for patrons_row in patronALL_dbcursor:
                print(f'{patrons_row[0]:<10} {patrons_row[1]:<20} {patrons_row[2]:<20} {patrons_row[3]:<35} {patrons_row[4]:<15}')

def showAllCheckouts():
       checkoutsALL_dbcursor = cnx.cursor()
       checkoutsALL_dbcursor.execute("""SELECT checkouts.CheckoutID, checkouts.BookID, books.title, checkouts.PatronID, CONCAT(patrons.FirstName, ' ', patrons.LastName) AS 'PatronName', checkouts.StaffID, checkouts.CheckoutDate, checkouts.DueDate, checkouts.ReturnDate
                                     FROM checkouts
                                     INNER JOIN books ON checkouts.BookID = books.bookID
                                     INNER JOIN patrons ON checkouts.PatronID = patrons.PatronID""")
       print(f'{"CheckoutID:":<12} {"BookID:":<10} {"BookName:":<40} {"PatronID:":<10} {"PatronName:":<20} {"StaffID:":<10} {"Checkout Date:":<15} {"Due Date:":<15}  {"Return Date:":<15}')
       for row in checkoutsALL_dbcursor:
                chk_date = row[6].strftime('%Y-%m-%d') if hasattr(row[6], 'strftime') else str(row[6])
                due_date = row[7].strftime('%Y-%m-%d') if hasattr(row[7], 'strftime') else str(row[7])
                return_date = row[8].strftime('%Y-%m-%d') if hasattr(row[8], 'strftime') else str(row[8])
                print(f'{row[0]:<12} {row[1]:<10} {row[2]:<40} {row[3]:<10} {row[4]:<20} {row[5]:<10} {chk_date:<15} {due_date:<15} {return_date:<15}')



try:
    print("Connecting server...")
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password9999",
        database="finalproject"
    )

    time.sleep(2)

    print("SQL Connection successful! \n")

    print("""---Library Management System---
Welcome! Please Login to Continue\n""")

    isloggedin = False
    userID = 0

    while not isloggedin:
        isloggedin, userID = loginPrompt()


except mysql.connector.Error as err:
    print(f"CRITICAL ERROR: {err}")

finally:
    if 'cnx' in locals() and cnx.is_connected():
        cnx.close()