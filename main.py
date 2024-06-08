import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.title("Student Registration System")
root.geometry("1080x720")
my_tree = ttk.Treeview(root)
conn = sqlite3.connect("Student.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS crud (
    stud_id INTEGER PRIMARY KEY,
    firstname TEXT,
    lastname TEXT,
    address TEXT,
    phone TEXT,
    user_id INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS login (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

current_user_id = None

def login():
    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.geometry("1080x720")

    def authenticate():
        username = usernameEntry.get()
        password = passwordEntry.get()
        cur.execute("SELECT * FROM login WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        if user:
            global current_user_id
            current_user_id = user[0]
            login_window.destroy()
            fetch_data()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register_user():
        username = usernameEntry.get()
        password = passwordEntry.get()
        if username and password:
            try:
                cur.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", "User registered successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")
        else:
            messagebox.showwarning("Warning", "Please fill all fields")

    usernameLabel = Label(login_window, text="Username", font=('Arial', 15))
    passwordLabel = Label(login_window, text="Password", font=('Arial', 15))
    usernameEntry = Entry(login_window, width=30, bd=3, font=('Arial', 15))
    passwordEntry = Entry(login_window, width=30, bd=3, font=('Arial', 15), show='*')
    loginButton = Button(login_window, text="Login", padx=20, pady=10, font=('Arial', 15),bg="#84F894", command=authenticate)
    registerButton = Button(login_window, text="Register", padx=10, pady=10, font=('Arial', 15),bg="#F4FE82", command=register_user)

    usernameLabel.pack(pady=10)
    usernameEntry.pack(pady=5)
    passwordLabel.pack(pady=10)
    passwordEntry.pack(pady=5)
    loginButton.pack(pady=10)
    registerButton.pack(pady=10)

    
def add_student():
    stud_id = studidEntry.get()
    firstname = fnameEntry.get()
    lastname = lnameEntry.get()
    address = addressEntry.get()
    phone = phoneEntry.get()
    
    if stud_id and firstname and lastname and address and phone:
        cur.execute("INSERT INTO crud (stud_id, firstname, lastname, address, phone, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (stud_id, firstname, lastname, address, phone, current_user_id))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        fetch_data()
    else:
        messagebox.showwarning("Warning", "Please fill all fields")

def fetch_data():
    for item in my_tree.get_children():
        my_tree.delete(item)
    cur.execute("SELECT * FROM crud WHERE user_id=?", (current_user_id,))
    rows = cur.fetchall()
    for row in rows:
        my_tree.insert("", END, values=row)

def update_student():
    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')
    stud_id = studidEntry.get()
    firstname = fnameEntry.get()
    lastname = lnameEntry.get()
    address = addressEntry.get()
    phone = phoneEntry.get()

    if stud_id and firstname and lastname and address and phone:
        cur.execute("""UPDATE crud SET firstname=?, lastname=?, address=?, phone=?
                       WHERE stud_id=? AND user_id=?""",
                    (firstname, lastname, address, phone, stud_id, current_user_id))
        conn.commit()
        messagebox.showinfo("Success", "Student updated successfully!")
        fetch_data()
    else:
        messagebox.showwarning("Warning", "Please fill all fields")

def delete_student():
    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')
    if values:
        cur.execute("DELETE FROM crud WHERE stud_id=? AND user_id=?", (values[0], current_user_id))
        conn.commit()
        messagebox.showinfo("Success", "Student deleted successfully!")
        fetch_data()
    else:
        messagebox.showwarning("Warning", "Please select a student")

def search_student():
    stud_id = studidEntry.get()
    for item in my_tree.get_children():
        my_tree.delete(item)
    cur.execute("SELECT * FROM crud WHERE stud_id=? AND user_id=?", (stud_id, current_user_id))
    rows = cur.fetchall()
    for row in rows:
        my_tree.insert("", END, values=row)

def select_student():
    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')
    if values:
        studidEntry.delete(0, END)
        fnameEntry.delete(0, END)
        lnameEntry.delete(0, END)
        addressEntry.delete(0, END)
        phoneEntry.delete(0, END)
        studidEntry.insert(0, values[0])
        fnameEntry.insert(0, values[1])
        lnameEntry.insert(0, values[2])
        addressEntry.insert(0, values[3])
        phoneEntry.insert(0, values[4])
    else:
        messagebox.showwarning("Warning", "Please select a student")

def reset_fields():
    studidEntry.delete(0, END)
    fnameEntry.delete(0, END)
    lnameEntry.delete(0, END)
    addressEntry.delete(0, END)
    phoneEntry.delete(0, END)

label = Label(root, text="Student Registration System (CRUD OPERATION)", font=('Arial Bold', 30))
label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=40)

studidLabel = Label(root, text="Stud ID", font=('Arial', 15))
fnameLabel = Label(root, text="Firstname", font=('Arial', 15))
lnameLabel = Label(root, text="Lastname", font=('Arial', 15))
addressLabel = Label(root, text="Address", font=('Arial', 15))
phoneLabel = Label(root, text="Phone", font=('Arial', 15))

studidLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
fnameLabel.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
lnameLabel.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
addressLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5)
phoneLabel.grid(row=7, column=0, columnspan=1, padx=50, pady=5)

studidEntry = Entry(root, width=55, bd=3, font=('Arial', 15))
fnameEntry = Entry(root, width=55, bd=3, font=('Arial', 15))
lnameEntry = Entry(root, width=55, bd=3, font=('Arial', 15))
addressEntry = Entry(root, width=55, bd=3, font=('Arial', 15))
phoneEntry = Entry(root, width=55, bd=3, font=('Arial', 15))

studidEntry.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
fnameEntry.grid(row=4, column=1, columnspan=4, padx=5, pady=0)
lnameEntry.grid(row=5, column=1, columnspan=4, padx=5, pady=0)
addressEntry.grid(row=6, column=1, columnspan=4, padx=5, pady=0)
phoneEntry.grid(row=7, column=1, columnspan=4, padx=5, pady=0)

addbtn = Button(root, text="Add", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#84F894", command=add_student)
updatebtn = Button(root, text="Update", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#84E8F8", command=update_student)
deletebtn = Button(root, text="Delete", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#FF9999", command=delete_student)
selectbtn = Button(root, text="Select", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#F4FE82", command=select_student)
resetbtn = Button(root, text="Reset", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#F398FF", command=reset_fields)
searchbtn = Button(root, text="Search", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#EEEEEE", command=search_student)

addbtn.grid(row=3, column=5, columnspan=1, rowspan=2)
updatebtn.grid(row=5, column=5, columnspan=1, rowspan=2)
deletebtn.grid(row=7, column=5, columnspan=1, rowspan=2)
selectbtn.grid(row=9, column=5, columnspan=1, rowspan=2)
resetbtn.grid(row=11, column=5, columnspan=1, rowspan=2)
searchbtn.grid(row=13, column=5, columnspan=1, rowspan=2)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial Bold', 15))
my_tree['columns'] = ("Stud ID", "Firstname", "Lastname", "Address", "Phone")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Stud ID", anchor=W, width=170)
my_tree.column("Firstname", anchor=W, width=150)
my_tree.column("Lastname", anchor=W, width=150)
my_tree.column("Address", anchor=W, width=165)
my_tree.column("Phone", anchor=W, width=150)

my_tree.heading("Stud ID", text="Student ID", anchor=W)
my_tree.heading("Firstname", text="Firstname", anchor=W)
my_tree.heading("Lastname", text="Lastname", anchor=W)
my_tree.heading("Address", text="Address", anchor=W)
my_tree.heading("Phone", text="Phone", anchor=W)

my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)
login()
root.mainloop()
