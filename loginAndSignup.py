from tkinter import *
from tkinter import messagebox, font
import mysql.connector as conn


class TicketApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Signup and Signin")
        self.window.geometry("600x600")
        self.window.configure(bg="#2D2D2D")
        self.Ticket_Reservation

        # Connect to the MySQL database
        self.mydb = conn.connect(
            host="localhost",
            user="root",
            password="123456",
            database="airline_ticket"
        )
        self.mycursor =self.mydb.cursor()

        # Create the users table if it doesn't exist
        self.mycursor.execute("""CREATE TABLE  IF NOT EXISTS User(
                name VARCHAR(255),
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255)
            )""")
        
        
        
        self.home()

    def home(self):
            for widget in self.window.winfo_children():
                widget.destroy()
            
            
            frame = Frame(self.window, bg="#2D2D2D")
            frame.place(relx=0.5, rely=0.5, anchor="center")

            custom_font = font.Font(family="Arial", size=30, weight="bold")
            label = Label(frame, text="Airline Ticket Reservation", padx=30, pady=30, fg="Pink", bg="#2D2D2D", font=custom_font)
            label.grid(row=0, columnspan=2, pady=20)

            Button(frame, text="Login", bg="Pink", activebackground="white", padx=10, pady=10, command=self.login).grid(row=1, column=0, padx=10, pady=50, sticky="nsew")
            Button(frame, text="Signup", bg="Pink", activebackground="white", padx=10, pady=10, command=self.signup).grid(row=1, column=1, padx=10, pady=50, sticky="nsew")

    

    def login(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        frame = Frame(self.window, bg="#2D2D2D")
        frame.place(relx=0.4, rely=0.4, anchor="center")

        custom_font = font.Font(family="Arial", size=40, weight="bold")
        login_head = Label(frame, text="Login", font=custom_font, padx=30, pady=30, fg="Pink", bg="#2D2D2D")
        login_head.grid(row=0, columnspan=2, pady=20)

        global username_entry
        label_font = font.Font(family="Arial", size=20)
        Label(frame, text="Username", bg="#2D2D2D", fg="white", font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        username_entry = Entry(frame, font=label_font)
        username_entry.grid(row=1, column=1, padx=10, pady=10)

        global password_entry
        Label(frame, text="Password", bg="#2D2D2D", fg="white", font=label_font).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        password_entry = Entry(frame, font=label_font, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        button_font = font.Font(family="Arial", size=18)
        Button(frame, text="Submit", bg="Pink", activebackground="white", padx=10, pady=10, command=self.login_submit, font=button_font).grid(row=3, columnspan=2, padx=20, pady=20)
        
    def login_submit(self):
        username = username_entry.get()
        password = password_entry.get()
        
        self.mycursor.execute("SELECT * FROM User WHERE name = %s AND password = %s", (username, password))
        user = self.mycursor.fetchone()
        
        if user:
            messagebox.showinfo("Success", "Successfully logged in!")
            self.Ticket_Reservation(username)

        elif(username=="" or password==""):
            messagebox.showwarning("Error", "field must not be empty")
            self.login()
        else:
            messagebox.showwarning("Error", "Invalid username or password")

    def signup(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        frame = Frame(self.window, bg="#2D2D2D")
        frame.place(relx=0.4, rely=0.4, anchor="center")

        custom_font = font.Font(family="Arial", size=40, weight="bold")
        signup_head = Label(frame, text="Signup", font=custom_font, padx=30, pady=30, fg="Pink", bg="#2D2D2D")
        signup_head.grid(row=0, columnspan=2, pady=20)

        global username_entry
        label_font = font.Font(family="Arial", size=20)
        Label(frame, text="Username", bg="#2D2D2D", fg="white", font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        username_entry = Entry(frame, font=label_font)
        username_entry.grid(row=1, column=1, padx=10, pady=10)

        global email_entry
        Label(frame, text="Email ID", bg="#2D2D2D", fg="white", font=label_font).grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        email_entry = Entry(frame, font=label_font)
        email_entry.grid(row=2, column=1, padx=10, pady=10)
        
        global password_entry
        Label(frame, text="Password", bg="#2D2D2D", fg="white", font=label_font).grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        password_entry = Entry(frame, font=label_font, show="*")
        password_entry.grid(row=3, column=1, padx=10, pady=10)
        
        global confirm_password_entry
        Label(frame, text="Confirm Password", bg="#2D2D2D", fg="white", font=label_font).grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        confirm_password_entry = Entry(frame, font=label_font, show="*")
        confirm_password_entry.grid(row=4, column=1, padx=10, pady=10)

        button_font = font.Font(family="Arial", size=18)
        Button(frame, text="Submit", bg="Pink", activebackground="white", padx=10, pady=10, command=self.signin_submit, font=button_font).grid(row=5, columnspan=2, padx=20, pady=20)
        # Button(frame, text="Back", bg="Pink", activebackground="white", padx=10, pady=10, command=home, font=button_font).grid(row=5, column=2, padx=20, pady=10)

    def signin_submit(self):
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        
        if password != confirm_password:
            messagebox.showwarning("Error", "Passwords do not match")
            self.signup()

        elif username=="" or email=="" or password=="" or confirm_password=="":
            messagebox.showwarning("Error", "field must not be empty")
            self.signup()

        
        elif len(password)<8:
            messagebox.showwarning("Error", "Password must be at least 8 characters long")
            self.signup()

        else:
            try:
                self.mycursor.execute("INSERT INTO User (name, email, password) VALUES (%s, %s, %s)", (username, email, password))
                self.mydb.commit()  # Commit changes to the database
                messagebox.showinfo("Success", "Successfully signed up!")
                self.Ticket_Reservation(username)
            except conn.IntegrityError:
                messagebox.showwarning("Error", "Email already exists")
                self.signup()
            except Exception as e:
                print("Error:", e)
                messagebox.showerror("Error", "An error occurred. Please try again later.")

    
    def Ticket_Reservation(self,username):
        from Reservation import Ticket_Reservation
        for widget in self.window.winfo_children():
            widget.destroy() 
        Ticket_Reservation(self.window,username)
        
        


root=Tk()
app=TicketApp(root)
root.mainloop()