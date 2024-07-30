from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector as conn
import random
import string

# Setup the database connection
mydb = conn.connect(
    host="localhost",
    user="root",
    password="123456",
    database="airline_ticket"
)
mycursor = mydb.cursor()
def column_exists(cursor, table_name, column_name):
    mycursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}';")
    return mycursor.fetchone() is not None

# Check and add column if it does not exist
if not column_exists(mycursor, 'UserData', 'reservation_id'):
    mycursor.execute("ALTER TABLE UserData ADD COLUMN reservation_id VARCHAR(255);")

if not column_exists(mycursor, 'UserData', 'canceled'):
    mycursor.execute("ALTER TABLE UserData ADD COLUMN canceled TINYINT(1) DEFAULT 0;")
     


# Define flight details
Flights = {
    "New York": "DF2753",
    "Hong Kong": "EN4267",
    "Toronto": "GT4638",
    "London": "KV3323",
    "Sydney": "LV2317",
    "Paris": "BD9032",
}

Flight_Time = {
    "New York": ["9:30am", "2:00pm", "8:00pm"],
    "Hong Kong": ["7:00am", "1:00pm", "6:00pm"],
    "Toronto": ["12:00pm", "7:30pm", "1:00am"],
    "London": ["5:00am", "10:00am", "3:45pm"],
    "Sydney": ["1:00pm", "4:00pm", "7:30pm"],
    "Paris": ["5:00pm", "12:00am", "3:00am"],
}

Meal = ["Asian vegetarian", "Fruit Platter", "Gluten Intolerant", "High Fibre", "Low Fat", "Low Calorie"]

prices = {
    "New York": 550,
    "Hong Kong": 500,
    "Toronto": 400,
    "London": 600,
    "Sydney": 700,
    "Paris": 800,
}

meal_prices = {
    "Asian vegetarian": 20,
    "Fruit Platter": 15,
    "Gluten Intolerant": 25,
    "High Fibre": 18,
    "Low Fat": 20,
    "Low Calorie": 22,
}

def generate_random_alphanumeric_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class Ticket_Reservation:
    def __init__(self,window, username):
        self.username = username
        self.window = window
        self.window.title("Reservation System")
        self.window.geometry("600x600")
        self.window.configure(bg="#2D2D2D")
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        frame = Frame(self.window, bg="#2D2D2D")
        frame.pack(pady=20)

        Label(frame, text="Flight Ticket Reservation", font=("Arial", 30, "bold"), fg="Pink", bg="#2D2D2D").pack(pady=20)
        Button(frame, text="Reserve Ticket", font=("Arial", 20, "bold"), command=self.reserve_ticket, bg="Pink", activebackground="white").pack(pady=20)
        Button(frame, text="Available Flights", font=("Arial", 20, "bold"), command=self.show_available_flights, bg="Pink", activebackground="white").pack(pady=20)
        Button(frame, text="Cancel Reservation", font=("Arial", 20, "bold"), command=self.view_reservations, bg="Pink", activebackground="white").pack(pady=20)

    def reserve_ticket(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        frame = Frame(self.window, bg="#2D2D2D")
        frame.pack(pady=25)

        Label(frame, text="Ticket Reservation", font=("Arial", 30, "bold"), fg="Pink", bg="#2D2D2D").grid(columnspan=3, pady=20)
        Label(frame, text="No. of Passengers", fg="white", bg="#2D2D2D", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.passenger_entry = Entry(frame, font=("Arial", 12))
        self.passenger_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(frame, text="Destination", fg="white", bg="#2D2D2D", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
        self.destination_entry = ttk.Combobox(frame, font=("Arial", 12), values=list(Flights.keys()))
        self.destination_entry.set("Pick an Option")
        self.destination_entry.grid(row=2, column=1, padx=10, pady=10)
        self.destination_entry.bind("<<ComboboxSelected>>", self.update_flight_times)

        Label(frame, text="Time", fg="white", bg="#2D2D2D", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10)
        self.time_entry = ttk.Combobox(frame, font=("Arial", 12), values=[])
        self.time_entry.set("Pick an Option")
        self.time_entry.grid(row=3, column=1, padx=10, pady=10)

        Label(frame, text="Ages (comma-separated):", fg="white", bg="#2D2D2D", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10)
        self.age_entry = Entry(frame, font=("Arial", 12))
        self.age_entry.grid(row=4, column=1, padx=10, pady=10)

        Label(frame, text="Meal", fg="white", bg="#2D2D2D", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=10)

        self.meal_vars = {}
        for i, meal in enumerate(Meal):
            var = BooleanVar()
            chk = Checkbutton(frame, text=meal, variable=var, bg="#2D2D2D", font=("Arial", 12))
            chk.grid(row=5+i, column=1, padx=10, pady=5, sticky="w")
            self.meal_vars[meal] = var

        Button(frame, text="Submit", font=("Arial", 12), command=self.submit_reservation, activebackground="white", bg="Pink").grid(row=6+len(Meal), columnspan=2, padx=10, pady=10)
        Button(frame, text="Back to Main Menu", font=("Arial", 10), command=self.create_main_menu, activebackground="white", bg="Pink").grid(row=7+len(Meal), columnspan=2, padx=10, pady=10)

    def update_flight_times(self, event):
        destination = self.destination_entry.get()
        times = Flight_Time.get(destination, [])
        self.time_entry['values'] = times

    def submit_reservation(self):
        passenger = self.passenger_entry.get()
        destination = self.destination_entry.get()
        time = self.time_entry.get()
        ages = [age.strip() for age in self.age_entry.get().split(',')]

        if not (passenger and destination and time and ages):
            messagebox.showwarning("Input Error", "Please fill in all the required fields.")
            return

        
        try:
            num_passengers = int(passenger)
            if len(ages) != num_passengers:
                messagebox.showwarning("Input Error", "Number of ages provided does not match number of passengers.")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number of passengers.")
            return

        meals = [meal for meal, var in self.meal_vars.items() if var.get()]

        # Generate a unique reservation ID
        reservation_id = self.generate_unique_reservation_id()

        # Calculate the total bill
        seat_price=prices[destination] 
        meal_price=sum(meal_prices[meal] for meal in meals)
        total_bill = seat_price + meal_price
        Ticket_Reservation_Details(self.window, passenger, destination, time, ages, meals,seat_price,meal_price, total_bill, reservation_id)
        self.save_reservation(passenger, destination, time, ages, meals, reservation_id)

    def generate_unique_reservation_id(self):
        while True:
            reservation_id = generate_random_alphanumeric_id()
            if not self.reservation_id_exists(reservation_id):
                return reservation_id

    def reservation_id_exists(self, reservation_id):
        """Check if a reservation ID already exists in the database."""
        query = "SELECT reservation_id FROM UserData WHERE reservation_id = %s"
        mycursor.execute(query, (reservation_id,))
        return mycursor.fetchone() is not None

    def save_reservation(self, passenger, destination, time, ages, meals, reservation_id):
        query = """INSERT INTO UserData (reservation_id, name, passenger, destination, time, ages, meal)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (reservation_id, self.username, passenger, destination, time, ','.join(ages), ','.join(meals))
        mycursor.execute(query, values)
        mydb.commit()

    def show_available_flights(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        frame = Frame(self.window, bg="#2D2D2D")
        frame.pack(pady=20, fill=BOTH, expand=True)

        canvas = Canvas(frame, bg="#2D2D2D")
        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#2D2D2D")

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", configure_scroll_region)

        Label(scrollable_frame, text="Available Flights", font=("Arial", 24, "bold"), fg="Pink", bg="#2D2D2D").pack(pady=10)

        for city, flight_no in Flights.items():
            Label(scrollable_frame, text=f"{city}: Flight No {flight_no}", font=("Arial", 15), fg="white", bg="#2D2D2D").pack(pady=5)
            if city in Flight_Time:
                for time in Flight_Time[city]:
                    Label(scrollable_frame, text=f"   - {time}", font=("Arial", 12), fg="white", bg="#2D2D2D").pack(pady=2)

        Button(scrollable_frame, text="Back to Main Menu", font=("Arial", 12), command=self.create_main_menu, bg="Pink", activebackground="white").pack(padx=10, pady=10)

    def view_reservations(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        frame = Frame(self.window, bg="#2D2D2D")
        frame.pack(pady=20)

        Label(frame, text="Your Reservations", font=("Arial", 24, "bold"), fg="Pink", bg="#2D2D2D").pack(pady=10)

        query = "SELECT reservation_id, destination, time FROM UserData WHERE name = %s AND canceled = FALSE"
        mycursor.execute(query, (self.username,))
        reservations = mycursor.fetchall()

        if reservations:
            for reservation in reservations:
                reservation_id, destination, time = reservation
                reservation_label = Label(frame, text=f"Reservation ID: {reservation_id} | Destination: {destination} | Time: {time}", font=("Arial", 12), fg="white", bg="#2D2D2D")
                reservation_label.pack(pady=5)
                cancel_button = Button(frame, text="Cancel", command=lambda rid=reservation_id: self.cancel_reservation(rid), bg="Pink", activebackground="white")
                cancel_button.pack(pady=2)
        else:
            Label(frame, text="No active reservations found.", font=("Arial", 14), fg="white", bg="#2D2D2D").pack(pady=5)

        Button(frame, text="Back to Main Menu", font=("Arial", 12), command=self.create_main_menu, bg="Pink", activebackground="white").pack(pady=20)

    def cancel_reservation(self, reservation_id):
        if messagebox.askyesno("Cancel Reservation", "Are you sure you want to cancel the reservation?"):
            query = "UPDATE UserData SET canceled = TRUE WHERE reservation_id = %s"
            mycursor.execute(query, (reservation_id,))
            mydb.commit()
            messagebox.showinfo("Success", "Your reservation has been canceled.")
            self.view_reservations()
class Ticket_Reservation_Details:
    def __init__(self, window, passenger, destination, time, ages, meals, seat_price, meal_price, total_bill, reservation_id):
        self.window = window
        self.passenger = passenger
        self.destination = destination
        self.time = time
        self.ages = ages
        self.meals = meals
        self.seat_price = seat_price
        self.meal_price = meal_price
        self.total_bill = total_bill
        self.reservation_id = reservation_id
        self.display()

    def display(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        frame = Frame(self.window, bg="#2D2D2D")
        frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        # Use grid for alignment
        Label(frame, text="Flight Ticket Reservation", font=("Arial", 24, "bold"), fg="Pink", bg="#2D2D2D").grid(row=0, column=0, columnspan=2, pady=10)

        # Reservation ID
        Label(frame, text="Reservation ID:", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        Label(frame, text=f"{self.reservation_id}", font=("Arial", 16, "bold"), fg="Pink", bg="#2D2D2D").grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Destination
        Label(frame, text="Destination:", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        Label(frame, text=f"{self.destination}", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Time
        Label(frame, text="Time:", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        Label(frame, text=f"{self.time}", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Passengers
        Label(frame, text="Passengers:", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        Label(frame, text=f"{self.passenger}", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Ages
        # row_index = 5
        for i, age in enumerate(self.ages, 1):
            Label(frame, text=f"Age of Passenger {i}:", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=5, column=0, sticky="e", padx=10, pady=5)
            Label(frame, text=f"{age}", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=5, column=1, sticky="w", padx=10, pady=5)
            # row_index += 1

        # Meals
        for i, meal in enumerate(self.meals, 1):
            Label(frame, text=f"Meal {i}:", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=6, column=0, sticky="e", padx=10, pady=5)
            Label(frame, text=f"{meal}", font=("Arial", 16), fg="white", bg="#2D2D2D").grid(row=6, column=1, sticky="w", padx=10, pady=5)
          

        # Seat Price
        Label(frame, text="Seat Price:", font=("Arial", 16, "bold"), fg="white", bg="#2D2D2D").grid(row=7, column=0, sticky="e", padx=10, pady=5)
        Label(frame, text=f"${self.seat_price}", font=("Arial", 16, "bold"), fg="white", bg="#2D2D2D").grid(row=7, column=1, sticky="w", padx=10, pady=5)
       

        # Meal Price
        Label(frame, text="Meal Price:", font=("Arial", 16, "bold"), fg="white", bg="#2D2D2D").grid(row=8, column=0, sticky="e", padx=10, pady=5)
        Label(frame, text=f"${self.meal_price}", font=("Arial", 16, "bold"), fg="white", bg="#2D2D2D").grid(row=8, column=1, sticky="w", padx=10, pady=5)
        

        Label(frame, text=f"{"-"*100}", font=("Arial", 16, "bold"), fg="white", bg="#2D2D2D").grid(row=9, columnspan=4, sticky="ew", padx=10, pady=5)

        # Total Bill
        Label(frame, text="Total Bill:", font=("Arial", 16, "bold"), fg="white", bg="#2D2D2D").grid(row=10, column=0, sticky="e", padx=10, pady=5)
        Label(frame, text=f"${self.total_bill}", font=("Arial", 16, "bold"), fg="white", bg="#2D2D2D").grid(row=10, column=1, sticky="w", padx=10, pady=5)
       

        Button(frame, text="Back to Main Menu", command=self.go_to_main_menu, bg="Pink", activebackground="white").grid(row=11, column=0, columnspan=2, pady=20)

    def go_to_main_menu(self):
        self.window.destroy()
        Ticket_Reservation(self.window,username)


username = "YourUsername"
window=Tk()  
app = Ticket_Reservation(window,username)
app.window.mainloop()
