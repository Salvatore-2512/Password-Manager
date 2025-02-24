from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

class Password:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1450x800+0+0")
        self.root.title("Password Manager")
        
        self.var_Sname = StringVar()
        self.var_url = StringVar()
        self.var_Uname = StringVar()
        self.var_pwd = StringVar()
        
        lbl = Label(self.root, text="Password Manager", font=('Courier New', 42, 'bold'), fg='darkblue', bg='white')
        lbl.place(x=0, y=0, width=1438, height=70)
        
        main_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        main_frame.place(x=0, y=60, width=1438, height=780)
        
        leftFrame = LabelFrame(main_frame, bd=2, relief=RIDGE, font=('Courier New', 27, 'bold'), bg="white", text="ENTRY", fg='blue')
        leftFrame.place(x=10, y=62, width=500, height=600)
        
        labels = ["SiteName:", "URL:", "UserName:", "Password:"]
        vars = [self.var_Sname, self.var_url, self.var_Uname, self.var_pwd]
        
        for i, (label, var) in enumerate(zip(labels, vars)):
            lbl = Label(leftFrame, text=label, font=('Arial', 21, 'bold'), bg='white')
            lbl.place(x=30, y=80 + i * 70)
            ent = ttk.Entry(leftFrame, textvariable=var, width=22, font=('Arial', 20))
            ent.place(x=170, y=80 + i * 70)
        
        button_frame = Frame(leftFrame, bd=2, relief=RIDGE, bg="white")
        button_frame.place(x=20, y=370, width=430, height=170)
        
        buttons = [
            ("ADD", self.addData),
            ("UPDATE", self.update),
            ("REFRESH", self.refresh),
            ("DELETE", self.delete)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = Button(button_frame, text=text, font=('Arial', 20, 'bold'), width=10, height=1, command=command)
            btn.grid(row=i//2, column=i%2, padx=30 if i%2 == 0 else 80, pady=30)
        
        rightFrame = LabelFrame(main_frame, bd=2, relief=RIDGE, font=('Courier New', 27, 'bold'), bg="white", text="TABLE", fg='blue')
        rightFrame.place(x=550, y=62, width=870, height=600)
        
        tableFrame = Frame(rightFrame, bd=3, relief=RIDGE)
        tableFrame.place(x=5, y=5, width=855, height=550)
        
        scroll_y = ttk.Scrollbar(tableFrame, orient=VERTICAL)
        self.passwdTable = ttk.Treeview(tableFrame, height=40, columns=("Sname", "url", "Uname", "pwd"), yscrollcommand=scroll_y.set)
        
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.passwdTable.yview)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=30, fieldbackground="silver")
        
        headings = ["Site Name", "URL", "UserName", "Password"]
        columns = ["Sname", "url", "Uname", "pwd"]
        
        for col, heading in zip(columns, headings):
            self.passwdTable.heading(col, text=heading)
            self.passwdTable.column(col, width=80, anchor=CENTER)
        
        self.passwdTable['show'] = 'headings'
        self.passwdTable.pack(fill=BOTH, expand=1)
        
        self.fetchData()
        self.passwdTable.bind("<ButtonRelease>", self.getCursor)
    
    def addData(self):
        con = mysql.connector.connect(host="localhost", username="root", password="Aryan@123", database="Project")
        mycursor = con.cursor()
        mycursor.execute('INSERT INTO passwd VALUES (%s, %s, %s, %s)',
                         (self.var_Sname.get(), self.var_url.get(), self.var_Uname.get(), self.var_pwd.get()))
        con.commit()
        self.fetchData()
        con.close()
        messagebox.showinfo('Success', 'Information has been Added', parent=self.root)
    
    def fetchData(self):
        con = mysql.connector.connect(host="localhost", username="root", password="Aryan@123", database="Project")
        mycursor = con.cursor()
        mycursor.execute("SELECT * FROM passwd")
        data = mycursor.fetchall()
        if data:
            self.passwdTable.delete(*self.passwdTable.get_children())
            for row in data:
                self.passwdTable.insert("", END, values=row)
        con.commit()
        con.close()
    
    def getCursor(self, event=""):
        cursor_row = self.passwdTable.focus()
        content = self.passwdTable.item(cursor_row)
        data = content['values']
        self.var_Sname.set(data[0])
        self.var_url.set(data[1])
        self.var_Uname.set(data[2])
        self.var_pwd.set(data[3])
    
    def update(self):
        con = mysql.connector.connect(host="localhost", username="root", password="Aryan@123", database="Project")
        mycursor = con.cursor()
        mycursor.execute("UPDATE passwd SET URL = %s, UserName = %s, Password = %s WHERE SiteName = %s", 
                         (self.var_url.get(), self.var_Uname.get(), self.var_pwd.get(), self.var_Sname.get()))
        con.commit()
        self.fetchData()
        con.close()
        messagebox.showinfo('Success', 'Information has been Updated', parent=self.root)
    
    def delete(self):
        if messagebox.askyesno('Delete', 'Are you sure you want to delete this password?', parent=self.root):
            con = mysql.connector.connect(host="localhost", username="root", password="Aryan@123", database="Project")
            mycursor = con.cursor()
            mycursor.execute("DELETE FROM passwd WHERE SiteName = %s", (self.var_Sname.get(),))
            con.commit()
            self.fetchData()
            con.close()
            messagebox.showinfo('Success', 'Information has been Deleted', parent=self.root)
    
    def refresh(self):
        self.var_Sname.set("")
        self.var_url.set("")
        self.var_Uname.set("")
        self.var_pwd.set("")

if __name__ == "__main__":
    root = Tk()
    obj = Password(root)
    root.mainloop()
