'''
For whoever is trying to make the recommended changes:

1. Make sure to install the required modules and keep a clean environment.
2. In order to get this working, you have to set up an ODBC data source on your computer.
    a. Make sure that the driver in the connection string matches the driver you use for your ODBC source
3. Hardcode your user and pass in. Ideally we'll set up an integration database and have developer credentials for that.
4. The top part is a GUI and you don't need to mess with it. The part that needs fixing is the rate() and save() method.
    a. save() and rate() are the same thing-- save isn't saving an existing change, it's rating it again but this time saving it.
    b. save() and rate() should be done with switches for each of the cases my dad/Robert wants instead of the if-else. You will probably want additional methods for each.
'''

import pyodbc
from tkinter import *
import xlwt

#### Init spreadsheet
wb = xlwt.Workbook()
ws = wb.add_sheet('Kids Database')

#### Connect to Azure SQLdb
username = "REPLACE WITH USERNAME"
password = "REPLACE WITH PASSWORD"
server = "REPLACE WITH SERVER NAME"
database = "REPLACE WITH DATABASE NAME"
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:'+server+'.database.windows.net,1433;Database='+database+';Uid='+username+';Pwd='+password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

#### Initialize GUI
ratings = Tk()
ratings.title('Rat Rater')
ratings.bind_class("Button", "<Key-Return>", lambda event: event.widget.invoke())

#### Set globals
k_value = IntVar()
k_value.__init__(value=75)
inf_val = IntVar()
inf_val.__init__(value=5)
winner_id = StringVar()
loser_id = StringVar()
winner_name = StringVar()
loser_name = StringVar()
winner_rating = StringVar()
loser_rating = StringVar()
school_name = StringVar()
result = StringVar()
result.__init__(value='W')
w_new_rate = StringVar()
w_new_rate.set('None')
l_new_rate = StringVar()
l_new_rate.set('None')

#### Select School
school_entry = Entry(ratings, textvariable = school_name, font=("Times New Roman", 12),width=3)
school_entry.grid(row=1,column=0)

#### GUI winner and loser's ID
Label(ratings, text = "Player 1: ", font=("Times New Roman", 16)).grid(row=3,column=3)
winner_entry = Entry(ratings, textvariable = winner_id, font=("Times New Roman", 16),width=6)
winner_entry.grid(row=3,column=4)
Label(ratings, text = "Player 2: ", font=("Times New Roman", 16)).grid(row=5,column=3)
loser_entry = Entry(ratings, textvariable = loser_id, font=("Times New Roman", 16),width=6)
loser_entry.grid(row=5,column=4)
Label(ratings,text = " ", font=("Times New Roman",6)).grid(row=6,column=4)
rate_button = Button(ratings, text = "Rate", font=("Times New Roman", 16), command = lambda: rate())
rate_button.grid(row=7,column=4)
save_button = Button(ratings, text = "Save Changes", font=("Times New Roman", 16), command = lambda: save_ratings())
save_button.grid(row=9,column=4)
win_or_draw = Entry(ratings, textvariable = result, font=("Times New Roman", 16),width=2)
win_or_draw.grid(row=4,column=4)

#### Auto-update the boxes
Label(ratings,textvariable=winner_name,font=("Times New Roman",16)).grid(row=3,column=7)
Label(ratings,textvariable=loser_name,font=("Times New Roman",16)).grid(row=5,column=7)
Label(ratings,text="     ",font=("Times New Roman",16)).grid(row=5,column=8)
Label(ratings,textvariable=winner_rating,font=("Times New Roman",16)).grid(row=3,column=9)
Label(ratings,textvariable=loser_rating,font=("Times New Roman",16)).grid(row=5,column=9)
Label(ratings,text="     ",font=("Times New Roman",16)).grid(row=5,column=10)
Label(ratings,textvariable=w_new_rate,font=("Times New Roman",16)).grid(row=3,column=11)
Label(ratings,textvariable=l_new_rate,font=("Times New Roman",16)).grid(row=5,column=11)

#### GUI formula information
Label(ratings, text = "Base gain", font=("Times New Roman", 12)).grid(row=1,column=12)
k_entry = Entry(ratings, textvariable = k_value, font=("Times New Roman", 12),width=4)
k_entry.grid(row=1,column=11)
Label(ratings, text = "Bonus", font=("Times New Roman", 12)).grid(row=2,column=12)
inflation_factor = Entry(ratings, textvariable = inf_val, font=("Times New Roman", 12),width=4)
inflation_factor.grid(row=2,column=11)
clear_button=Button(ratings,text="Clear",font=("Times New Roman",16),command=lambda:clear_text()).grid(row=9,column=9)
Label(ratings,text = "    ", font=("Times New Roman",6)).grid(row=8,column=4)
export_button=Button(ratings,text="Export",font=("Times New Roman", 16),command=lambda:export()).grid(row=9,column=12)

display_button=Button(ratings,text="Display",font=("Times New Roman",8),command=lambda:display()).grid(row=2,column=0)

#### Display
def display():
    var = school_name.get()
    var += '%'
    cursor = conn.cursor()
    cursor.execute("SELECT LocalID FROM KIDS WHERE LocalID LIKE ? ORDER BY FirstName", var)
    ids=cursor.fetchall()
    cursor.execute("SELECT FirstName FROM KIDS WHERE LocalID LIKE ? ORDER BY FirstName", var)
    names=cursor.fetchall()
    cursor.execute("SELECT lastName FROM KIDS WHERE LocalID LIKE ? ORDER BY FirstName", var)
    names2=cursor.fetchall()
    cursor.execute("SELECT Rating FROM KIDS WHERE LocalID LIKE ? ORDER BY FirstName", var)
    ratings=cursor.fetchall()
    c=0
    for val in ids:
        print(ids[c],names[c],names2[c],ratings[c])
        c+=1

#### Export
def export():
    var = school_name.get()
    var += '%'
    cursor = conn.cursor()
    cursor.execute("SELECT LocalID FROM KIDS WHERE LocalID LIKE ? ORDER BY LocalID", var)
    ids = cursor.fetchall()
    cursor.execute("SELECT Rating FROM KIDS WHERE LocalID LIKE ? ORDER BY LocalID", var)
    ratings = cursor.fetchall()

    counter1=0
    counter2=0
    id_list = []
    rating_list = []

    for val in ids:
        id_list += val

    for val in ratings:
        rating_list += val

    for obj in id_list:
        ws.write(counter1, 0, obj)
        counter1 += 1
        
    for obj in rating_list:
        ws.write(counter2, 1, obj)
        counter2 += 1

    wb.save('school.xls')

#### Clear method -----------------------------

fields = [winner_entry,loser_entry]
def clear_text():
    for obj in fields:
        obj.delete(0, END)

#### End of Clear Method ----------------------


#### Rate method ------------------------------

def rate():
    (winner_rating,winner_name,winner) = find_winner()
    (loser_rating,loser_name,loser) = find_loser()

    cursor = conn.cursor()

    try:
        k = int(k_value.get())
        if type(k) is not int:
            k = 75
        inflation_value = int(inf_val.get())
        if type(inflation_value) is not int:
            inflation_value = 75
        
        diff = loser_rating - winner_rating
        if diff <= -740:
            diff = -740

        res = 0
        r = result.get()
        if r == 'D':
            res = 0
        else:
            res = 1
        change = int(k*res + diff*.1)
        winner_new_rating = (winner_rating + change + inflation_value)
        loser_new_rating = (loser_rating - change + inflation_value)

        print(winner, winner_name, "wins: ", winner_rating, "-->", winner_new_rating)
        print(loser, loser_name, "loses: ", loser_rating, "-->", loser_new_rating)
    
#        cursor.execute("UPDATE KIDS SET Rating = ? WHERE LocalID = ?", winner_new_rating, winner)
#        cursor.execute("UPDATE KIDS SET Rating = ? WHERE LocalID = ?", loser_new_rating, loser)

        w_new_rate.set(winner_new_rating)
        l_new_rate.set(loser_new_rating)

    except Exception as e:
        print(str(e))
        
#### End of Rate ------------------------------
#### Find methods -----------------------------
def find_winner():
    try:
        cursor = conn.cursor()
        winner = winner_id.get()
        school = school_name.get()
        temp = school+winner
        cursor.execute("SELECT Rating FROM KIDS WHERE LocalID = ?",temp)
        winner_rating = cursor.fetchval()
        cursor.execute("SELECT FirstName FROM KIDS WHERE LocalID = ?",temp)
        winner_firstname = cursor.fetchval()
        return (winner_rating,winner_firstname,temp)
    except:
        return 0
def find_loser():
    try:
        cursor = conn.cursor()
        loser = loser_id.get()
        school = school_name.get()
        temp = school+loser
        cursor.execute("SELECT Rating FROM KIDS WHERE LocalID = ?",temp)
        loser_rating = cursor.fetchval()
        cursor.execute("SELECT FirstName FROM KIDS WHERE LocalID = ?",temp)
        loser_firstname = cursor.fetchval()
        return (loser_rating,loser_firstname,temp)
    except:
        return 0

#### End of Find methods --------------------------

#### Save method ----------------------------------

def save_ratings(): # Ok nobody look at this method
    cursor = conn.cursor()

    (winner_rating,winner_name,winner) = find_winner()
    (loser_rating,loser_name,loser) = find_loser()

    cursor = conn.cursor()

    k = int(k_value.get())
    inflation_value = int(inf_val.get())
    
    diff = loser_rating - winner_rating
    if diff <= -740:
        diff = -740

    res = 0
    r = result.get()
    if r == 'D':
        res = 0
    else:
        res = 1
    change = int(k*res + diff*.1)
    winner_new_rating = (winner_rating + change + inflation_value)
    loser_new_rating = (loser_rating - change + inflation_value)

    cursor.execute("UPDATE KIDS SET Rating = ? WHERE LocalID = ?", winner_new_rating, winner)
    cursor.execute("UPDATE KIDS SET Rating = ? WHERE LocalID = ?", loser_new_rating, loser)
    conn.commit()

    winner_entry.focus()
    clear_text()
    w_new_rate.set('None')
    l_new_rate.set('None')

#### Trace methods
def update_loser(*args):
    cursor = conn.cursor()
    loser = loser_id.get()
    school = school_name.get()
    school = school.upper()
    temp = school+loser

    cursor.execute("SELECT Rating FROM KIDS WHERE LocalID = ?", temp)
    rating=cursor.fetchval()
    loser_rating.set(rating)
    cursor.execute("SELECT FirstName FROM KIDS WHERE LocalID = ?", temp)
    name=cursor.fetchval()
    loser_name.set(name)

def update_winner(*args):
    cursor = conn.cursor()
    winner = winner_id.get()
    school = school_name.get()
    temp = school+winner

    cursor.execute("SELECT Rating FROM KIDS WHERE LocalID = ?", temp)
    rating=cursor.fetchval()
    winner_rating.set(rating)
    cursor.execute("SELECT FirstName FROM KIDS WHERE LocalID = ?", temp)
    name=cursor.fetchval()
    winner_name.set(name)
    
loser_id.trace("w",update_loser)
winner_id.trace("w",update_winner)
ratings.mainloop()
