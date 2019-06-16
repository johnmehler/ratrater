# RatRater
Python script to interact with US Chess Center KIDS database

## Setup process
1. Replace the placeholder variables with the username, pass, server, and database name. 
2. Set up an ODBC data source on your computer.
  a. For Windows, that means typing "ODBC" in the search bar and selecting "ODBC data sources (32-bit)"
  b. Add "ODBC Driver 17 for SQL server". The name and description are for your benefit, the server name must match the server you're working on.
  c. Authenticate with SQL Server Authentication, and use the credentials you were given. 
  d. Continue through and select finish, then verify that the tests connect properly.
  e. Verify that the program loads when you run it.
  
## TODO
1. Update export() to include first and last names

2. I would like an "undo" button that would undo a mistaken game result entry that has been entered after hitting the "save changes" button in the Ratrater game results window.

3. Update rate() and save() methods to have the dialog window display the result as "draw" instead of a "win"/"loss".

4. Break rate() and save() methods into cases using switches and add several new options
  a. F - The bottom player was forfeited. Subtract an additional 25 points from the rating of the loser.
  b. X - Double forfeit. Both players lose 75 points.
  c. In the case that the result is not one of the accepted results, do not make a change and print a message to the user.

5. If a rating is under 1000, an error message should be printed and no changes should be made.
