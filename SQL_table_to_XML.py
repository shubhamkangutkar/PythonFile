import tkinter.messagebox as messagebox
from tkinter import *
import mysql.connector as m
from email_validator import validate_email, EmailNotValidError
import re
import pgeocode

root = Tk()
# root.geometry("450x600")
root.title('Validate Data')
email_reg = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'

def button_press(event):
    if (host == "" or user == "" or pw == "" or db == "" or table == ""):
        messagebox.showinfo("Information","All fields are required!")
    else:
        count = 0
        host_value = host.get()
        user_value = user.get()
        pw_value = pw.get()
        db_value = db.get()
        table_value = table.get()
        file_value = file.get()

        mydb = m.connect(host=host_value, user=user_value, passwd=pw_value, database=db_value)
        mycursor = mydb.cursor()
        query = "select * from %s Limit 10" % table_value
        mycursor.execute(query)
        table_data = mycursor.fetchall()
        table_columns = mycursor.column_names
        for i in table_data:
            print(i)
        outfileName = r'C:\Users\ShubhamKangutkar\Desktop\%s.xml' %file_value

        outfile = open(outfileName, 'w')
        outfile.write('<?xml version="1.0" ?>\n')
        outfile.write('<mydata>\n')
        for row in table_data:
              try:
                nomi = pgeocode.Nominatim(row[1])
                value = nomi.query_postal_code(row[5])
                if value[1] == row[1]:
              # try:
              #   valid = validate_email(row[2])
              # if re.search(email_reg, row[2]):
                    outfile.write('  <row>\n')
                    outfile.write('    <KUNNR>%s</KUNNR>\n' % row[0])
                    outfile.write('    <LAND1>%s</LAND1>\n' % row[1])
                    outfile.write('    <NAME1>%s</NAME1>\n' % row[2])
                    outfile.write('    <NAME2>%s</NAME2>\n' % row[3])
                    outfile.write('    <PSTLZ>%s</PSTLZ>\n' % row[5])
                    outfile.write('    <TELF1>%s</TELF1>\n' % row[9])
                    outfile.write('    <ADRNR>%s</ADRNR>\n' % row[12])
                    outfile.write('  </row>\n')
                    outfile.write('</mydata>\n')
                    count = count + 1
                else:
                    print('customer %s Postal code %s not Valid.' % (row[0],row[5]))
              except ValueError as e:
                    print( 'customer %s Postal code %s not Valid.'%(row[0],row[5]))
        outfile.close()
        messagebox.showinfo("File Created","%s.xml file is created with valid records : %s " %(file_value,count))

host_label = Label(root,text='Host :')
host_label.grid(row = 2, column = 1)

host = StringVar()
host.set('localhost')
host = Entry(root,width=60, textvariable = host)
host.grid(row=2, column=3)

user_label = Label(root,text='User :')
user_label.grid(row = 3, column = 1)

user = StringVar()
user.set('root')
user = Entry(root,width=60, textvariable=user)
user.grid(row=3, column=3)

pw_label = Label(root,text='Password :')
pw_label.grid(row = 4, column = 1)

pw = StringVar()
pw.set('Dag96622')
pw = Entry(root,width=60, textvariable=pw)
pw.grid(row=4, column=3)

db_label = Label(root,text='Database :')
db_label.grid(row = 5, column = 1)

db = StringVar()
db.set('s04')
db = Entry(root,width=60, textvariable = db)
db.grid(row=5, column=3)

table_label = Label(root,text='Table :')
table_label.grid(row = 6, column = 1)

table = StringVar()
table.set('kna1')
table = Entry(root,width=60, textvariable = table)
table.grid(row=6, column=3)


file_label = Label(root,text='File name :')
file_label.grid(row = 7, column = 1)

file = StringVar()
file.set('kna1')
file = Entry(root,width=60, textvariable = file)
file.grid(row=7, column=3)

grabBtn = Button(root, text="Validate and Generate XML", bg='light blue')
grabBtn.grid(row=8, column=3)
grabBtn.bind('<Button-1>', button_press)
#
# button = Button(root,text = "Validate and Generate XML", command=button_press)
# button.place(x=150, y=130)

root.mainloop()
