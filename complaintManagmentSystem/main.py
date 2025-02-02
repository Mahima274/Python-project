import mysql.connector
import tkinter as tk
from tkinter import Button, Label
from tkinter import messagebox, PhotoImage, Label,Button,Frame,Toplevel
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import *

import bcrypt


# Establish MySQL connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="Radhekrishn..",  # Replace with your MySQL password
        database="university_complaints_db"  # Replace with your MySQL database name
    )

def register_user():
    db = connect_db()
    cursor = db.cursor()

    username = entry_username.get()
    email = entry_email.get()
    password = entry_password.get()

    if username and email and password:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                           (username, email, hashed_password))
            db.commit()
            messagebox.showinfo("Success", "Signup successful!")
            signup_window.destroy()
            login_page()  # Return to login page after signup
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            db.close()
    else:
        messagebox.showerror("Error", "All fields are required!")

def login_user():
    db = connect_db()
    cursor = db.cursor()

    username = entry_username.get()
    password = entry_password.get()

    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        main_window()  # Open main page after successful login
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

    cursor.close()
    db.close()


# Signup Page
def signup_page():
    global signup_window, entry_username, entry_email, entry_password
    
    signup_window = tk.Tk()
    signup_window.title("Signup")
    
    # Set window geometry and background
    signup_window.geometry("1330x778+0+0")
    signup_window.configure(bg="white")

    bg_image = PhotoImage(file='mang.png')  # Background image for signup
    titleLabel = Label(signup_window, image=bg_image, compound="left",
                       text="  Signup  ", font=('times new roman', 30, 'bold'),
                       bg='#010c48', fg="white", anchor='w', padx='20')
    titleLabel.place(x=0, y=0, relwidth=1)

    tk.Label(signup_window, text="Username:", bg="white", font=('times new roman', 20, 'bold'), fg='#010c48').place(x=400, y=200)
    entry_username = tk.Entry(signup_window, font=('times new roman', 18))
    entry_username.place(x=600, y=200)

    tk.Label(signup_window, text="Email:", bg="white", font=('times new roman', 20, 'bold'), fg='#010c48').place(x=400, y=270)
    entry_email = tk.Entry(signup_window, font=('times new roman', 18))
    entry_email.place(x=600, y=270)

    tk.Label(signup_window, text="Password:", bg="white", font=('times new roman', 20, 'bold'), fg='#010c48').place(x=400, y=340)
    entry_password = tk.Entry(signup_window, show='*', font=('times new roman', 18))
    entry_password.place(x=600, y=340)

    tk.Button(signup_window, text="Signup", command=register_user, font=('times new roman', 20, 'bold'), fg='#010c48').place(x=600, y=420)
    
    signup_window.mainloop()

# Function to log out the user
def logout_user():
    global current_user
    current_user = None
    root.destroy()
    login_page()  # Redirect to the login page after logging out

# Function to update user information
def update_user():
    global current_user
    db = connect_db()
    cursor = db.cursor()

    new_username = entry_new_username.get()
    new_email = entry_new_email.get()
    new_password = entry_new_password.get()

    if new_username and new_email and new_password:
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute("UPDATE users SET username=%s, email=%s, password=%s WHERE username=%s", 
                           (new_username, new_email, hashed_password, current_user))
            db.commit()
            messagebox.showinfo("Success", "User information updated successfully!")
            current_user = new_username  # Update current user if username is changed
            settings_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            db.close()
    else:
        messagebox.showerror("Error", "All fields are required!")

# Function to create the settings page
def settings_page():
    global settings_window, entry_new_username, entry_new_email, entry_new_password

    settings_window = tk.Toplevel(root)  # Create a new window
    settings_window.title("Settings")
    settings_window.geometry("400x400")
    settings_window.configure(bg="white")

    tk.Label(settings_window, text="New Username:", bg="white", font=('times new roman', 15)).pack(pady=10)
    entry_new_username = tk.Entry(settings_window, font=('times new roman', 15))
    entry_new_username.pack(pady=10)

    tk.Label(settings_window, text="New Email:", bg="white", font=('times new roman', 15)).pack(pady=10)
    entry_new_email = tk.Entry(settings_window, font=('times new roman', 15))
    entry_new_email.pack(pady=10)

    tk.Label(settings_window, text="New Password:", bg="white", font=('times new roman', 15)).pack(pady=10)
    entry_new_password = tk.Entry(settings_window, show='*', font=('times new roman', 15))
    entry_new_password.pack(pady=10)

    tk.Button(settings_window, text="Update", command=update_user, font=('times new roman', 15), bg="#009688", fg="white").pack(pady=20)
    tk.Button(settings_window, text="Logout", command=logout_user, font=('times new roman', 15), bg="#e57373", fg="white").pack(pady=20)

def exit_app():
    # Confirm exit
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()  # Close the main window


# Login Page
def login_page():
    global login_window, entry_username, entry_password

    login_window = tk.Tk()
    login_window.title("Login")
    
    # Set window geometry and background
    login_window.geometry("1330x778+0+0")
    login_window.configure(bg="white")

    bg_image = PhotoImage(file='mang.png')  # Background image for login
    titleLabel = Label(login_window, image=bg_image, compound="left",
                       text="  Login  ", font=('times new roman', 30, 'bold'),
                       bg='#010c48', fg="white", anchor='w', padx='20')
    titleLabel.place(x=0, y=0, relwidth=1)

    tk.Label(login_window, text="Username:", bg="white", font=('times new roman', 20, 'bold'), fg='#010c48').place(x=400, y=200)
    entry_username = tk.Entry(login_window, font=('times new roman', 18))
    entry_username.place(x=600, y=200)

    tk.Label(login_window, text="Password:", bg="white", font=('times new roman', 20, 'bold'), fg='#010c48').place(x=400, y=270)
    entry_password = tk.Entry(login_window, show='*', font=('times new roman', 18))
    entry_password.place(x=600, y=270)

    tk.Button(login_window, text="Login", command=login_user, font=('times new roman', 20, 'bold'), fg='#010c48').place(x=600, y=350)
    tk.Button(login_window, text="Signup", command=lambda: [login_window.destroy(), signup_page()], font=('times new roman', 20, 'bold'), fg='#010c48').place(x=600, y=400)

    login_window.mainloop()

# Global variable for the main application window
root = None

# Main indow
def main_window():
   global root
   if root is None:
    root = tk.Tk()  # Initialize root here
    root.title("Complaint Management System")
    root.geometry("1330x778+0+0")
    root.configure(bg="white")


    # Load background image
    try:
        bg_image = PhotoImage(file='mang.png')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")
        return
    titleLabel = Label(root, image=bg_image, compound="left", text="  Complaint Management System  ", font=('times new roman', 30, 'bold'), bg='#010c48', fg="white", anchor='w', padx='20')
    titleLabel.place(x=0, y=0, relwidth=1)

    logoutButton = Button(root, text='Logout', font=('times new roman', 20, 'bold'), fg='#010c48', command=logout_user)
    logoutButton.place(x=1100, y=10)

    leftFrame = Frame(root)
    leftFrame.place(x=0, y=102, width=200, height=555)

    # Right frame for displaying dynamic content
    rightFrame = Frame(root, bg="white")
    rightFrame.place(x=200, y=102, width=1070, height=555)

    boardImage = PhotoImage(file="board.png")
    imageLabel = Label(leftFrame, image=boardImage)
    imageLabel.grid(row=0, column=0)
    imageLabel.pack()

    menuLabel = Label(leftFrame, text="Menu", font=('times new roman', 20), bg='#009688')
    menuLabel.pack(fill=X)

    Lodge_Complaint_button = Button(leftFrame, text="Lodge Complaint", font=('times new roman', 19, 'bold'), anchor='w', command=Lodge_form)
    Lodge_Complaint_button.pack(fill=X)

    view_button = Button(leftFrame, text="View Complaint", font=('times new roman', 19, 'bold'), anchor='w', command=View_form)
    view_button.pack(fill=X)

    withdraw_button = Button(leftFrame, text="Withdraw Complaint", font=('times new roman', 16, 'bold'), anchor='w', command=Withdraw_form)
    withdraw_button.pack(fill=X)

    Complaint_status_button = Button(leftFrame, text="Complaint Status", font=('times new roman', 18, 'bold'), anchor='w', command=Complaints_status)
    Complaint_status_button.pack(fill=X)

    solved_Complaint_button = Button(leftFrame, text="Complaint Solved", font=('times new roman', 18, 'bold'), anchor='w', command=Complaints_solved)
    solved_Complaint_button.pack(fill=X)

    Settings_button = Button(leftFrame, text="Settings", font=('times new roman', 19, 'bold'), anchor='w',command=settings_page)
    Settings_button.pack(fill=X)

    Exit_button = Button(leftFrame, text="Exit", font=('times new roman', 19, 'bold'), anchor='w',command=exit_app)
    Exit_button.pack(fill=X)

    reg_frame=Frame(root,bg='#2C3E50',bd=3,relief=RIDGE)
    reg_frame.place(x=400,y=125,width=280,height=170)
    reg_icon=PhotoImage(file="register.png")
    reg_icon_label=Label(reg_frame,image=reg_icon)
    reg_icon_label.pack(pady=10)
    reg_icon_label=Label(reg_frame,text="Registered Complaints",bg='#2C3E50',fg="white",font=('times new roman',15,'bold'))
    reg_icon_label.pack()
    reg_count_label=Label(reg_frame,text=0,bg='#2C3E50',fg="white",font=('times new roman',30,'bold'))
    reg_count_label.pack()

    pending_frame=Frame(root,bg='#2C3E50',bd=3,relief=RIDGE)
    pending_frame.place(x=800,y=125,width=280,height=170)
    pending_icon=PhotoImage(file="pending.png")
    pending_icon_label=Label(pending_frame,image=pending_icon)
    pending_icon_label.pack()
    pending_icon_label=Label(pending_frame,text="pending Complaints",bg='#2C3E50',fg="white",font=('times new roman',15,'bold'))
    pending_icon_label.pack()
    pending_count_label=Label(pending_frame,text=0,bg='#2C3E50',fg="white",font=('times new roman',30,'bold'))
    pending_count_label.pack()

    solved_frame=Frame(root,bg='#2C3E50',bd=3,relief=RIDGE)
    solved_frame.place(x=400,y=310,width=280,height=170)
    solved_icon=PhotoImage(file="solved.png")
    solved_icon_label=Label(solved_frame,image=solved_icon)
    solved_icon_label.pack()
    solved_icon_label=Label(solved_frame,text="solvedComplaints",bg='#2C3E50',fg="white",font=('times new roman',15,'bold'))
    solved_icon_label.pack()
    solved_label=Label(solved_frame,text=0,bg='#2C3E50',fg="white",font=('times new roman',30,'bold'))
    solved_label.pack()

    Inprocess_frame=Frame(root,bg='#2C3E50',bd=3,relief=RIDGE)
    Inprocess_frame.place(x=800,y=310,width=280,height=170)
    Inprocess_icon=PhotoImage(file="progress.png")
    Inprocess_icon_label=Label(Inprocess_frame,image=Inprocess_icon)
    Inprocess_icon_label.pack()
    Inprocess_icon_label=Label(Inprocess_frame,text="In process Complaints",bg='#2C3E50',fg="white",font=('times new roman',15,'bold'))
    Inprocess_icon_label.pack()
    Inprocess_label=Label(Inprocess_frame,text=0,bg='#2C3E50',fg="white",font=('times new roman',30,'bold'))
    Inprocess_label.pack()

    total_frame=Frame(root,bg='#2C3E50',bd=3,relief=RIDGE)
    total_frame.place(x=600,y=495,width=280,height=170)
    total_icon=PhotoImage(file="total.png")
    total_icon_label=Label(total_frame,image=total_icon)
    total_icon_label.pack()
    total_icon_label=Label(total_frame,text="total Complaints",bg='#2C3E50',fg="white",font=('times new roman',15,'bold'))
    total_icon_label.pack()
    total_count_label=Label(total_frame,text=0,bg='#2C3E50',fg="white",font=('times new roman',30,'bold'))
    total_count_label.pack()

    total_frame=Frame(root,bg='#2C3E50',bd=3,relief=RIDGE)
    total_frame.place(x=600,y=495,width=280,height=170)
    total_icon=PhotoImage(file="total.png")
    total_icon_label=Label(total_frame,image=total_icon)
    total_icon_label.pack()
    total_icon_label=Label(total_frame,text="total Complaints",bg='#2C3E50',fg="white",font=('times new roman',15,'bold'))
    total_icon_label.pack()
    total_count_label=Label(total_frame,text=0,bg='#2C3E50',fg="white",font=('times new roman',30,'bold'))
    total_count_label.pack()
    
    root.mainloop()
   else:
    root.deiconify()

# Adjust the login_user function
def login_user():
    db = connect_db()
    cursor = db.cursor()

    username = entry_username.get()
    password = entry_password.get()

    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        main_window()  # Open main page after successful login
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

    cursor.close()
    db.close()

# Define a function to handle the submission
def Lodge_form():
    Lodge_frame= Frame(root,width=1070,height=567,bg="white")
    Lodge_frame.place(x=200, y=100)
    headingLabel=Label(Lodge_frame,text="WELCOME ",font=("Times of roman",16,"bold"),bg='#0f4d7d',fg='white')    
    headingLabel.place(x=0,y=0,relwidth=1)
# Declare the image as global to maintain the reference
    global back_image
    back_image=PhotoImage(file="back.png")
    back_button=Button(Lodge_frame,image=back_image,bd=0,cursor='hand2',bg="white",command=lambda: Lodge_frame.place_forget())
    back_button.place(x=10,y=30)
    topFrame=Frame(Lodge_frame,bg="white")
    topFrame.place(x=0,y=60,relwidth=1,height=235)
    # Labels and Entry fields for the form
    Label(topFrame, text="Name:", font=("Times of Roman", 14), bg="white").place(x=20, y=20)
    name_entry = Entry(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    name_entry.place(x=150, y=20, width=400)
    Label(topFrame, text="Reg No:", font=("Times of Roman", 14), bg="white").place(x=20, y=60)
    reg_no_entry = Entry(topFrame, font=("Times of Roman", 12),bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    reg_no_entry.place(x=150, y=60, width=200)
    Label(topFrame, text="Email:", font=("Times of Roman", 14), bg="white").place(x=20, y=100)
    email_entry = Entry(topFrame, font=("Times of Roman", 12),bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    email_entry.place(x=150, y=100, width=200)
    Label(topFrame, text="Department:", font=("Times of Roman", 14), bg="white").place(x=20, y=140)
    department_entry = Entry(topFrame, font=("Times of Roman", 12),bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    department_entry.place(x=150, y=140, width=200)
    Label(topFrame, text="Complaint Description:", font=("Times of Roman", 14), bg="white").place(x=20, y=180)
    complaint_description = Text(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black", wrap='word')
    complaint_description.place(x=230, y=190, width=600, height=200)
   #Submit button
    submit_button = Button(Lodge_frame, text="Submit", font=("Times New Roman", 14), bg='#009688', fg='white', width=20, height=2)
    submit_button.place(x=450, y=350)  # Adjust coordinates as necessary
def View_form():
    global arrow_image
    View_frame = Frame(root, width=1070, height=567, bg="white")
    View_frame.place(x=200, y=100)
    headingLabel = Label(View_frame, text="VIEW COMPLAINTS", font=("Times of Roman", 16, "bold"), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0, y=0, relwidth=1)
# Back utton
    arrow_image=PhotoImage(file="arrow.png")
    arrow_button = Button(View_frame, image=arrow_image, bd=0, cursor='hand2', bg="white", command=lambda: View_frame.place_forget())
    arrow_button.place(x=10, y=30)
    topFrame = Frame(View_frame, bg="white")
    topFrame.place(x=0, y=60, relwidth=1, height=235)
# Label and Entry fields for viewing complaints
    Label(topFrame, text="Reg No:", font=("Times of Roman", 14), bg="white").place(x=20, y=20)
    reg_no_entry = Entry(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    reg_no_entry.place(x=150, y=20, width=400)
    Label(topFrame, text="Complainant ID:", font=("Times of Roman", 14), bg="white").place(x=20, y=60)
    complainant_id_entry = Entry(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    complainant_id_entry.place(x=160, y=60, width=400)
    Label(topFrame, text="Complaint Description:", font=("Times of Roman", 14), bg="white").place(x=20, y=100)
    complaint_description = Text(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black", wrap='word')
    complaint_description.place(x=230, y=100, width=600, height=200)


def Withdraw_form():
    global back_image
    Withdraw_frame = Frame(root, width=1070, height=567, bg="white")
    Withdraw_frame.place(x=200, y=100)
    headingLabel = Label(Withdraw_frame, text="WITHDRAW COMPLAINTS", font=("Times of Roman", 16, "bold"), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0, y=0, relwidth=1)
# Back utton
    global draw_image
    draw_image=PhotoImage(file="draw.png")
    draw_button = Button(Withdraw_frame, image=draw_image, bd=0, cursor='hand2', bg="white", command=lambda:   Withdraw_frame.place_forget())
    draw_button.place(x=10, y=30)
    topFrame = Frame(Withdraw_frame, bg="white")
    topFrame.place(x=0, y=60, relwidth=1, height=235)
    # Labels and Entry fields for withdrawing complaints
    Label(topFrame, text="Reg No:", font=("Times of Roman", 14), bg="white").place(x=20, y=20)
    reg_no_entry = Entry(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    reg_no_entry.place(x=150, y=20, width=400)
    Label(topFrame, text="Complaint ID:", font=("Times of Roman", 14), bg="white").place(x=20, y=60)
    complaint_id_entry = Entry(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    complaint_id_entry.place(x=150, y=60, width=400)
    # Withdraw button
    withdraw_button = Button(Withdraw_frame, text="Withdraw", font=("Times New Roman", 14), bg='#FF5733', fg='white', width=20, height=2)
    withdraw_button.place(x=450, y=350)  # Adjust coordinates as necessary


def Complaints_solved():
    global back_image
    # Solved complaints frame (if needed)
    Solved_frame = Frame(root, width=1070, height=567, bg="white")
    Solved_frame.place(x=200, y=100)
    headingLabel = Label(Solved_frame, text="SOLVED COMPLAINTS", font=("Times of Roman", 16, "bold"), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0, y=0, relwidth=1)
# Back utton
    global comp_image
    comp_image=PhotoImage(file="comp.png")
    comp_button = Button(Solved_frame, image=draw_image, bd=0, cursor='hand2', bg="white", command=lambda:   Solved_frame.place_forget())
    comp_button.place(x=10, y=30)
    topFrame = Frame(Solved_frame, bg="white")
    topFrame.place(x=0, y=60, relwidth=1, height=235)
    # Labels and Entry fields for solved complaints
    Label(topFrame, text="Reg No:", font=("Times of Roman", 14), bg="white").place(x=20, y=20)
    reg_no_entry = Entry(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    reg_no_entry.place(x=150, y=20, width=400)
    Label(topFrame, text="Complaint ID:", font=("Times of Roman", 14), bg="white").place(x=20, y=60)
    complaint_id_entry = Entry(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    complaint_id_entry.place(x=150, y=60, width=400)
    Label(topFrame, text="Solution Description:", font=("Times of Roman", 14), bg="white").place(x=20, y=100)
    solution_description = Text(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black", wrap='word')
    solution_description.place(x=220, y=140, width=600, height=100)


def  Complaints_status():
    global back_image
    Status_frame = Frame(root, width=1070, height=567, bg="white")
    Status_frame.place(x=200, y=100)
    headingLabel = Label(Status_frame, text="CHECK COMPLAINT STATUS", font=("Times of Roman", 16, "bold"), bg='#0f4d7d', fg='white')
    headingLabel.place(x=0, y=0, relwidth=1)
# Back utton
    global status_image
    status_image=PhotoImage(file="comp.png")
    status_button = Button(Status_frame, image=draw_image, bd=0, cursor='hand2', bg="white", command=lambda:   Status_frame.place_forget())
    status_button.place(x=10, y=30)
    topFrame = Frame(Status_frame, bg="white")
    topFrame.place(x=0, y=60, relwidth=1, height=235)
    # Labels and Entry fields for checking complaint status
    Label(topFrame, text="Reg No:", font=("Times of Roman", 14), bg="white").place(x=20, y=20)
    reg_no_entry = Entry(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    reg_no_entry.place(x=150, y=20, width=400)
    Label(topFrame, text="Complaint ID:", font=("Times of Roman", 14), bg="white").place(x=20, y=60)
    complaint_id_entry = Entry(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    complaint_id_entry.place(x=150, y=60, width=400)
    Label(topFrame, text="Status:", font=("Times of Roman", 14), bg="white").place(x=20, y=100)
    status_entry = Entry(topFrame, font=("Times of Roman", 12), bd=2, highlightthickness=2, highlightbackground="black", highlightcolor="black")
    status_entry.place(x=150, y=100, width=400)
    # Submit button for checking status
    check_status_button = Button(Status_frame, text="Check Status", font=("Times New Roman", 14), bg='#009688', fg='white', width=20, height=2)
    check_status_button.place(x=450, y=350)  # Adjust coordinates as necessary


# Callthe login page function to start the applica
login_page()